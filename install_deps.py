"""
Dependency installer for Anki Gemini Live
Run this script from Anki's add-on folder to install required packages
"""

import sys
import subprocess
import os


def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies for Anki Gemini Live...")
    
    # Get the directory where this script is located
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(addon_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print(f"Error: requirements.txt not found at {requirements_file}")
        return False
    
    # Install packages to the add-on directory
    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            requirements_file,
            "--target",
            addon_dir,
            "--upgrade"
        ])
        print("\n✓ Dependencies installed successfully!")
        print("\nPlease restart Anki for the changes to take effect.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error installing dependencies: {e}")
        print("\nYou may need to install manually:")
        print(f"  pip install -r {requirements_file} --target {addon_dir}")
        return False


if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
