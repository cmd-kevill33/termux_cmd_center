# START HERE: Termux Command Center Beginner Guide

Welcome to the Termux Command Center. This file is your first stop if you are new to Termux or security tooling.

It contains step-by-step setup commands, configuration instructions, and usage commands that will get the tool working from scratch.

---

## 1. Install Termux and Termux:API

1. Install Termux from F-Droid or the official website.
2. Open Termux.
3. Install the Termux API package:

```bash
pkg update && pkg upgrade -y
pkg install termux-api -y
```

4. Grant Termux storage access:

```bash
termux-setup-storage
```

When prompted, allow storage permission. This is required so the app can read and write logs, backups, and reports.

---

## 2. Install Git and Python in Termux

Termux needs Git to clone the repository and Python to run the tool.

```bash
pkg install python git -y
```

Verify Python and Git:

```bash
python --version
git --version
```

If `python` is not found, use `python3`.

---

## 3. Clone the repository into Termux

Choose a directory where you want the tool to live. The recommended location is Termux home or shared storage.

```bash
cd ~
mkdir -p termux_cmd_center
cd termux_cmd_center
git clone https://github.com/cmd-kevill33/termux_cmd_center.git .
```

If the repository is already cloned in a folder, use that folder and skip the clone step.

---

## 4. Install Python dependencies

Install all required Python packages using pip:

```bash
pip install --user -r requirements.txt
```

If the command fails because a package is missing or cannot compile, install these extra Termux packages first:

```bash
pkg install clang make libffi-dev openssl-dev python-dev -y
```

Then run the pip install command again.

---

## 5. Make the command center executable

Set executable permissions for the main script and setup script:

```bash
chmod +x main.py setup.sh
```

---

## 6. Optional: Run the automated setup script

The setup script installs many additional security tools used by the command center.

```bash
./setup.sh
```

This may take a while and will install tools such as `nmap`, `sqlmap`, `metasploit`, `john`, and others.

> If you only want the Python features, you can skip this step.

---

## 7. Start the Termux Command Center

Launch the application:

```bash
python main.py
```

If `python` is not found, use:

```bash
python3 main.py
```

You will see the main menu. Use the number keys to choose each option.

---

## 8. What to do first

Use these first commands to get familiar with the tool:

1. Run the dashboard:
   - Choose `1` and review system metrics.
2. Start automated monitoring:
   - Choose `2` and follow prompts.
3. Scan a network:
   - Choose `3`, enter a target like `192.168.1.0/24`, and run a scan.
4. Test mobile features:
   - Choose `9` and try location, camera, or battery status.

---

## 9. Configure API keys

To use third-party intelligence sources, add API keys to `configs/api_keys.json`.

Example structure:

```json
{
  "virustotal": {
    "api_key": "YOUR_VIRUSTOTAL_KEY",
    "rate_limit": 4,
    "timeout": 30
  },
  "shodan": {
    "api_key": "YOUR_SHODAN_KEY",
    "rate_limit": 1,
    "timeout": 10
  }
}
```

If the file does not exist, create it manually.

---

## 10. Basic commands for inexperienced users

### Verify the setup

```bash
ls -la
python --version
python main.py
```

### View the repository contents

```bash
pwd
ls -la
find . -maxdepth 2 -type f
```

### If the program fails

1. Make sure you are in the cloned folder.
2. Run:
   ```bash
   python main.py
   ```
3. If the error says `matplotlib` or `seaborn` missing, install them:
   ```bash
   pip install --user matplotlib seaborn pandas
   ```
4. If the error says `termux-api` missing, install:
   ```bash
   pkg install termux-api -y
   ```

---

## 11. Recommended Termux command sequence

If you want a single sequence of commands to run from scratch, use this:

```bash
pkg update && pkg upgrade -y
pkg install python git termux-api clang make libffi-dev openssl-dev python-dev -y
termux-setup-storage
cd ~
mkdir -p termux_cmd_center
cd termux_cmd_center
git clone https://github.com/cmd-kevill33/termux_cmd_center.git .
pip install --user -r requirements.txt
chmod +x main.py setup.sh
./setup.sh
python main.py
```

> You can skip `./setup.sh` if you do not need the full toolchain.

---

## 12. Help and support

If you need more help:
- Open `README.md`
- Open `USER_GUIDE.md`
- Review the `modules/` folder to see feature descriptions
- Use the main menu in the app for interactive help

---

## 13. Important safety note

This tool is for authorized security testing only. Do not use it on networks or devices you do not own or have permission to test.

---

Congratulations, you are ready to run the Termux Command Center.

If you want, I can also add a direct `start` command alias and a simple beginner menu entry to the README.