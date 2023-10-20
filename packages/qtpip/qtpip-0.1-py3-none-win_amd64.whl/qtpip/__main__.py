import sys
import subprocess
from pathlib import Path


if __name__ == "__main__":
    install_dir = Path(__file__).parent
    subprocess.run([f"{install_dir / 'qtpip'}"] + sys.argv[1:])
