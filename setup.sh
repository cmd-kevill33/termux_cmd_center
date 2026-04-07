#!/bin/bash
# Termux Command Center Setup Script
# This script sets up the necessary directories, installs dependencies, and configures Termux for the Command Center.

set -e

echo "Setting up Termux Command Center..."

# Check if running in Termux
if [ -z "$TERMUX_VERSION" ]; then
    echo "Warning: This script is designed for Termux. Some features may not work on other systems."
fi

# Create main directory
CMD_CENTER_DIR="$HOME/termux_cmd_center"
echo "Creating directory: $CMD_CENTER_DIR"
mkdir -p "$CMD_CENTER_DIR"

# Create subdirectories
echo "Creating subdirectories..."
mkdir -p "$CMD_CENTER_DIR/config"
mkdir -p "$CMD_CENTER_DIR/modules"
mkdir -p "$CMD_CENTER_DIR/tools"
mkdir -p "$CMD_CENTER_DIR/logs"
mkdir -p "$CMD_CENTER_DIR/data"

# Copy files from repo to CMD_CENTER_DIR
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Copying files from $REPO_DIR to $CMD_CENTER_DIR"
cp -r "$REPO_DIR"/* "$CMD_CENTER_DIR/" 2>/dev/null || true

# Install Python if not installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    pkg install python -y
fi

# Install required packages
echo "Installing comprehensive pen testing toolkit..."
pkg update && pkg upgrade -y

# Core networking and system tools
pkg install curl wget git python python2 ruby perl php nodejs golang openssh netcat-openbsd -y

# Essential security tools
pkg install nmap nikto dirb hydra john-the-ripper hashcat aircrack-ng tcpdump wireshark-gtk sqlmap metasploit -y

# Additional network tools
pkg install netdiscover arp-scan hping3 masscan dnsutils traceroute mtr -y

# Web application testing
pkg install wpscan joomlavs -y

# Forensics and analysis
pkg install binwalk foremost scalpel exiftool -y

# Password cracking
pkg install medusa patator cewl -y

# Wireless tools
pkg install reaver bully pixiewps -y

# Mobile testing
pkg install apktool jadx -y

# Cloud tools
pkg install awscli -y

# Development and scripting
pkg install vim nano tmux screen -y

# Termux API for advanced features
pkg install termux-api -y

# Install Python dependencies
if [ -f "$CMD_CENTER_DIR/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r "$CMD_CENTER_DIR/requirements.txt"
fi

# Set up storage access
echo "Setting up storage access..."
termux-setup-storage

# Configure Termux properties for better functionality
TERMUX_PROPS="$HOME/.termux/termux.properties"
if [ ! -f "$TERMUX_PROPS" ]; then
    mkdir -p "$HOME/.termux"
    cat > "$TERMUX_PROPS" << EOF
# Termux Command Center Configuration
extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]
EOF
    echo "Created termux.properties with extra keys configuration."
else
    echo "termux.properties already exists. Please manually add extra-keys if desired."
fi

# Create a launcher script
LAUNCHER="$CMD_CENTER_DIR/launch.sh"
cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
# Launcher for Termux Command Center
cd "$HOME/termux_cmd_center"
python3 main.py "$@"
EOF
chmod +x "$LAUNCHER"

# Add to PATH or create alias
SHELL_RC="$HOME/.bashrc"
if ! grep -q "termux_cmd_center" "$SHELL_RC"; then
    echo "Adding alias to $SHELL_RC"
    echo "alias cmdcenter='cd \$HOME/termux_cmd_center && python3 main.py'" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:\$HOME/termux_cmd_center\"" >> "$SHELL_RC"
fi

echo "Setup complete!"
echo "Run 'cmdcenter' or 'cd ~/termux_cmd_center && python3 main.py' to start."
echo "Restart Termux or run 'source ~/.bashrc' to use the alias."