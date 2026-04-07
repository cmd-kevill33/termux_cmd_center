#!/bin/bash
# Basic honeypot setup script for Termux Command Center

PORT=${1:-2222}
LOGFILE="$HOME/termux_cmd_center/logs/honeypot_$(date +%Y%m%d_%H%M%S).log"

echo "Setting up basic honeypot on port $PORT"
echo "Logs will be saved to $LOGFILE"
echo "Press Ctrl+C to stop"
echo ""

# Create log directory if it doesn't exist
mkdir -p "$HOME/termux_cmd_center/logs"

# Start honeypot
while true; do
    echo "$(date): Connection attempt on port $PORT" >> "$LOGFILE"
    nc -l -p $PORT -e sh 2>> "$LOGFILE" &
    NC_PID=$!
    wait $NC_PID
done