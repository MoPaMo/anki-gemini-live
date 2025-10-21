"""
Gemini Live Dialog - Main UI for voice-based card review
"""

from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, Qt, QProgressBar
)
from aqt import mw
from aqt.utils import showWarning, tooltip

from .gemini_client import GeminiLiveClient
from .audio_handler import AudioHandler
from .card_presenter import CardPresenter


class GeminiLiveDialog(QDialog):
    """Main dialog for Gemini Live review session"""
    
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        self.gemini_client = None
        self.audio_handler = AudioHandler()
        self.card_presenter = CardPresenter(mw.col, config)
        
        self.session_active = False
        self.current_card = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Anki Gemini Live")
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Ready to start")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.status_label)
        
        # Current card display
        card_label = QLabel("Current Card:")
        layout.addWidget(card_label)
        
        self.card_display = QTextEdit()
        self.card_display.setReadOnly(True)
        self.card_display.setMaximumHeight(150)
        layout.addWidget(self.card_display)
        
        # Transcript area
        transcript_label = QLabel("Conversation:")
        layout.addWidget(transcript_label)
        
        self.transcript = QTextEdit()
        self.transcript.setReadOnly(True)
        layout.addWidget(self.transcript)
        
        # Progress bar for audio activity
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Session")
        self.start_button.clicked.connect(self.start_session)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Session")
        self.stop_button.clicked.connect(self.stop_session)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.mute_button = QPushButton("Mute Mic")
        self.mute_button.clicked.connect(self.toggle_mute)
        self.mute_button.setEnabled(False)
        button_layout.addWidget(self.mute_button)
        
        layout.addLayout(button_layout)
        
        # Close button
        close_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close_dialog)
        close_layout.addStretch()
        close_layout.addWidget(close_button)
        layout.addLayout(close_layout)
        
        self.setLayout(layout)
        
    def start_session(self):
        """Start Gemini Live session"""
        try:
            self.status_label.setText("Connecting to Gemini...")
            self.start_button.setEnabled(False)
            
            # Initialize Gemini client
            self.gemini_client = GeminiLiveClient(self.config["gemini_api_key"])
            self.gemini_client.connect(
                on_audio=self.on_gemini_audio,
                on_text=self.on_gemini_text,
                on_error=self.on_error
            )
            
            # Wait a bit for connection
            from aqt.qt import QTimer
            QTimer.singleShot(1000, self.on_connected)
            
        except Exception as e:
            self.on_error(f"Failed to start session: {str(e)}")
            
    def on_connected(self):
        """Called when connection is established"""
        try:
            # Setup system instruction for Gemini
            system_instruction = self._create_system_instruction()
            self.gemini_client.setup_voice_mode(system_instruction)
            
            # Get first card
            self.current_card = self.card_presenter.get_next_card()
            if not self.current_card:
                showWarning("No cards available for review.")
                self.close_dialog()
                return
                
            # Display card question
            question = self.card_presenter.get_card_question(self.current_card)
            self.card_display.setText(question)
            
            # Start audio recording
            self.audio_handler.start_recording(self.on_audio_recorded)
            
            # Send initial prompt to Gemini
            initial_prompt = f"Let's review this flashcard. The question is: {question}. Please ask me this question in a natural, conversational way."
            self.gemini_client.send_text(initial_prompt)
            
            self.session_active = True
            self.status_label.setText("Session Active - Speak naturally!")
            self.stop_button.setEnabled(True)
            self.mute_button.setEnabled(True)
            self.progress_bar.setValue(50)
            
            self.add_to_transcript("System", "Session started. Gemini will ask you the question.")
            
        except Exception as e:
            self.on_error(f"Connection error: {str(e)}")
            
    def _create_system_instruction(self) -> str:
        """Create system instruction for Gemini"""
        instruction = """You are a friendly study partner helping someone review their Anki flashcards.

Your role:
1. Ask the flashcard question in a natural, conversational way
2. Listen carefully to the user's answer
3. Evaluate if their answer is correct and complete
4. Rate the answer as: Again (wrong/don't know), Hard (partially correct), Good (correct), or Easy (perfect/very confident)
5. Provide encouraging feedback
6. If requested, explain concepts or provide additional context

Guidelines:
- Be conversational and supportive, not robotic
- If the answer is partially correct, acknowledge what's right and gently guide them
- For incorrect answers, give the correct answer and a brief explanation
- Keep responses concise but helpful
- After evaluating, clearly state the rating (Again/Hard/Good/Easy)
"""
        
        if self.config.get("explanation_enabled"):
            instruction += "\n- Be ready to answer follow-up questions and provide deeper explanations"
            
        return instruction
        
    def on_audio_recorded(self, audio_data: bytes):
        """Handle recorded audio from microphone"""
        if self.session_active and self.gemini_client:
            self.gemini_client.send_audio(audio_data)
            # Visual feedback for recording
            self.progress_bar.setValue(75)
            from aqt.qt import QTimer
            QTimer.singleShot(100, lambda: self.progress_bar.setValue(50))
            
    def on_gemini_audio(self, audio_data: bytes):
        """Handle audio response from Gemini"""
        if self.session_active:
            self.audio_handler.play_audio(audio_data)
            # Visual feedback for playback
            self.progress_bar.setValue(100)
            from aqt.qt import QTimer
            QTimer.singleShot(200, lambda: self.progress_bar.setValue(50))
            
    def on_gemini_text(self, text: str):
        """Handle text response from Gemini"""
        self.add_to_transcript("Gemini", text)
        
        # Check if Gemini provided a rating
        rating = self._extract_rating(text)
        if rating:
            self.rate_card(rating)
            
    def _extract_rating(self, text: str) -> str or None:
        """Extract rating from Gemini's response"""
        text_lower = text.lower()
        
        # Look for explicit rating statements
        if "rating: again" in text_lower or "rate this again" in text_lower:
            return "again"
        elif "rating: hard" in text_lower or "rate this hard" in text_lower:
            return "hard"
        elif "rating: good" in text_lower or "rate this good" in text_lower:
            return "good"
        elif "rating: easy" in text_lower or "rate this easy" in text_lower:
            return "easy"
            
        # Look for rating keywords at end of response
        words = text_lower.split()
        if len(words) > 0:
            last_words = " ".join(words[-5:])
            if "again" in last_words and ("incorrect" in text_lower or "wrong" in text_lower):
                return "again"
            elif "hard" in last_words:
                return "hard"
            elif "easy" in last_words:
                return "easy"
            elif "good" in last_words or "correct" in text_lower:
                return "good"
                
        return None
        
    def rate_card(self, rating: str):
        """Rate the current card and move to next"""
        if not self.current_card:
            return
            
        # Map rating to Anki ease
        ease_map = {
            "again": 1,
            "hard": 2,
            "good": 3,
            "easy": 4
        }
        
        ease = ease_map.get(rating, 3)
        
        # Answer the card in Anki
        self.card_presenter.answer_card(self.current_card, ease)
        
        tooltip(f"Card rated: {rating.title()}")
        self.add_to_transcript("System", f"Card rated as: {rating.title()}")
        
        # Get next card
        from aqt.qt import QTimer
        QTimer.singleShot(2000, self.load_next_card)
        
    def load_next_card(self):
        """Load the next card for review"""
        self.current_card = self.card_presenter.get_next_card()
        
        if not self.current_card:
            self.add_to_transcript("System", "All cards reviewed! Great job!")
            tooltip("Review session complete!")
            from aqt.qt import QTimer
            QTimer.singleShot(2000, self.stop_session)
            return
            
        # Display new card
        question = self.card_presenter.get_card_question(self.current_card)
        self.card_display.setText(question)
        
        # Prompt Gemini to ask the new question
        prompt = f"Let's move to the next card. The question is: {question}. Please ask me this question."
        self.gemini_client.send_text(prompt)
        
        self.add_to_transcript("System", "Moving to next card...")
        
    def add_to_transcript(self, speaker: str, message: str):
        """Add message to transcript"""
        self.transcript.append(f"<b>{speaker}:</b> {message}<br>")
        
    def toggle_mute(self):
        """Toggle microphone mute"""
        if self.audio_handler.is_recording():
            self.audio_handler.stop_recording()
            self.mute_button.setText("Unmute Mic")
            self.status_label.setText("Microphone Muted")
        else:
            self.audio_handler.start_recording(self.on_audio_recorded)
            self.mute_button.setText("Mute Mic")
            self.status_label.setText("Session Active - Speak naturally!")
            
    def stop_session(self):
        """Stop the Gemini Live session"""
        self.session_active = False
        
        if self.audio_handler:
            self.audio_handler.stop_recording()
            self.audio_handler.stop_playback()
            
        if self.gemini_client:
            self.gemini_client.disconnect()
            
        self.status_label.setText("Session Stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.mute_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.add_to_transcript("System", "Session ended.")
        
    def on_error(self, error_msg: str):
        """Handle errors"""
        self.add_to_transcript("Error", error_msg)
        showWarning(f"Error: {error_msg}")
        self.stop_session()
        
    def close_dialog(self):
        """Close the dialog"""
        self.stop_session()
        if self.audio_handler:
            self.audio_handler.cleanup()
        self.accept()
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.close_dialog()
        event.accept()
