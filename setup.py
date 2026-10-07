import platform
import subprocess
import sys
from pathlib import Path

script_dir = Path(__file__).parent.resolve()

venv_dir = script_dir / ".venv"

# Create virtual environment
subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])

# Find the venv's Python/pip
if platform.system() == "Windows":
    python = venv_dir / "Scripts" / "python.exe"
else:
    python = venv_dir / "bin" / "python"

# Install dependencies
subprocess.check_call([
    str(python), "-m", "pip", "install", "-r", str(script_dir / "requirements.txt")
])

print("Setup complete!")
input("Press enter to continue...")