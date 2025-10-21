"""
Anki Gemini Live - Voice-based card review using Google's Gemini Live API

This add-on enables natural voice conversations with Gemini AI for reviewing
Anki flashcards. It feels like having a study partner who asks questions,
evaluates answers, and provides feedback.
"""

from . import main

def init():
    """Initialize the add-on"""
    main.setup_addon()
