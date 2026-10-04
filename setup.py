import os
import platform
import subprocess
import sys

venv = ".venv"

# Create virtual environment
subprocess.check_call([sys.executable, "-m", "venv", venv])

# Find the venv's Python/pip
if platform.system() == "Windows":
    python = os.path.join(venv, "Scripts", "python.exe")
else:
    python = os.path.join(venv, "bin", "python")

# Install dependencies
subprocess.check_call([
    python, "-m", "pip", "install", "-r", "requirements.txt"
])

print("Setup complete!")