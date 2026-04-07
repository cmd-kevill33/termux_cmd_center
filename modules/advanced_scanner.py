"""
Advanced Network Scanner Module for Termux Command Center
Comprehensive network scanning with automatic detection, error handling, and data collection.
"""

import json
import time
import threading
import os
from datetime import datetime
from pathlib import Path
import subprocess
import ipaddress
import re

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Advanced network scanning and reconnaissance"
        self.scan_results = {}
        self.is_scanning = False
        self.scan_log = self.cc.logs_dir / "network_scan.log"

    def run(self):
        print("\n=== Advanced Network Scanner ===")
        print("1. Auto-scan current network")
        print("2. Custom network scan")
        print("3. Continuous monitoring")
        print("4. View scan results")
        print("5. Export scan data")
        print("6. Network health check")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.auto_scan_network()
            elif choice == "2":
                self.custom_scan()
            elif choice == "3":
                self.continuous_monitoring()
            elif choice == "4":
                self.view_results()
            elif choice == "5":
                self.export_data()
            elif choice == "6":
                self.network_health_check()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def log_message(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)

        with open(self.scan_log, 'a') as f:
            f.write(log_entry + "\n")

    def get_current_network(self):
        """Automatically detect current network information"""
        try:
            # Get IP and subnet
            result = self.cc.run_command("ip route get 1")
            if result[0]:
                # Parse IP route output
                lines = result[0].split('\n')
                for line in lines:
                    if 'src' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == 'src':
                                ip = parts[i+1]
                            elif part.startswith('dev'):
                                interface = parts[i+1]
                        break

                # Get subnet mask
                result = self.cc.run_command(f"ip addr show {interface}")
                subnet_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', result[0])
                if subnet_match:
                    network = ipaddress.IPv4Network(f"{subnet_match.group(1)}/{subnet_match.group(2)}", strict=False)
                    return {
                        'ip': ip,
                        'interface': interface,
                        'network': str(network),
                        'gateway': self.get_gateway(),
                        'dns': self.get_dns_servers()
                    }
        except Exception as e:
            self.log_message(f"Error detecting network: {e}")

        return None

    def get_gateway(self):
        """Get default gateway"""
        try:
            result = self.cc.run_command("ip route show default")
            if result[0]:
                match = re.search(r'via (\d+\.\d+\.\d+\.\d+)', result[0])
                if match:
                    return match.group(1)
        except:
            pass
        return "Unknown"

    def get_dns_servers(self):
        """Get DNS servers"""
        try:
            result = self.cc.run_command("cat /etc/resolv.conf")
            dns_servers = []
            for line in result[0].split('\n'):
                if line.startswith('nameserver'):
                    dns_servers.append(line.split()[1])
            return dns_servers
        except:
            return ["8.8.8.8", "8.8.4.4"]  # Fallback

    def auto_scan_network(self):
        """Automatically scan the current network"""
        self.log_message("Starting automatic network scan...")

        network_info = self.get_current_network()
        if not network_info:
            self.log_message("Could not detect current network. Using fallback scan.")
            self.fallback_scan()
            return

        self.log_message(f"Detected network: {network_info['network']}")
        self.log_message(f"Local IP: {network_info['ip']}")
        self.log_message(f"Interface: {network_info['interface']}")
        self.log_message(f"Gateway: {network_info['gateway']}")

        # Start comprehensive scan
        scan_id = f"auto_scan_{int(time.time())}"
        self.scan_results[scan_id] = {
            'network_info': network_info,
            'start_time': datetime.now().isoformat(),
            'phases': {}
        }

        try:
            # Phase 1: Basic network mapping
            self.log_message("Phase 1: Network mapping...")
            self.phase_network_mapping(scan_id, network_info)

            # Phase 2: Host discovery
            self.log_message("Phase 2: Host discovery...")
            self.phase_host_discovery(scan_id, network_info)

            # Phase 3: Service enumeration
            self.log_message("Phase 3: Service enumeration...")
            self.phase_service_enum(scan_id, network_info)

            # Phase 4: Vulnerability assessment
            self.log_message("Phase 4: Vulnerability assessment...")
            self.phase_vuln_assessment(scan_id, network_info)

            # Phase 5: Data collection
            self.log_message("Phase 5: Additional data collection...")
            self.phase_data_collection(scan_id, network_info)

        except Exception as e:
            self.log_message(f"Scan error: {e}")
            self.fallback_scan()

        self.scan_results[scan_id]['end_time'] = datetime.now().isoformat()
        self.log_message(f"Scan completed. Results saved with ID: {scan_id}")

    def phase_network_mapping(self, scan_id, network_info):
        """Phase 1: Basic network mapping"""
        try:
            # Ping sweep
            network = network_info['network']
            result = self.cc.run_command(f"nmap -sn {network} -T4 --min-parallelism 100")
            self.scan_results[scan_id]['phases']['network_mapping'] = {
                'ping_sweep': result[0],
                'errors': result[1]
            }

            # ARP scan for faster local network discovery
            result = self.cc.run_command(f"arp-scan --interface={network_info['interface']} --localnet")
            self.scan_results[scan_id]['phases']['network_mapping']['arp_scan'] = result[0]

        except Exception as e:
            self.log_message(f"Network mapping error: {e}")
            self.scan_results[scan_id]['phases']['network_mapping'] = {'error': str(e)}

    def phase_host_discovery(self, scan_id, network_info):
        """Phase 2: Detailed host discovery"""
        try:
            network = network_info['network']
            # Comprehensive host discovery
            result = self.cc.run_command(f"nmap -PS21,22,23,25,53,80,110,139,443,445,993,995 {network} -T4")
            self.scan_results[scan_id]['phases']['host_discovery'] = {
                'tcp_ping': result[0],
                'errors': result[1]
            }

            # UDP host discovery
            result = self.cc.run_command(f"nmap -PU53,67,68,69,123,135,137,138,161,162,500,514,520,631,1434 {network} -T4")
            self.scan_results[scan_id]['phases']['host_discovery']['udp_ping'] = result[0]

        except Exception as e:
            self.log_message(f"Host discovery error: {e}")
            self.scan_results[scan_id]['phases']['host_discovery'] = {'error': str(e)}

    def phase_service_enum(self, scan_id, network_info):
        """Phase 3: Service enumeration"""
        try:
            network = network_info['network']
            # Service version detection
            result = self.cc.run_command(f"nmap -sV -sC --version-intensity 5 {network} -T4 --max-retries 2")
            self.scan_results[scan_id]['phases']['service_enum'] = {
                'service_versions': result[0],
                'errors': result[1]
            }

            # OS detection
            result = self.cc.run_command(f"nmap -O --osscan-guess {network} -T4")
            self.scan_results[scan_id]['phases']['service_enum']['os_detection'] = result[0]

        except Exception as e:
            self.log_message(f"Service enumeration error: {e}")
            self.scan_results[scan_id]['phases']['service_enum'] = {'error': str(e)}

    def phase_vuln_assessment(self, scan_id, network_info):
        """Phase 4: Vulnerability assessment"""
        try:
            network = network_info['network']
            # Basic vulnerability scanning
            result = self.cc.run_command(f"nmap --script vuln {network} -T3 --script-timeout 30s")
            self.scan_results[scan_id]['phases']['vuln_assessment'] = {
                'nmap_vuln': result[0],
                'errors': result[1]
            }

            # Additional vulnerability checks
            result = self.cc.run_command(f"nikto -h {network} -Tuning 1234567890abc -timeout 10")
            self.scan_results[scan_id]['phases']['vuln_assessment']['nikto_scan'] = result[0]

        except Exception as e:
            self.log_message(f"Vulnerability assessment error: {e}")
            self.scan_results[scan_id]['phases']['vuln_assessment'] = {'error': str(e)}

    def phase_data_collection(self, scan_id, network_info):
        """Phase 5: Additional data collection"""
        try:
            collection_data = {}

            # Wireless network info (if available)
            result = self.cc.run_command("iwconfig 2>/dev/null | head -10")
            collection_data['wireless'] = result[0]

            # Routing table
            result = self.cc.run_command("ip route show")
            collection_data['routing_table'] = result[0]

            # ARP table
            result = self.cc.run_command("arp -a")
            collection_data['arp_table'] = result[0]

            # Network connections
            result = self.cc.run_command("netstat -tuln")
            collection_data['netstat'] = result[0]

            # Firewall rules (if available)
            result = self.cc.run_command("iptables -L -n")
            collection_data['firewall'] = result[0]

            self.scan_results[scan_id]['phases']['data_collection'] = collection_data

        except Exception as e:
            self.log_message(f"Data collection error: {e}")
            self.scan_results[scan_id]['phases']['data_collection'] = {'error': str(e)}

    def fallback_scan(self):
        """Fallback scanning when automatic detection fails"""
        self.log_message("Using fallback scanning methods...")

        try:
            # Try common network ranges
            common_ranges = ["192.168.1.0/24", "192.168.0.0/24", "10.0.0.0/24", "172.16.0.0/24"]

            for network in common_ranges:
                self.log_message(f"Trying network: {network}")
                result = self.cc.run_command(f"nmap -sn {network} -T4 --host-timeout 5s")
                if "Host is up" in result[0]:
                    self.log_message(f"Found active network: {network}")
                    # Perform basic scan on found network
                    result = self.cc.run_command(f"nmap -F {network} -T4")
                    scan_id = f"fallback_scan_{network.replace('/', '_')}_{int(time.time())}"
                    self.scan_results[scan_id] = {
                        'network': network,
                        'scan_type': 'fallback',
                        'results': result[0],
                        'timestamp': datetime.now().isoformat()
                    }
                    break

        except Exception as e:
            self.log_message(f"Fallback scan failed: {e}")

    def custom_scan(self):
        """Custom network scanning"""
        network = input("Enter network (e.g., 192.168.1.0/24): ").strip()
        scan_type = input("Scan type (basic/full/vuln/custom): ").strip().lower()

        if scan_type == "basic":
            cmd = f"nmap -F {network} -T4"
        elif scan_type == "full":
            cmd = f"nmap -A -T4 {network}"
        elif scan_type == "vuln":
            cmd = f"nmap --script vuln {network} -T3"
        else:
            options = input("Enter custom nmap options: ").strip()
            cmd = f"nmap {options} {network}"

        self.log_message(f"Running custom scan: {cmd}")
        result = self.cc.run_command(cmd)
        print(result[0])
        if result[1]:
            print("Errors:", result[1])

    def continuous_monitoring(self):
        """Continuous network monitoring"""
        if self.is_scanning:
            print("Monitoring already running. Stop first.")
            return

        duration = input("Monitoring duration in minutes (0 for indefinite): ").strip()
        try:
            duration = int(duration) * 60 if duration else 0
        except:
            duration = 300  # 5 minutes default

        self.is_scanning = True
        self.log_message(f"Starting continuous monitoring for {duration} seconds")

        def monitor():
            start_time = time.time()
            while self.is_scanning and (duration == 0 or time.time() - start_time < duration):
                try:
                    # Quick network health check
                    result = self.cc.run_command("ping -c 1 8.8.8.8")
                    status = "UP" if result[2] == 0 else "DOWN"
                    self.log_message(f"Internet connectivity: {status}")

                    # Check local network
                    network_info = self.get_current_network()
                    if network_info:
                        result = self.cc.run_command(f"nmap -sn {network_info['network']} -T5 --host-timeout 1s")
                        host_count = result[0].count("Host is up")
                        self.log_message(f"Active hosts on network: {host_count}")

                    time.sleep(60)  # Check every minute

                except Exception as e:
                    self.log_message(f"Monitoring error: {e}")
                    time.sleep(30)

            self.is_scanning = False
            self.log_message("Continuous monitoring stopped")

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        print("Monitoring started in background. Check logs for updates.")

    def view_results(self):
        """View scan results"""
        if not self.scan_results:
            print("No scan results available.")
            return

        print("Available scans:")
        for i, scan_id in enumerate(self.scan_results.keys(), 1):
            scan = self.scan_results[scan_id]
            network = scan.get('network_info', {}).get('network', scan.get('network', 'Unknown'))
            timestamp = scan.get('start_time', scan.get('timestamp', 'Unknown'))
            print(f"{i}. {scan_id} - {network} ({timestamp})")

        choice = input("Enter scan number to view: ").strip()
        try:
            scan_id = list(self.scan_results.keys())[int(choice)-1]
            self.display_scan_details(scan_id)
        except:
            print("Invalid choice.")

    def display_scan_details(self, scan_id):
        """Display detailed scan results"""
        scan = self.scan_results[scan_id]
        print(f"\n=== Scan Details: {scan_id} ===")

        if 'network_info' in scan:
            print("Network Information:")
            for key, value in scan['network_info'].items():
                print(f"  {key}: {value}")

        if 'phases' in scan:
            for phase_name, phase_data in scan['phases'].items():
                print(f"\n{phase_name.upper()}:")
                if isinstance(phase_data, dict):
                    for key, value in phase_data.items():
                        if isinstance(value, str) and len(value) > 200:
                            print(f"  {key}: [Output too long, check logs]")
                        else:
                            print(f"  {key}: {value}")
                else:
                    print(f"  {phase_data}")

    def export_data(self):
        """Export scan data"""
        if not self.scan_results:
            print("No data to export.")
            return

        filename = f"network_scan_export_{int(time.time())}.json"
        filepath = self.cc.data_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.scan_results, f, indent=2)

        print(f"Data exported to: {filepath}")

    def network_health_check(self):
        """Network health check"""
        print("=== Network Health Check ===")

        checks = [
            ("Internet Connectivity", "ping -c 3 8.8.8.8"),
            ("DNS Resolution", "nslookup google.com"),
            ("Local Network", "ping -c 3 192.168.1.1"),
            ("Gateway Reachability", "ping -c 3 $(ip route show default | awk '{print $3}')"),
        ]

        for check_name, command in checks:
            print(f"\n{check_name}:")
            try:
                result = self.cc.run_command(command)
                if result[2] == 0:
                    print("✓ PASS")
                else:
                    print("✗ FAIL")
                    if result[1]:
                        print(f"Error: {result[1]}")
            except Exception as e:
                print(f"✗ ERROR: {e}")