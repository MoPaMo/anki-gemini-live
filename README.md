# Anki Gemini Live

An Anki extension that connects to Google's Gemini Live API to provide a natural voice-based flashcard review experience. It's like having a study partner who asks you questions, listens to your answers, evaluates them, and provides helpful feedback - all through natural conversation.

## Features

- 🎤 **Voice Interaction**: Speak naturally with Gemini AI during card reviews
- 🔊 **Audio Responses**: Hear questions and feedback in Gemini's voice
- ✅ **Automatic Rating**: AI evaluates your answers and rates cards accordingly
- 💡 **Explanations**: Ask for clarifications and deeper understanding
- 📚 **Seamless Integration**: Works with your existing Anki decks and scheduling

## How It Works

1. Start a Gemini Live session from Anki's Tools menu
2. Gemini asks you flashcard questions in a natural voice
3. You answer verbally through your microphone
4. Gemini evaluates your answer and rates it (Again/Hard/Good/Easy)
5. Get feedback, explanations, and move to the next card
6. Your review progress is automatically saved to Anki

## Installation

### Prerequisites

- Anki 2.1.50 or later
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Python 3.9 or later (comes with Anki)
- Working microphone and speakers

### Steps

1. **Download the Add-on**
   - Clone or download this repository
   - Or install from AnkiWeb (once published)

2. **Install in Anki**
   - Open Anki
   - Go to Tools → Add-ons → View Files
   - Copy the `anki-gemini-live` folder into the add-ons directory
   - Restart Anki

3. **Install Dependencies**
   
   The add-on requires `websockets` and `pyaudio`. Install them:
   
   **Option A - Using Terminal (Recommended)**
   ```bash
   # Navigate to the add-on folder
   cd ~/Documents/Anki2/addons21/anki_gemini_live/
   
   # Install dependencies
   pip install -r requirements.txt --target .
   ```
   
   **Option B - Manual Installation**
   - Windows: `%APPDATA%\Anki2\addons21\anki_gemini_live\`
   - Mac: `~/Library/Application Support/Anki2/addons21/anki_gemini_live/`
   - Linux: `~/.local/share/Anki2/addons21/anki_gemini_live/`

4. **Configure API Key**
   - In Anki, go to Tools → Add-ons
   - Select "Anki Gemini Live"
   - Click "Config"
   - Enter your Gemini API key in the `gemini_api_key` field
   - Click "OK"

## Usage

### Starting a Session

1. Make sure you have cards due for review
2. Go to Tools → Start Gemini Live Session
3. The dialog will open and connect to Gemini
4. Wait for Gemini to ask the first question
5. Answer naturally using your microphone
6. Listen to feedback and ratings
7. Continue through your cards!

### During a Session

- **Speak naturally**: No need for commands, just answer the questions
- **Ask for help**: Say things like "Can you explain that?" or "I don't understand"
- **Mute/Unmute**: Use the Mute button if needed
- **Stop anytime**: Click Stop Session to end early

### Configuration Options

Access via Tools → Add-ons → Anki Gemini Live → Config:

- `gemini_api_key`: Your Google Gemini API key **(required)**
- `voice_language`: Language for voice recognition (default: "en-US")
- `auto_rate_threshold`: Confidence threshold for automatic rating (0.0-1.0)
- `voice_detection_sensitivity`: Microphone sensitivity (0.0-1.0)
- `explanation_enabled`: Enable/disable AI explanations (true/false)

## Architecture

The add-on consists of several key components:

```
anki-gemini-live/
├── __init__.py              # Entry point
├── main.py                  # Menu setup and session launcher
├── gemini_client.py         # Gemini Live API WebSocket client
├── audio_handler.py         # Audio recording and playback
├── gemini_live_dialog.py    # Main UI dialog
├── card_presenter.py        # Anki card interactions
├── config.json              # Default configuration
└── manifest.json            # Add-on metadata
```

### Key Technologies

- **Gemini Live API**: Google's real-time multimodal AI
- **WebSockets**: Bidirectional streaming communication
- **PyAudio**: Audio I/O handling
- **Anki API**: Card scheduling and review management
- **PyQt6**: User interface

## Troubleshooting

### "No module named 'websockets'" Error

Make sure you installed the dependencies:
```bash
pip install -r requirements.txt --target .
```

### Microphone Not Working

- Check your system microphone permissions
- Ensure PyAudio is properly installed
- Try adjusting `voice_detection_sensitivity` in config

### Connection Issues

- Verify your API key is correct
- Check your internet connection
- Ensure firewall allows WebSocket connections

### No Audio Playback

- Check system audio output settings
- Verify speakers are working in other applications
- Try adjusting system volume

## Privacy & Security

- Your API key is stored locally in Anki's configuration
- Audio is streamed directly to Google's Gemini API
- No data is stored or logged by this add-on
- Review Google's privacy policy for Gemini API usage

## Development

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/MoPaMo/anki-gemini-live.git
cd anki-gemini-live

# Install dependencies
pip install -r requirements.txt

# Symlink to Anki add-ons folder for testing
ln -s $(pwd) ~/Documents/Anki2/addons21/anki_gemini_live
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with Anki
5. Submit a pull request

## Limitations

- Requires active internet connection
- Gemini API usage may incur costs (check Google's pricing)
- Voice recognition quality depends on microphone and environment
- Currently only supports Gemini 2.0 Flash Exp model

## Roadmap

- [ ] Support for multiple languages
- [ ] Customizable voice personalities
- [ ] Session statistics and analytics
- [ ] Offline mode with local TTS/STT
- [ ] Mobile device support
- [ ] Study group mode (multiple users)

## License

MIT License - see LICENSE file for details

## Credits

Created by MoPaMo

Powered by:
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Anki](https://apps.ankiweb.net/)

## Support

- [Report Issues](https://github.com/MoPaMo/anki-gemini-live/issues)
- [Discussions](https://github.com/MoPaMo/anki-gemini-live/discussions)

## Changelog

### v0.1.0 (Initial Release)
- Voice-based card review with Gemini Live
- Automatic answer evaluation and rating
- Real-time audio streaming
- Configuration dialog for API key
- Support for explanations and feedback