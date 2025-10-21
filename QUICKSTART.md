# Quick Start Guide

Get started with Anki Gemini Live in 5 minutes!

## Prerequisites

- ✅ Anki 2.1.50 or later installed
- ✅ Working microphone and speakers
- ✅ Internet connection
- ✅ Google account

## Quick Setup

### 1. Get API Key (2 minutes)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in and click "Create API Key"
3. Copy your key

### 2. Install Add-on (2 minutes)

```bash
# Navigate to Anki add-ons folder
cd ~/Library/Application\ Support/Anki2/addons21/  # Mac
cd %APPDATA%\Anki2\addons21\  # Windows
cd ~/.local/share/Anki2/addons21/  # Linux

# Clone the repository
git clone https://github.com/MoPaMo/anki-gemini-live.git anki_gemini_live

# Install dependencies
cd anki_gemini_live
pip install -r requirements.txt --target .
```

### 3. Configure (1 minute)

1. Open Anki
2. Tools → Add-ons → Anki Gemini Live → Config
3. Paste your API key in `gemini_api_key`
4. Save and restart Anki

## First Session

1. **Start**: Tools → Start Gemini Live Session
2. **Listen**: Gemini asks the question
3. **Answer**: Speak your answer naturally
4. **Feedback**: Hear evaluation and rating
5. **Continue**: Move to next card automatically

## Tips

- 💡 Speak naturally - no commands needed
- 🔇 Use "Mute Mic" if you need a break
- ❓ Ask questions like "Can you explain that?"
- ⏸️ Click "Stop Session" to end early

## Having Issues?

See [SETUP.md](SETUP.md) for detailed troubleshooting.

---

Enjoy your AI study partner! 🎓✨
