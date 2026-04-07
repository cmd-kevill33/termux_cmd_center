# Termux Command Center User Guide

## Overview

The Termux Command Center is a modular Android security toolkit built for Termux. It supports purple teaming, OSINT, reconnaissance, penetration testing, monitoring, mobile security, and secure operations.

This user guide explains:
- How to install and set up the tool in Termux
- Required dependencies and Termux packages
- How to use each module
- Real usage examples
- Configuration and API key setup
- Troubleshooting and tips

## Requirements

### Android Requirements
- Android device with Termux installed
- Termux API installed (`termux-api` package)
- Storage access granted
- Device network access for scanning and API calls

### Termux Requirements
- Python 3.x (`python` package)
- Git (`git` package)
- Required Termux packages: `wget`, `curl`, `openssh`, `proot`, `termux-exec`

### Recommended Packages
```bash
pkg update && pkg upgrade
pkg install python git termux-api curl wget nano
termux-setup-storage
```

## Clone the repository into Termux

Open Termux and run:

```bash
cd ~/storage/shared
mkdir termux_cmd_center
cd termux_cmd_center
git clone https://github.com/cmd-kevill33/termux_cmd_center.git .
```

> If you cloned into another folder, replace `~/storage/shared` with that path.

## Install dependencies

### Python dependencies

Inside the repository folder:

```bash
pip install --user -r requirements.txt
```

If `pip install` fails because of missing build tools, install the required packages:

```bash
pkg install clang make libffi-dev openssl-dev python-dev
```

### Termux API setup

Install Termux API support:

```bash
pkg install termux-api
```

Then grant storage and permission access when prompted:

```bash
termux-setup-storage
```

## Make scripts executable

Run:

```bash
chmod +x setup.sh
chmod +x main.py
```

## Optional automated setup

The repository includes `setup.sh` to help install tools.
Use it if you want to install all supported security packages automatically:

```bash
./setup.sh
```

> Note: This script may require additional permissions and storage space. If you only need the Python features, the `pip` step is sufficient.

## Start the Command Center

Launch the application with:

```bash
python main.py
```

If `python` is not available, use `python3`:

```bash
python3 main.py
```

## Main menu overview

When the application starts, you will see a menu with these options:

1. Dashboard
2. Automated Monitoring
3. Advanced Scanner
4. API Integrations
5. AI/ML Analysis
6. Reporting & Visualization
7. Collaboration
8. Performance Monitoring
9. Mobile Features
10. Backup & Restore
11. Security Hardening

Use the number keys to navigate.

## Module usage examples

### 1. Dashboard

The Dashboard provides a real-time view of system and network status.

Example:

- Select `1` from the main menu
- View CPU, memory, network, and process statistics
- Check alerts for abnormal activity

Use it to monitor Termux resource usage while scanning or testing.

### 2. Automated Monitoring

This module runs background monitoring and logs events.

Example:

- Select `2`
- Configure monitoring intervals and thresholds
- Enable alert notifications for high CPU, disk, or network activity

This is ideal for long-running reconnaissance or threat detection.

### 3. Advanced Scanner

The scanner module supports intelligent network scans.

Example:

- Select `3`
- Enter a target IP or subnet, for example `192.168.1.0/24`
- Choose automatic scan profiles and active detection

Use it for host discovery, service enumeration, and vulnerability mapping.

### 4. API Integrations

This module integrates third-party intelligence sources.

Example:

- Select `4`
- Add API keys for VirusTotal, Shodan, or IPInfo
- Query IP addresses and domains
- Cache results for faster repeated lookup

### 5. AI/ML Analysis

Use this for anomaly detection and pattern recognition.

Example:

- Select `5`
- Load network or event data
- Run a statistical analysis or machine learning model
- Review anomalous events and predictive alerts

### 6. Reporting & Visualization

Generate charts and reports for your findings.

Example:

- Select `6`
- Create an overview report or timeline
- Save charts to the `data/charts` folder

