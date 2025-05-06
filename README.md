Automates setup by creating a Python virtual environment, installing required tools (`uv`, `jupyterlab`, `streamlit`), and ensuring Git & VS Code are available.
Includes OS-specific logic to optionally activate the environment after setup.

**Requirements:**

Python 3.11+ must be installed
The script uses **python3 -m venv** and expects Python 3.

Check with:
**python3 --version**

**Linux (Debian/Ubuntu):**
Required:
**sudo apt update**
**sudo apt install -y python3.11 python3.11-venv python3.11-distutils curl git unzip**

**For Windows:**

Open Command Prompt:
Press Windows + R, type cmd, and press Enter.

Download Python Using curl:
First, ensure that curl is installed on your system (it comes pre-installed with Windows 10 and 11). To download Python, run the following command:
**curl -O https://www.python.org/ftp/python/3.x.x/python-3.11.3.exe**

**For MacOS:**

Open Terminal:
Press Cmd + Space, type Terminal, and press Enter to open the Terminal.

Install Homebrew (if not already installed):
If you don’t have Homebrew installed, you can install it by running the following command:
**/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"**
Follow the on-screen instructions to complete the installation.

Install Python Using Homebrew:
Once Homebrew is installed, run the following command to install the latest version of Python:
**brew install python**

Verify Python Installation:
After installation, you can verify that Python is installed correctly by typing:
**python3 --version**

