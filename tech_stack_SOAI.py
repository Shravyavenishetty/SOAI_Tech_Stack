import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path

VENV_DIR = Path(".venv")

def run_command(command, exit_on_error=True):
    print(f"\n▶️ Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print("❌ Command failed.")
        if exit_on_error:
            sys.exit(1)
    return result.returncode

def install_uv():
    if shutil.which("uv"):
        print("✅ uv is already installed globally.")
        return

    print("📦 Installing uv...")

    os_name = platform.system()
    if os_name == "Linux":
        run_command("curl -Ls https://astral.sh/uv/install.sh | bash")
    elif os_name == "Darwin":
        run_command("curl -Ls https://astral.sh/uv/install.sh | bash")
    elif os_name == "Windows":
        run_command("powershell -Command \"iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex\"")
    else:
        print("❌ Unsupported OS.")
        sys.exit(1)

def create_uv_virtualenv():
    if VENV_DIR.exists():
        print(f"✅ Virtual environment already exists at '{VENV_DIR}'")
    else:
        print(f"📦 Creating virtual environment at '{VENV_DIR}' using uv...")
        run_command(f"uv venv {VENV_DIR}")

    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"

def install_with_uv(venv_python, packages):
    for pkg in packages:
        print(f"📦 Installing: {pkg}")
        run_command(f"uv pip install --python {venv_python} --upgrade {pkg}")

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
    install_uv()
    venv_python = create_uv_virtualenv()

    packages = [
        "jupyterlab==4.2.1",
        "streamlit>=1.40"
    ]
    install_with_uv(venv_python, packages)

    install_git()
    install_vscode()

    print("\n✅ Setup complete!")
    print("\n👉 To activate the virtual environment manually:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")

if __name__ == "__main__":
    main()
