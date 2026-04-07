#!/bin/bash
# Quick system information script for Termux Command Center

echo "=== System Information ==="
echo "Device: $(getprop ro.product.model)"
echo "Android Version: $(getprop ro.build.version.release)"
echo "Termux Version: $TERMUX_VERSION"
echo "Architecture: $(uname -m)"
echo "Kernel: $(uname -r)"
echo ""

echo "=== Network Information ==="
echo "IP Address: $(ip route get 1 | awk '{print $7}')"
echo "MAC Address: $(ip link | grep -o 'link/ether [0-9a-f:]*' | head -1 | cut -d' ' -f2)"
echo "Gateway: $(ip route | grep default | awk '{print $3}')"
echo ""

echo "=== Storage Information ==="
echo "Internal Storage:"
df -h /data | tail -1
echo ""
echo "External Storage:"
df -h /storage/emulated/0 2>/dev/null || echo "No external storage detected"
echo ""

echo "=== Battery Information ==="
termux-battery-status 2>/dev/null || echo "Battery info not available"
echo ""

echo "=== Running Processes ==="
ps aux | head -10