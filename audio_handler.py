"""
Audio recording and playback handler
Manages microphone input and speaker output
"""

import pyaudio
import wave
import threading
import queue
from typing import Callable, Optional


class AudioHandler:
    """Handles audio recording and playback for voice interaction"""
    
    # Audio configuration matching Gemini Live API requirements
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # 16kHz sample rate for Gemini
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.playing = False
        self.record_thread = None
        self.playback_thread = None
        self.audio_callback = None
        self.playback_queue = queue.Queue()
        
    def start_recording(self, callback: Callable[[bytes], None]):
        """Start recording audio from microphone"""
        if self.recording:
            return
            
        self.audio_callback = callback
        self.recording = True
        self.record_thread = threading.Thread(target=self._record_loop, daemon=True)
        self.record_thread.start()
        
    def _record_loop(self):
        """Recording loop - captures audio and sends to callback"""
        try:
            stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            while self.recording:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    if self.audio_callback:
                        self.audio_callback(data)
                except Exception as e:
                    print(f"Recording error: {e}")
                    break
                    
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.recording = False
            
    def stop_recording(self):
        """Stop recording audio"""
        self.recording = False
        if self.record_thread:
            self.record_thread.join(timeout=1.0)
            
    def play_audio(self, audio_data: bytes):
        """Queue audio data for playback"""
        self.playback_queue.put(audio_data)
        
        # Start playback thread if not already running
        if not self.playing:
            self.playing = True
            self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
            self.playback_thread.start()
            
    def _playback_loop(self):
        """Playback loop - plays audio from queue"""
        try:
            stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK
            )
            
            while self.playing or not self.playback_queue.empty():
                try:
                    # Get audio data from queue with timeout
                    audio_data = self.playback_queue.get(timeout=0.5)
                    
                    # Play audio in chunks
                    for i in range(0, len(audio_data), self.CHUNK * 2):
                        chunk = audio_data[i:i + self.CHUNK * 2]
                        stream.write(chunk)
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Playback error: {e}")
                    break
                    
            stream.stop_stream()
            stream.close()
            self.playing = False
            
        except Exception as e:
            print(f"Failed to start playback: {e}")
            self.playing = False
            
    def stop_playback(self):
        """Stop audio playback"""
        self.playing = False
        # Clear the queue
        while not self.playback_queue.empty():
            try:
                self.playback_queue.get_nowait()
            except queue.Empty:
                break
                
        if self.playback_thread:
            self.playback_thread.join(timeout=1.0)
            
    def cleanup(self):
        """Clean up audio resources"""
        self.stop_recording()
        self.stop_playback()
        self.audio.terminate()
        
    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.recording
        
    def is_playing(self) -> bool:
        """Check if currently playing audio"""
        return self.playing or not self.playback_queue.empty()
