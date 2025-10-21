"""
Google Gemini Live API client
Handles WebSocket connection and audio streaming
"""

import json
import base64
import asyncio
import websockets
from typing import Callable, Optional
import threading
import queue


class GeminiLiveClient:
    """Client for Google Gemini Live API with voice support"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws = None
        self.is_connected = False
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.loop = None
        self.thread = None
        
    def connect(self, on_audio: Callable, on_text: Callable, on_error: Callable):
        """Connect to Gemini Live API"""
        self.on_audio = on_audio
        self.on_text = on_text
        self.on_error = on_error
        
        # Start async event loop in separate thread
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        
    def _run_event_loop(self):
        """Run asyncio event loop in separate thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_ws())
        
    async def _connect_ws(self):
        """Establish WebSocket connection"""
        # Gemini Live API endpoint
        url = f"wss://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:streamGenerateContent?key={self.api_key}"
        
        try:
            async with websockets.connect(url, max_size=10**7) as ws:
                self.ws = ws
                self.is_connected = True
                
                # Start tasks for sending and receiving
                await asyncio.gather(
                    self._send_loop(),
                    self._receive_loop()
                )
        except Exception as e:
            self.on_error(f"Connection error: {str(e)}")
            self.is_connected = False
            
    async def _send_loop(self):
        """Send audio data from queue to Gemini"""
        while self.is_connected:
            try:
                # Get audio chunk from queue (non-blocking with timeout)
                audio_data = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.audio_queue.get(timeout=0.1)
                )
                
                if audio_data is None:  # Stop signal
                    break
                    
                # Send audio chunk to Gemini
                message = {
                    "realtimeInput": {
                        "mediaChunks": [{
                            "mimeType": "audio/pcm",
                            "data": base64.b64encode(audio_data).decode('utf-8')
                        }]
                    }
                }
                await self.ws.send(json.dumps(message))
                
            except queue.Empty:
                await asyncio.sleep(0.01)
            except Exception as e:
                self.on_error(f"Send error: {str(e)}")
                break
                
    async def _receive_loop(self):
        """Receive responses from Gemini"""
        while self.is_connected:
            try:
                response = await self.ws.recv()
                data = json.loads(response)
                
                # Handle different response types
                if "serverContent" in data:
                    content = data["serverContent"]
                    
                    # Handle text response
                    if "modelTurn" in content:
                        parts = content["modelTurn"].get("parts", [])
                        for part in parts:
                            if "text" in part:
                                self.on_text(part["text"])
                    
                    # Handle audio response
                    if "realtimeAudio" in content:
                        audio_data = base64.b64decode(
                            content["realtimeAudio"]["data"]
                        )
                        self.on_audio(audio_data)
                        
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                self.on_error(f"Receive error: {str(e)}")
                break
                
    def send_audio(self, audio_data: bytes):
        """Queue audio data to be sent to Gemini"""
        if self.is_connected:
            self.audio_queue.put(audio_data)
            
    def send_text(self, text: str):
        """Send text message to Gemini"""
        if self.is_connected and self.loop:
            asyncio.run_coroutine_threadsafe(
                self._send_text_async(text),
                self.loop
            )
            
    async def _send_text_async(self, text: str):
        """Send text message asynchronously"""
        message = {
            "clientContent": {
                "turns": [{
                    "role": "user",
                    "parts": [{"text": text}]
                }],
                "turnComplete": True
            }
        }
        await self.ws.send(json.dumps(message))
        
    def setup_voice_mode(self, system_instruction: str):
        """Configure the session with system instructions"""
        if self.is_connected and self.loop:
            asyncio.run_coroutine_threadsafe(
                self._setup_voice_mode_async(system_instruction),
                self.loop
            )
            
    async def _setup_voice_mode_async(self, system_instruction: str):
        """Setup voice mode configuration"""
        setup_message = {
            "setup": {
                "model": "models/gemini-2.0-flash-exp",
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "Aoede"
                            }
                        }
                    }
                },
                "systemInstruction": {
                    "parts": [{"text": system_instruction}]
                }
            }
        }
        await self.ws.send(json.dumps(setup_message))
        
    def disconnect(self):
        """Disconnect from Gemini Live API"""
        self.is_connected = False
        self.audio_queue.put(None)  # Stop signal
        
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
