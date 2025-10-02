# TODO: MOVE THIS TO A BETTER LOCATION MAYBE I THINK IT WILL BE GOOD TO SEPARATE MODULES FOR WEB_SERVER AND API_APPLICATION.

# Default Imports
import subprocess
import sys

# Local Imports
from . import constants as CONSTANTS


def run_echo_new_window(message: str):
    if sys.platform == "win32":
        # Windows: launches a new Command Prompt window
        subprocess.Popen(["start", "cmd", "/k", f"echo {message}"], shell=True)
    elif sys.platform == "darwin":
        # macOS: launches a new Terminal window
        apple_script = f"""
        tell application "Terminal"
            do script "echo {message}"
        end tell
        """
        subprocess.Popen(["osascript", "-e", apple_script])
    else:
        # Linux: launches a new terminal (try gnome-terminal, fallback to x-terminal-emulator)
        try:
            subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c", f"echo {message}; exec bash"]
            )
        except FileNotFoundError:
            subprocess.Popen(["x-terminal-emulator", "-e", f"echo {message}; bash"])
