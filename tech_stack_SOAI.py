import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path

VENV_DIR = Path(".venv")  # Hidden venv directory

def run_command(command, exit_on_error=True):
    print(f"\n▶️ Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0 and exit_on_error:
        print("❌ Command failed. Exiting.")
        sys.exit(1)

def install_uv():
    # Check if uv is installed globally
    result = subprocess.run("uv --version", shell=True, stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        print("📦 Installing 'uv' globally using curl...")
        os_name = platform.system()
        if os_name == "Linux":
            run_command("curl -sSL https://github.com/urxvt/uv/releases/latest/download/uv-linux-x86_64.tar.gz | tar -xz -C /usr/local/bin")
        elif os_name == "Darwin":
            run_command("curl -L https://github.com/urxvt/uv/releases/latest/download/uv-darwin-x86_64.tar.gz | tar -xz -C /usr/local/bin")
        elif os_name == "Windows":
            run_command("curl -LO https://github.com/urxvt/uv/releases/latest/download/uv-win64.zip")
            run_command("unzip uv-win64.zip -d C:\\Program Files\\uv")
            print("Make sure 'C:\\Program Files\\uv' is added to your PATH.")
    else:
        print("✅ 'uv' is already installed globally.")

def create_virtualenv_with_uv():
    if not VENV_DIR.exists():
        print(f"📦 Creating virtual environment in '{VENV_DIR}' using 'uv'...")
        run_command(f"uv venv {VENV_DIR}")
    else:
        print(f"✅ Virtual environment already exists at '{VENV_DIR}'")

    # Get platform-specific python path inside the venv
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"

def ensure_uv_in_venv(venv_python):
    result = subprocess.run(f"{venv_python} -m uv --version", shell=True, stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        print("📦 Installing 'uv' inside the virtual environment...")
        run_command(f"{venv_python} -m pip install --upgrade pip")
        run_command(f"{venv_python} -m pip install uv")
    else:
        print("✅ 'uv' is already available in the virtual environment.")

def install_with_uv(venv_python, packages):
    for pkg in packages:
        print(f"📦 Installing: {pkg}")
        run_command(f"{venv_python} -m uv pip install --upgrade {pkg}")

def install_git():
    if shutil.which("git"):
        print("✅ Git is already installed.")
        return

    print("📦 Installing Git...")
    os_name = platform.system()
    if os_name == "Linux":
        run_command("sudo apt update && sudo apt install -y git")
    elif os_name == "Darwin":
        run_command("brew install git")
    elif os_name == "Windows":
        run_command("winget install --id Git.Git -e --source winget")

def install_vscode():
    if shutil.which("code"):
        print("✅ VS Code is already installed.")
        return

    print("📦 Installing Visual Studio Code...")
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
    install_uv()  # Install uv globally
    create_virtualenv_with_uv()  # Create virtual environment with uv
    venv_python = VENV_DIR / "bin" / "python" if platform.system() != "Windows" else VENV_DIR / "Scripts" / "python.exe"
    ensure_uv_in_venv(venv_python)

    packages = [
        "jupyterlab==4.2.1",
        "streamlit>=1.40"
    ]
    install_with_uv(venv_python, packages)

    install_git()
    install_vscode()

    print("\n✅ Setup complete!")
    print(f"\n👉 To activate the virtual environment manually:")
    if platform.system() == "Windows":
        print(f"   .venv\\Scripts\\activate")
    else:
        print(f"   source .venv/bin/activate")

if __name__ == "__main__":
    main()
