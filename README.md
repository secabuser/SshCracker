# SSH Cracker

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

##  How to Use
### Linux
#### Step 1: Install Prerequisites
- Check if Python 3.x is installed:
  ```bash
  python3 --version
- If Python is not installed, install it using your package manager:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
- Next, install the required libraries:
  ```bash
  pip3 install paramiko pyfiglet colorama

### Windows
#### Step 1: Install Python
- Download and install Python 3.x from the official Python website : https://www.python.org/
- During installation, make sure to check the box that says Add Python to PATH
- Verify that Python is installed by opening Command Prompt (cmd) and typing:
  ``bash
  python --version
You should see the installed Python version.

#### Step 2: Install Required Libraries
- Open Command Prompt (cmd)
- Install the required libraries by running:
  ```bash
  pip install paramiko pyfiglet colorama
- Confirm that the libraries are installed by typing:
 ```bash
  pip list

  
  
