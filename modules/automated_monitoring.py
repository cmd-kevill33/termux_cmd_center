"""
Automated Network Monitoring Module for Termux Command Center
Continuous network monitoring with intelligent error handling and data collection.
"""

import time
import threading
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import ipaddress
import re

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Automated network monitoring and data collection"
        self.is_monitoring = False
        self.monitor_thread = None
        self.monitor_config = {
            'interval': 60,  # seconds
            'duration': 0,   # 0 = indefinite
            'network_range': None,
            'alerts_enabled': True,
            'data_retention_days': 7
        }
        self.monitor_data = []
        self.alerts = []
        self.load_config()

    def load_config(self):
        """Load monitoring configuration"""
        config_file = self.cc.config_dir / "network_monitor.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.monitor_config.update(json.load(f))

    def save_config(self):
        """Save monitoring configuration"""
        config_file = self.cc.config_dir / "network_monitor.json"
        with open(config_file, 'w') as f:
            json.dump(self.monitor_config, f, indent=2)

    def run(self):
        print("\n=== Automated Network Monitoring ===")
        print("1. Start monitoring")
        print("2. Stop monitoring")
        print("3. Configure monitoring")
        print("4. View monitoring data")
        print("5. View alerts")
        print("6. Generate report")
        print("7. Quick network health check")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.start_monitoring()
            elif choice == "2":
                self.stop_monitoring()
            elif choice == "3":
                self.configure_monitoring()
            elif choice == "4":
                self.view_monitoring_data()
            elif choice == "5":
                self.view_alerts()
            elif choice == "6":
                self.generate_report()
            elif choice == "7":
                self.quick_health_check()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def start_monitoring(self):
        """Start automated monitoring"""
        if self.is_monitoring:
            print("Monitoring is already running.")
            return

        print("Starting automated network monitoring...")

        # Auto-detect network if not configured
        if not self.monitor_config['network_range']:
            network_info = self.get_current_network()
            if network_info:
                self.monitor_config['network_range'] = network_info['network']
                self.save_config()
                print(f"Auto-detected network: {network_info['network']}")
            else:
                print("Could not detect network. Please configure manually.")
                return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()

        print("✓ Monitoring started in background")
        print(f"Interval: {self.monitor_config['interval']} seconds")
        if self.monitor_config['duration'] > 0:
            print(f"Duration: {self.monitor_config['duration']} seconds")
        else:
            print("Duration: Indefinite (until stopped)")

    def stop_monitoring(self):
        """Stop automated monitoring"""
        if not self.is_monitoring:
            print("Monitoring is not running.")
            return

        print("Stopping monitoring...")
        self.is_monitoring = False

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        print("✓ Monitoring stopped")

    def configure_monitoring(self):
        """Configure monitoring settings"""
        print("Current configuration:")
        for key, value in self.monitor_config.items():
            print(f"  {key}: {value}")

        print("\nEnter new values (press Enter to keep current):")

        for key in self.monitor_config:
            current = self.monitor_config[key]
            if isinstance(current, bool):
                value = input(f"{key} ({current}): ").strip().lower()
                if value in ['true', '1', 'yes', 'y']:
                    self.monitor_config[key] = True
                elif value in ['false', '0', 'no', 'n']:
                    self.monitor_config[key] = False
            else:
                value = input(f"{key} ({current}): ").strip()
                if value:
                    try:
                        if isinstance(current, int):
                            self.monitor_config[key] = int(value)
                        else:
                            self.monitor_config[key] = value
                    except:
                        print(f"Invalid value for {key}")

        self.save_config()
        print("Configuration saved.")

    def monitoring_loop(self):
        """Main monitoring loop"""
        start_time = time.time()
        last_cleanup = start_time

        while self.is_monitoring:
            try:
                current_time = time.time()

                # Perform monitoring checks
                self.perform_monitoring_checks()

                # Cleanup old data (daily)
                if current_time - last_cleanup > 86400:  # 24 hours
                    self.cleanup_old_data()
                    last_cleanup = current_time

                # Check duration limit
                if self.monitor_config['duration'] > 0 and current_time - start_time > self.monitor_config['duration']:
                    self.log_message("Monitoring duration reached, stopping...")
                    self.is_monitoring = False
                    break

                # Wait for next interval
                time.sleep(self.monitor_config['interval'])

            except Exception as e:
                self.log_error(f"Monitoring loop error: {e}")
                time.sleep(30)  # Wait before retrying

    def perform_monitoring_checks(self):
        """Perform all monitoring checks"""
        timestamp = datetime.now().isoformat()
        checks = {}

        try:
            # Network connectivity
            checks['internet_connectivity'] = self.check_internet_connectivity()

            # Local network scan
            checks['network_scan'] = self.perform_quick_network_scan()

            # Service availability
            checks['service_checks'] = self.check_critical_services()

            # System resources
            checks['system_resources'] = self.check_system_resources()

            # Wireless status (if applicable)
            checks['wireless_status'] = self.check_wireless_status()

            # Generate alerts
            self.generate_alerts(checks)

            # Store data
            data_point = {
                'timestamp': timestamp,
                'checks': checks
            }
            self.monitor_data.append(data_point)

            # Keep only recent data
            cutoff_time = datetime.now() - timedelta(days=self.monitor_config['data_retention_days'])
            self.monitor_data = [
                dp for dp in self.monitor_data
                if datetime.fromisoformat(dp['timestamp']) > cutoff_time
            ]

            self.log_message(f"Monitoring check completed at {timestamp}")

        except Exception as e:
            self.log_error(f"Error during monitoring checks: {e}")

    def check_internet_connectivity(self):
        """Check internet connectivity"""
        try:
            result = self.cc.run_command("ping -c 3 -W 5 8.8.8.8")
            return {
                'status': 'up' if result[2] == 0 else 'down',
                'latency': self.extract_ping_time(result[0]) if result[2] == 0 else None
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def perform_quick_network_scan(self):
        """Perform quick network scan"""
        try:
            network = self.monitor_config['network_range']
            if not network:
                return {'status': 'no_network_configured'}

            # Quick ping sweep
            result = self.cc.run_command(f"nmap -sn -T5 --host-timeout=2s {network}")
            hosts_up = result[0].count("Host is up")

            return {
                'network': network,
                'hosts_up': hosts_up,
                'scan_time': self.extract_nmap_time(result[0])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def check_critical_services(self):
        """Check critical services"""
        services = {
            'ssh': ('22', 'tcp'),
            'http': ('80', 'tcp'),
            'https': ('443', 'tcp'),
            'dns': ('53', 'udp')
        }

        results = {}
        for service_name, (port, protocol) in services.items():
            try:
                if protocol == 'tcp':
                    result = self.cc.run_command(f"timeout 3 bash -c '</dev/tcp/localhost/{port}' && echo 'open' || echo 'closed'")
                else:
                    result = self.cc.run_command(f"timeout 3 nc -uz localhost {port} && echo 'open' || echo 'closed'")

                results[service_name] = 'open' in result[0].lower()
            except:
                results[service_name] = False

        return results

    def check_system_resources(self):
        """Check system resources"""
        try:
            # CPU usage
            result = self.cc.run_command("top -n 1 | grep 'CPU:' | awk '{print $2}'")
            cpu_usage = result[0].strip().rstrip('%') if result[0] else 'unknown'

            # Memory usage
            result = self.cc.run_command("free | grep Mem | awk '{printf \"%.0f\", $3/$2 * 100.0}'")
            mem_usage = result[0].strip() if result[0] else 'unknown'

            # Disk usage
            result = self.cc.run_command("df / | tail -1 | awk '{print $5}'")
            disk_usage = result[0].strip().rstrip('%') if result[0] else 'unknown'

            return {
                'cpu_usage': cpu_usage,
                'memory_usage': mem_usage,
                'disk_usage': disk_usage
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def check_wireless_status(self):
        """Check wireless network status"""
        try:
            result = self.cc.run_command("iwconfig 2>/dev/null | head -5")
            if result[0] and 'wlan' in result[0]:
                return {'wireless_available': True, 'details': result[0][:200]}
            else:
                return {'wireless_available': False}
        except:
            return {'wireless_available': False}

    def generate_alerts(self, checks):
        """Generate alerts based on monitoring data"""
        if not self.monitor_config['alerts_enabled']:
            return

        alerts = []

        # Internet connectivity alerts
        if checks.get('internet_connectivity', {}).get('status') == 'down':
            alerts.append({
                'type': 'connectivity',
                'severity': 'high',
                'message': 'Internet connectivity is down'
            })

        # High resource usage alerts
        resources = checks.get('system_resources', {})
        try:
            if resources.get('cpu_usage', 0) > 90:
                alerts.append({
                    'type': 'resource',
                    'severity': 'medium',
                    'message': f'High CPU usage: {resources["cpu_usage"]}%'
                })
            if resources.get('memory_usage', 0) > 90:
                alerts.append({
                    'type': 'resource',
                    'severity': 'high',
                    'message': f'High memory usage: {resources["memory_usage"]}%'
                })
        except:
            pass

        # Network changes
        if len(self.monitor_data) > 1:
            prev_scan = self.monitor_data[-2]['checks'].get('network_scan', {})
            curr_scan = checks.get('network_scan', {})

            prev_hosts = prev_scan.get('hosts_up', 0)
            curr_hosts = curr_scan.get('hosts_up', 0)

            if abs(curr_hosts - prev_hosts) > 2:  # Significant change
                alerts.append({
                    'type': 'network_change',
                    'severity': 'medium',
                    'message': f'Network hosts changed: {prev_hosts} -> {curr_hosts}'
                })

        if alerts:
            self.alerts.extend(alerts)
            # Keep only recent alerts
            cutoff_time = datetime.now() - timedelta(days=1)
            self.alerts = [
                alert for alert in self.alerts
                if 'timestamp' not in alert or datetime.fromisoformat(alert.get('timestamp', datetime.now().isoformat())) > cutoff_time
            ]

            for alert in alerts:
                self.log_message(f"ALERT: {alert['message']}")

    def extract_ping_time(self, output):
        """Extract ping time from output"""
        match = re.search(r'time=(\d+\.?\d*)', output)
        return float(match.group(1)) if match else None

    def extract_nmap_time(self, output):
        """Extract scan time from nmap output"""
        match = re.search(r'scanned in ([\d.]+)', output)
        return float(match.group(1)) if match else None

    def get_current_network(self):
        """Get current network information"""
        try:
            result = self.cc.run_command("ip route get 1")
            if result[0]:
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

                result = self.cc.run_command(f"ip addr show {interface}")
                subnet_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', result[0])
                if subnet_match:
                    network = ipaddress.IPv4Network(f"{subnet_match.group(1)}/{subnet_match.group(2)}", strict=False)
                    return {
                        'ip': ip,
                        'interface': interface,
                        'network': str(network)
                    }
        except:
            pass
        return None

    def cleanup_old_data(self):
        """Clean up old monitoring data"""
        cutoff_time = datetime.now() - timedelta(days=self.monitor_config['data_retention_days'])
        initial_count = len(self.monitor_data)
        self.monitor_data = [
            dp for dp in self.monitor_data
            if datetime.fromisoformat(dp['timestamp']) > cutoff_time
        ]
        removed_count = initial_count - len(self.monitor_data)
        if removed_count > 0:
            self.log_message(f"Cleaned up {removed_count} old data points")

    def log_message(self, message):
        """Log monitoring message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] MONITOR: {message}"
        print(log_entry)

        log_file = self.cc.logs_dir / "network_monitor.log"
        with open(log_file, 'a') as f:
            f.write(log_entry + "\n")

    def log_error(self, message):
        """Log monitoring error"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] MONITOR ERROR: {message}"
        print(log_entry)

        log_file = self.cc.logs_dir / "network_monitor_errors.log"
        with open(log_file, 'a') as f:
            f.write(log_entry + "\n")

    def view_monitoring_data(self):
        """View monitoring data"""
        if not self.monitor_data:
            print("No monitoring data available.")
            return

        print(f"Total data points: {len(self.monitor_data)}")
        print("Recent data points:")

        # Show last 10 data points
        for dp in self.monitor_data[-10:]:
            timestamp = dp['timestamp']
            checks = dp['checks']

            internet = checks.get('internet_connectivity', {}).get('status', 'unknown')
            hosts = checks.get('network_scan', {}).get('hosts_up', 'unknown')

            print(f"  {timestamp}: Internet={internet}, Hosts={hosts}")

    def view_alerts(self):
        """View monitoring alerts"""
        if not self.alerts:
            print("No alerts generated.")
            return

        print(f"Total alerts: {len(self.alerts)}")
        print("Recent alerts:")

        for alert in self.alerts[-10:]:
            severity = alert.get('severity', 'unknown')
            message = alert.get('message', 'No message')
            print(f"  [{severity.upper()}] {message}")

    def generate_report(self):
        """Generate monitoring report"""
        if not self.monitor_data:
            print("No data available for report generation.")
            return

        report = {
            'generated_at': datetime.now().isoformat(),
            'monitoring_period': {
                'start': self.monitor_data[0]['timestamp'] if self.monitor_data else None,
                'end': self.monitor_data[-1]['timestamp'] if self.monitor_data else None,
                'total_points': len(self.monitor_data)
            },
            'summary': self.generate_summary(),
            'alerts': self.alerts[-50:],  # Last 50 alerts
            'recommendations': self.generate_recommendations()
        }

        report_file = self.cc.data_dir / f"monitoring_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Report generated: {report_file}")

    def generate_summary(self):
        """Generate monitoring summary"""
        if not self.monitor_data:
            return {}

        summary = {
            'total_checks': len(self.monitor_data),
            'connectivity_issues': 0,
            'resource_issues': 0,
            'network_changes': 0
        }

        for dp in self.monitor_data:
            checks = dp['checks']

            # Connectivity issues
            if checks.get('internet_connectivity', {}).get('status') == 'down':
                summary['connectivity_issues'] += 1

            # Resource issues
            resources = checks.get('system_resources', {})
            try:
                if float(resources.get('cpu_usage', 0)) > 80 or float(resources.get('memory_usage', 0)) > 80:
                    summary['resource_issues'] += 1
            except:
                pass

        return summary

    def generate_recommendations(self):
        """Generate monitoring recommendations"""
        recommendations = []

        if not self.monitor_data:
            return recommendations

        summary = self.generate_summary()

        if summary.get('connectivity_issues', 0) > len(self.monitor_data) * 0.1:
            recommendations.append("Consider improving internet connectivity or switching providers")

        if summary.get('resource_issues', 0) > len(self.monitor_data) * 0.05:
            recommendations.append("Monitor system resources more closely - consider optimization")

        if len(self.alerts) > 10:
            recommendations.append("Review alert thresholds and monitoring configuration")

        return recommendations

    def quick_health_check(self):
        """Perform quick network health check"""
        print("=== Quick Network Health Check ===")

        checks = [
            ("Internet Connectivity", self.check_internet_connectivity),
            ("Local Network", lambda: self.perform_quick_network_scan()),
            ("Critical Services", self.check_critical_services),
            ("System Resources", self.check_system_resources)
        ]

        for check_name, check_func in checks:
            print(f"\n{check_name}:")
            try:
                result = check_func()
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {result}")
            except Exception as e:
                print(f"  Error: {e}")

        print("\nHealth check complete.")