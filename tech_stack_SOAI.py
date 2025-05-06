import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path

VENV_DIR = Path(".venv")  # Virtual environment directory

def run_command(command, exit_on_error=True):
    print(f"\n Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0 and exit_on_error:
        print(" Command failed. Exiting.")
        sys.exit(1)

def install_uv():
    # Check if uv is installed globally
    result = subprocess.run("uv --version", shell=True, stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print(" 'uv' is already installed globally.")
        return

    print(" Installing 'uv' globally using curl...")
    os_name = platform.system()
    if os_name == "Linux":
        run_command("curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz -C /usr/local/bin")
    elif os_name == "Darwin":
        run_command("curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-apple-darwin.tar.gz | tar -xz -C /usr/local/bin")
    elif os_name == "Windows":
        run_command("curl -LO https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip")
        run_command("powershell -Command \"Expand-Archive -Force uv-x86_64-pc-windows-msvc.zip -DestinationPath 'C:\\Program Files\\uv'\"")
        print(" Please add 'C:\\Program Files\\uv' to your PATH manually.")

def create_virtualenv_with_uv():
    if not VENV_DIR.exists():
        print(f" Creating virtual environment in '{VENV_DIR}' using 'uv'...")
        run_command(f"uv venv {VENV_DIR}")
    else:
        print(f" Virtual environment already exists at '{VENV_DIR}'")

    # Get platform-specific python path inside the venv
    return VENV_DIR / ("Scripts" if platform.system() == "Windows" else "bin") / "python"

def install_with_uv(venv_python, packages):
    for pkg in packages:
        print(f" Installing: {pkg}")
        run_command(f"{venv_python} -m uv pip install --upgrade {pkg}")

def install_git():
    if shutil.which("git"):
        print(" Git is already installed.")
        return

    print(" Installing Git...")
    os_name = platform.system()
    if os_name == "Linux":
        run_command("sudo apt update && sudo apt install -y git")
    elif os_name == "Darwin":
        run_command("brew install git")
    elif os_name == "Windows":
        run_command("winget install --id Git.Git -e --source winget")

def install_vscode():
    if shutil.which("code"):
        print(" VS Code is already installed.")
        return

    print(" Installing Visual Studio Code...")
    os_name = platform.system()
    if os_name == "Linux":
        run_command("curl -LO https://update.code.visualstudio.com/latest/linux-deb-x64/stable")
        run_command("sudo apt install ./stable")
    elif os_name == "Darwin":
        run_command("curl -L -o vscode.zip https://update.code.visualstudio.com/latest/darwin/universal/stable")
        run_command("unzip vscode.zip -d /Applications")
    elif os_name == "Windows":
        run_command("curl -LO https://update.code.visualstudio.com/latest/win32-x64-user/stable")
        run_command("start stable")

def main():
    install_uv()
    venv_python = create_virtualenv_with_uv()

    packages = [
        "jupyterlab==4.2.1",
        "streamlit>=1.40"
    ]
    install_with_uv(venv_python, packages)

    install_git()
    install_vscode()

    print("\n Setup complete!")
    print("\n To activate the virtual environment manually:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")

if __name__ == "__main__":
    main()
