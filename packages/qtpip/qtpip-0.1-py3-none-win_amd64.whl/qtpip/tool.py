import sys
import subprocess
from pathlib import Path


def run_qtpip():
    module_directory = Path(__file__).parent
    ext = ".exe" if sys.platform == "win32" else ""
    binary = f"qtpip{ext}"
    subprocess.run([module_directory / binary] + sys.argv[1:])
