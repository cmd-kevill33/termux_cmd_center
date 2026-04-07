#!/bin/bash
# Quick network scan script for Termux Command Center

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    echo "Example: $0 192.168.1.1 or $0 example.com"
    exit 1
fi

echo "=== Quick Network Scan for $TARGET ==="
echo ""

echo "1. Ping test:"
ping -c 4 $TARGET
echo ""

echo "2. Basic port scan (top 1000 ports):"
nmap -T4 --top-ports 1000 $TARGET
echo ""

echo "3. Service detection:"
nmap -sV -T4 --top-ports 100 $TARGET
echo ""

echo "4. OS detection:"
nmap -O $TARGET
echo ""

echo "5. Vulnerability scan (basic):"
nmap --script vuln -T4 $TARGET
echo ""

echo "Scan complete. Use detailed modules for more comprehensive analysis."