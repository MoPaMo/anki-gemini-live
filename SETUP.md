# Setup Guide for Anki Gemini Live

This guide will help you get Anki Gemini Live up and running.

## Step 1: Get a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (keep it secure!)

## Step 2: Install the Add-on

### Method A: From GitHub (Development)

1. Clone or download this repository:
   ```bash
   git clone https://github.com/MoPaMo/anki-gemini-live.git
   ```

2. Locate your Anki add-ons folder:
   - **Windows**: `%APPDATA%\Anki2\addons21\`
   - **Mac**: `~/Library/Application Support/Anki2/addons21/`
   - **Linux**: `~/.local/share/Anki2/addons21/`

3. Copy the entire `anki-gemini-live` folder to the add-ons directory

4. Rename it to `anki_gemini_live` (underscore instead of hyphen)

### Method B: From AnkiWeb (Coming Soon)

Once published on AnkiWeb:
1. Open Anki
2. Go to Tools → Add-ons → Get Add-ons
3. Enter the add-on code
4. Click OK

## Step 3: Install Dependencies

The add-on requires two Python packages: `websockets` and `pyaudio`.

### Easy Installation (Recommended)

1. Open Anki
2. Go to Tools → Add-ons
3. Select "Anki Gemini Live"
4. Click "View Files"
5. In the opened folder, run:
   ```bash
   python install_deps.py
   ```
6. Restart Anki

### Manual Installation

If the easy method doesn't work:

```bash
# Navigate to the add-on folder
cd /path/to/Anki2/addons21/anki_gemini_live/

# Install dependencies
pip install websockets pyaudio --target .
```

### Platform-Specific Notes

#### Windows
- Make sure Python is in your PATH
- You may need to install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) for PyAudio

#### Mac
- Install PortAudio first: `brew install portaudio`
- Then install PyAudio: `pip install pyaudio`

#### Linux
- Install PortAudio development files:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install portaudio19-dev
  
  # Fedora
  sudo dnf install portaudio-devel
  
  # Arch
  sudo pacman -S portaudio
  ```

## Step 4: Configure the Add-on

1. Open Anki
2. Go to Tools → Add-ons
3. Select "Anki Gemini Live"
4. Click "Config"
5. Enter your Gemini API key:
   ```json
   {
       "gemini_api_key": "YOUR_API_KEY_HERE",
       "voice_language": "en-US",
       "auto_rate_threshold": 0.8,
       "voice_detection_sensitivity": 0.5,
       "explanation_enabled": true
   }
   ```
6. Click "OK"
7. Restart Anki

## Step 5: Test Your Setup

1. Make sure you have some cards due for review
2. Go to Tools → Start Gemini Live Session
3. Allow microphone access if prompted
4. Wait for Gemini to connect and ask the first question
5. Answer naturally using your voice!

## Troubleshooting

### "Module not found" Errors

If you see errors about missing modules:
1. Make sure dependencies are installed in the add-on folder (not globally)
2. Check that you used `--target .` when installing
3. Restart Anki after installing dependencies

### Microphone Issues

1. Check system microphone permissions
2. Test your microphone in other applications
3. Try adjusting `voice_detection_sensitivity` in config
4. Make sure no other application is using the microphone

### Connection Errors

1. Verify your API key is correct
2. Check your internet connection
3. Make sure Gemini API is enabled for your project
4. Check if your firewall blocks WebSocket connections

### Audio Playback Issues

1. Check system audio settings
2. Test audio in other applications
3. Make sure speakers/headphones are connected
4. Try adjusting system volume

### PyAudio Installation Fails

**Windows:**
- Install from pre-built wheel: `pip install pipwin && pipwin install pyaudio`

**Mac:**
- Install PortAudio first: `brew install portaudio`

**Linux:**
- Install system dependencies first (see Platform-Specific Notes above)

## Getting Help

If you're still having issues:

1. Check the [GitHub Issues](https://github.com/MoPaMo/anki-gemini-live/issues)
2. Look at [Discussions](https://github.com/MoPaMo/anki-gemini-live/discussions)
3. Create a new issue with:
   - Your operating system
   - Anki version
   - Error messages
   - Steps to reproduce

## Next Steps

Once everything is working:

- Review the [README.md](README.md) for usage tips
- Customize settings in the config
- Start your first voice review session!
- Share your feedback and suggestions

Happy studying! 🎓
