"""
Main module for Anki Gemini Live add-on
Sets up the menu action and initializes the extension
"""

from aqt import mw, gui_hooks
from aqt.qt import QAction
from aqt.utils import showInfo, showWarning

from .gemini_live_dialog import GeminiLiveDialog


def start_gemini_live_session():
    """Start a new Gemini Live review session"""
    config = mw.addonManager.getConfig(__name__)
    
    # Check if API key is configured
    if not config.get("gemini_api_key"):
        showWarning(
            "Please configure your Gemini API key in:\n"
            "Tools → Add-ons → Anki Gemini Live → Config\n\n"
            "Get your API key from: https://makersuite.google.com/app/apikey"
        )
        return
    
    # Check if there are cards due for review
    if mw.col.sched.counts()[0] == 0:
        showInfo("No cards are due for review right now.")
        return
    
    # Open the Gemini Live dialog
    dialog = GeminiLiveDialog(mw, config)
    dialog.exec()


def setup_menu():
    """Add menu item to Anki's Tools menu"""
    action = QAction("Start Gemini Live Session", mw)
    action.triggered.connect(start_gemini_live_session)
    mw.form.menuTools.addAction(action)


def setup_addon():
    """Initialize the add-on"""
    # Setup menu when profile is loaded
    gui_hooks.profile_did_open.append(setup_menu)