If `matplotlib` is not installed, this module will still load but visualization features may be disabled.

### 7. Collaboration

Used to organize team operations and shared knowledge.

Example:

- Select `7`
- Add users and assign roles
- Share notes, alerts, and project tasks

This helps coordinate red/blue team activities.

### 8. Performance Monitoring

Track device performance and optimize usage.

Example:

- Select `8`
- Start monitoring CPU, memory, disk, and network
- View performance analytics over time

Useful when running heavy scans or exploit tools.

### 9. Mobile Features

This module uses Termux:API for Android-specific capabilities.

Example:

- Select `9`
- Use camera capture, GPS location, sensor readings, and device info
- Access battery stats, notifications, and basic device security checks

These features work only on Android with Termux:API installed.

### 10. Backup & Restore

Use this module to protect configuration and data.

Example:

- Select `10`
- Create a full or configuration-only backup
- Restore a backup when needed
- Export/import data to JSON, CSV, XML, SQL, or YAML

### 11. Security Hardening

Secure your Termux environment and verify compliance.

Example:

- Select `11`
- Review encryption and audit logging status
- Enable rate limiting and input validation
- Generate security reports

## Termux-specific setup notes

### Grant storage permission

Always run:

```bash
termux-setup-storage
```

This allows the app to read and write logs, backups, and report files.

### Install Termux API commands

For mobile features, install:

```bash
pkg install termux-api
```

Then test basic API access:

```bash
termux-camera-photo -c 1 /sdcard/test.jpg
termux-location-get
termux-battery-status
```

### Python environment

Termux sometimes uses `python3` by default. If `python main.py` fails, use:

```bash
python3 main.py
```

## Configuration

### API keys

Add your API keys to `configs/api_keys.json` if it exists. Example structure:

```json
{
  "virustotal": {
    "api_key": "YOUR_KEY",
    "rate_limit": 4,
    "timeout": 30
  },
  "shodan": {
    "api_key": "YOUR_KEY",
    "rate_limit": 1,
    "timeout": 10
  }
}
```

### Custom settings

- `data/` stores logs, reports, backups, and security data
- `configs/` stores custom configurations
- `modules/` contains feature modules

## Working examples

### Example 1: Basic reconnaissance

```bash
cd ~/termux_cmd_center
python main.py
```
- Choose `3` for Advanced Scanner
- Enter `192.168.1.0/24`
- Use the default scan profile

### Example 2: Collect device location

```bash
cd ~/termux_cmd_center
python main.py
```
- Choose `9` for Mobile Features
- Select location services

### Example 3: Create a backup

```bash
cd ~/termux_cmd_center
python main.py
```
- Choose `10` Backup & Restore
- Create a full backup

## Troubleshooting

### The app fails to start

- Ensure you are in the repository directory
- Run `python main.py` or `python3 main.py`
- Install dependencies: `pip install --user -r requirements.txt`
- Use `termux-setup-storage`

### Missing Termux API support

- Install `pkg install termux-api`
- Grant permissions when prompted

### Visualizations not working

If `matplotlib` or `seaborn` is missing, install them manually:

```bash
pip install --user matplotlib seaborn pandas
```

### Git clone only shows README

That means the repository on GitHub was not updated yet. Run these commands from the correct Termux directory:

```bash
git clone https://github.com/cmd-kevill33/termux_cmd_center.git
cd termux_cmd_center
ls -la
```

## Best practices

- Use this toolkit only on devices and networks you own or have permission to test.
- Keep API keys secret and secure.
- Back up your data before making major changes.
- Run `./setup.sh` only when you are ready to install tools.

## What to do next

1. Install Termux packages and Python dependencies
2. Run `python main.py`
3. Explore the dashboard first
4. Configure API integrations if you need OSINT intelligence
5. Use mobile features only on Android devices with Termux:API

## Support

If you need help, open an issue on GitHub or review the `README.md` and `USER_GUIDE.md` for details.
