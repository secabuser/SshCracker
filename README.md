# SSH Cracker

A Python-based tool for multi-threaded SSH ‌‌Cracking

## Features
- **Multi-threaded Testing:** Quickly scan multiple IPs with configurable thread limits.
- **Detailed Logging:** Outputs results to separate log files for success, errors, and no access.
- **User-Friendly Interface:** Clear, colorful, and interactive console interface.
- **Asynchronous Logging:** Ensures smooth performance without delays.

## Requirements
- Python 3.x
- Required libraries:
  - `paramiko`
  - `pyfiglet`
  - `colorama`

Install dependencies using:
```bash
pip install -r requirements.txt


---

## How to Use

### Linux
#### Step 1: Install Prerequisites
1. Check if Python 3.x is installed:
   ```bash
   python3 --version

2. If Python is not installed, install it using your package manager:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip

### Linux
#### Step 1: Install Python
1. Download and install Python 3.x from the official Python website:
  https://www.python.org/
2. During installation, check the box that says Add Python to PATH.
3. Verify the installation by opening Command Prompt (cmd) and typing:
  ```cmd
  python --version
#### Step 2: Install Required Libraries
1. Open Command Prompt (cmd).
2. Install the required libraries by running:
  ```cmd
  pip install paramiko pyfiglet colorama
#### Step 3: Run the Script
- Execute the script using:
  ```cmd
  python main.py
