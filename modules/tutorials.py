"""
Tutorials Module for Termux Command Center
Detailed guides and tutorials for various security topics.
"""

import os
from pathlib import Path

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Detailed guides and tutorials"
        self.tutorials_dir = self.cc.data_dir / "tutorials"
        self.tutorials_dir.mkdir(exist_ok=True)
        self.create_sample_tutorials()

    def run(self):
        print("\n=== Tutorials & Guides ===")
        print("1. Basic Linux commands")
        print("2. Network reconnaissance")
        print("3. Web application testing")
        print("4. Wireless security")
        print("5. Social engineering")
        print("6. Incident response")
        print("7. Malware analysis")
        print("8. Forensics")
        print("9. Cryptography basics")
        print("10. Programming for security")
        print("11. Create custom tutorial")
        print("12. View all tutorials")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.show_tutorial("linux_basics.md")
            elif choice == "2":
                self.show_tutorial("recon_tutorial.md")
            elif choice == "3":
                self.show_tutorial("web_testing.md")
            elif choice == "4":
                self.show_tutorial("wireless_security.md")
            elif choice == "5":
                self.show_tutorial("social_engineering.md")
            elif choice == "6":
                self.show_tutorial("incident_response.md")
            elif choice == "7":
                self.show_tutorial("malware_analysis.md")
            elif choice == "8":
                self.show_tutorial("forensics.md")
            elif choice == "9":
                self.show_tutorial("cryptography.md")
            elif choice == "10":
                self.show_tutorial("security_programming.md")
            elif choice == "11":
                self.create_tutorial()
            elif choice == "12":
                self.list_tutorials()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def create_sample_tutorials(self):
        tutorials = {
            "linux_basics.md": """
# Basic Linux Commands for Security Professionals

## File Operations
- `ls -la`: List files with details
- `cat file.txt`: Display file contents
- `grep "pattern" file.txt`: Search for text
- `find /path -name "*.txt"`: Find files

## Process Management
- `ps aux`: Show running processes
- `kill PID`: Terminate process
- `top`: Monitor processes

## Network Tools
- `ifconfig` or `ip addr`: Network interfaces
- `ping host`: Test connectivity
- `netstat -tuln`: Open ports

## Package Management (Termux)
- `pkg update && pkg upgrade`: Update packages
- `pkg install package_name`: Install package
- `pkg list-installed`: Show installed packages
""",
            "recon_tutorial.md": """
# Network Reconnaissance Tutorial

## Passive Reconnaissance
1. WHOIS lookup: `whois domain.com`
2. DNS enumeration: `dig domain.com ANY`
3. Shodan search: `shodan search "hostname:target.com"`

## Active Reconnaissance
1. Port scanning: `nmap -p- target.com`
2. Service detection: `nmap -sV target.com`
3. OS fingerprinting: `nmap -O target.com`

## Web Reconnaissance
1. Directory busting: `dirb http://target.com /usr/share/wordlists/dirb/common.txt`
2. Technology detection: `whatweb http://target.com`
3. SSL analysis: `sslscan target.com`

## Tips
- Always get permission before active scanning
- Use VPN or Tor for anonymity
- Document everything for reporting
""",
            "web_testing.md": """
# Web Application Testing Guide

## Information Gathering
- Identify technologies: `whatweb http://target.com`
- Check for common files: `dirb http://target.com`
- Review source code for comments/hidden paths

## Vulnerability Assessment
- SQL injection: `sqlmap -u "http://target.com?id=1"`
- XSS testing: Manual testing with payloads
- CSRF testing: Check for missing tokens

## Authentication Testing
- Default credentials
- Password strength
- Session management

## Authorization Testing
- IDOR (Insecure Direct Object References)
- Privilege escalation
- Access control bypass

## Tools
- Burp Suite
- OWASP ZAP
- Nikto
- Dirbuster
""",
            "wireless_security.md": """
# Wireless Security Testing

## Wireless Reconnaissance
1. Put interface in monitor mode: `airmon-ng start wlan0`
2. Scan for networks: `airodump-ng wlan0mon`
3. Capture handshake: `airodump-ng -c 6 --bssid BSSID -w capture wlan0mon`

## WEP Cracking
1. Capture IVs: `aireplay-ng -1 0 -a BSSID wlan0mon`
2. Fake auth: `aireplay-ng -1 6000 -o 1 -q 10 -a BSSID wlan0mon`
3. Crack: `aircrack-ng -z capture.cap`

## WPA Cracking
1. Deauth client: `aireplay-ng -0 5 -a BSSID -c CLIENT wlan0mon`
2. Crack with wordlist: `aircrack-ng -w wordlist.txt capture.cap`

## Wireless Tools
- Aircrack-ng suite
- Reaver (WPS)
- Fern WiFi Cracker
- Kismet
""",
            "social_engineering.md": """
# Social Engineering Techniques

## Phishing
- Email phishing
- Spear phishing
- Whaling
- Vishing (voice phishing)

## Pretexting
- Creating false scenarios
- Impersonation
- Authority exploitation

## Baiting
- USB drops
- Fake WiFi hotspots
- Malicious downloads

## Tools
- SET (Social-Engineer Toolkit)
- Gophish
- King Phisher

## Defense
- Security awareness training
- Email filtering
- Multi-factor authentication
- Incident reporting procedures
""",
            "incident_response.md": """
# Incident Response Process

## Preparation Phase
- Develop incident response plan
- Assemble response team
- Train personnel
- Prepare tools and resources

## Identification Phase
- Monitor for indicators
- Analyze alerts
- Determine incident scope
- Notify stakeholders

## Containment Phase
- Short-term containment
- Long-term containment
- Evidence preservation

## Eradication Phase
- Remove malware/artifacts
- Close vulnerabilities
- Patch systems

## Recovery Phase
- Restore systems
- Monitor for recurrence
- Document lessons learned

## Lessons Learned Phase
- Conduct debrief
- Update procedures
- Improve defenses

## Tools
- SIEM systems
- Forensic tools
- Log analysis
- Backup systems
""",
            "malware_analysis.md": """
# Malware Analysis Basics

## Static Analysis
- File hashing (MD5, SHA256)
- String analysis: `strings malware.exe`
- PE analysis: `pefile` or `pestudio`
- Signature scanning: VirusTotal

## Dynamic Analysis
- Sandbox execution
- Network monitoring
- Process monitoring
- Registry monitoring

## Behavioral Analysis
- API calls
- File system changes
- Network connections
- Persistence mechanisms

## Tools
- Wireshark (network)
- Process Monitor
- Regshot (registry)
- IDA Pro / Ghidra (reverse engineering)

## Safe Analysis
- Use virtual machines
- Network isolation
- Backup important data
- Follow containment procedures
""",
            "forensics.md": """
# Digital Forensics Guide

## File System Forensics
- Timeline analysis
- Deleted file recovery
- Metadata extraction
- Hash verification

## Memory Forensics
- Memory acquisition
- Process analysis
- Network artifact extraction
- Malware detection

## Network Forensics
- Packet capture analysis
- Log correlation
- Traffic reconstruction
- Anomaly detection

## Mobile Forensics
- Device acquisition
- Data extraction
- App analysis
- Cloud data recovery

## Tools
- Autopsy
- Volatility (memory)
- Wireshark
- FTK Imager

## Chain of Custody
- Document everything
- Preserve evidence integrity
- Maintain legal compliance
""",
            "cryptography.md": """
# Cryptography Basics

## Symmetric Encryption
- AES (Advanced Encryption Standard)
- DES (Data Encryption Standard)
- 3DES

## Asymmetric Encryption
- RSA
- ECC (Elliptic Curve Cryptography)
- Diffie-Hellman key exchange

## Hash Functions
- MD5 (deprecated)
- SHA-256
- SHA-3

## Digital Signatures
- RSA signatures
- ECDSA
- Ed25519

## Tools
- OpenSSL
- GPG
- Keytool

## Best Practices
- Use strong algorithms
- Proper key management
- Regular key rotation
- Secure random number generation
""",
            "security_programming.md": """
# Programming for Security

## Languages
- Python: Security scripting
- Bash: Automation
- Go: Fast tools
- C: Low-level security

## Security Libraries
- cryptography (Python)
- OpenSSL
- scapy (network packets)
- pwntools (exploitation)

## Secure Coding
- Input validation
- Buffer overflow prevention
- SQL injection prevention
- XSS prevention

## Tool Development
- Command-line tools
- Web interfaces
- API clients
- Automation scripts

## Best Practices
- Code review
- Testing
- Documentation
- Version control
"""
        }

        for filename, content in tutorials.items():
            filepath = self.tutorials_dir / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    f.write(content.strip())

    def show_tutorial(self, filename):
        filepath = self.tutorials_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                content = f.read()
            print(content)
        else:
            print(f"Tutorial {filename} not found")

    def create_tutorial(self):
        title = input("Tutorial title: ").strip()
        filename = title.lower().replace(' ', '_') + ".md"
        filepath = self.tutorials_dir / filename
        content = f"# {title}\n\n[Your tutorial content here]\n"
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Tutorial created: {filepath}")

    def list_tutorials(self):
        print("Available tutorials:")
        for file in self.tutorials_dir.glob("*.md"):
            print(f"- {file.name}")