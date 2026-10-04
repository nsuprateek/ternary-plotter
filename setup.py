import os
import platform
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
input("Press enter to continue...")