"""
Dashboard Module for Termux Command Center
Real-time monitoring dashboard with visualizations and alerts.
"""

import time
import threading
import json
import re
import ipaddress
from datetime import datetime, timedelta
from pathlib import Path
import curses
import curses.textpad
import locale

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Real-time dashboard with monitoring and visualizations"
        self.dashboard_data = {}
        self.alerts = []
        self.is_running = False
        self.update_interval = 5  # seconds
        self.dashboard_file = self.cc.data_dir / "dashboard_data.json"

    def run(self):
        print("\n=== Real-time Dashboard ===")
        print("1. Launch interactive dashboard")
        print("2. View system overview")
        print("3. Monitor network status")
        print("4. View recent alerts")
        print("5. Generate dashboard report")
        print("6. Configure dashboard")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.launch_interactive_dashboard()
            elif choice == "2":
                self.show_system_overview()
            elif choice == "3":
                self.monitor_network_status()
            elif choice == "4":
                self.view_recent_alerts()
            elif choice == "5":
                self.generate_dashboard_report()
            elif choice == "6":
                self.configure_dashboard()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def launch_interactive_dashboard(self):
        """Launch curses-based interactive dashboard"""
        try:
            locale.setlocale(locale.LC_ALL, '')
            curses.wrapper(self._dashboard_main)
        except Exception as e:
            print(f"Dashboard error: {e}")
            print("Falling back to text-based dashboard...")
            self.show_text_dashboard()

    def _dashboard_main(self, stdscr):
        """Main dashboard function for curses"""
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(1000)  # 1 second timeout

        height, width = stdscr.getmaxyx()

        while self.is_running:
            stdscr.clear()

            # Draw borders
            stdscr.border()

            # Title
            title = "Termux Command Center - Live Dashboard"
            stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

            # System info section
            self._draw_system_info(stdscr, 3, 2)

            # Network status
            self._draw_network_status(stdscr, 3, width // 2 + 1)

            # Recent alerts
            self._draw_alerts(stdscr, 10, 2)

            # Active scans/modules
            self._draw_active_operations(stdscr, 10, width // 2 + 1)

            # Status bar
            status = f"Last update: {datetime.now().strftime('%H:%M:%S')} | Press 'q' to quit"
            stdscr.addstr(height - 1, 0, status, curses.A_REVERSE)

            stdscr.refresh()

            # Check for quit key
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break

            time.sleep(self.update_interval)

    def _draw_system_info(self, stdscr, y, x):
        """Draw system information section"""
        stdscr.addstr(y, x, "System Status", curses.A_BOLD)
        stdscr.addstr(y + 1, x, "─" * 20)

        try:
            # CPU, Memory, Disk
            result = self.cc.run_command("top -n 1 | head -5")
            lines = result[0].split('\n')[:5]
            for i, line in enumerate(lines):
                if i < 4:  # Limit to 4 lines
                    stdscr.addstr(y + 2 + i, x, line[:30])
        except:
            stdscr.addstr(y + 2, x, "System info unavailable")

    def _draw_network_status(self, stdscr, y, x):
        """Draw network status section"""
        stdscr.addstr(y, x, "Network Status", curses.A_BOLD)
        stdscr.addstr(y + 1, x, "─" * 20)

        try:
            # Internet connectivity
            result = self.cc.run_command("ping -c 1 8.8.8.8")
            status = "✓ Online" if result[2] == 0 else "✗ Offline"
            stdscr.addstr(y + 2, x, f"Internet: {status}")

            # Local network
            network_info = self.get_current_network()
            if network_info:
                stdscr.addstr(y + 3, x, f"Network: {network_info.get('network', 'Unknown')}")
                stdscr.addstr(y + 4, x, f"IP: {network_info.get('ip', 'Unknown')}")
        except:
            stdscr.addstr(y + 2, x, "Network info unavailable")

    def _draw_alerts(self, stdscr, y, x):
        """Draw recent alerts section"""
        stdscr.addstr(y, x, "Recent Alerts", curses.A_BOLD)
        stdscr.addstr(y + 1, x, "─" * 20)

        recent_alerts = self.alerts[-5:]  # Last 5 alerts
        for i, alert in enumerate(recent_alerts):
            if i < 5:
                alert_text = f"{alert.get('type', 'Unknown')}: {alert.get('message', '')[:25]}"
                stdscr.addstr(y + 2 + i, x, alert_text)

    def _draw_active_operations(self, stdscr, y, x):
        """Draw active operations section"""
        stdscr.addstr(y, x, "Active Operations", curses.A_BOLD)
        stdscr.addstr(y + 1, x, "─" * 20)

        # Check for running processes
        try:
            result = self.cc.run_command("ps aux | grep -E '(nmap|python|msfconsole)' | grep -v grep | wc -l")
            active_scans = result[0].strip()
            stdscr.addstr(y + 2, x, f"Active scans: {active_scans}")

            # Check monitoring status
            monitoring_active = "Yes" if hasattr(self.cc, 'modules') and 'automated_monitoring' in self.cc.modules and self.cc.modules['automated_monitoring'].is_monitoring else "No"
            stdscr.addstr(y + 3, x, f"Monitoring: {monitoring_active}")
        except:
            stdscr.addstr(y + 2, x, "Status unavailable")

    def show_text_dashboard(self):
        """Fallback text-based dashboard"""
        print("=== Text-based Dashboard ===")

        while True:
            print("\n" + "="*50)
            print(f"Dashboard Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50)

            # System status
            print("\n📊 System Status:")
            try:
                result = self.cc.run_command("df -h / | tail -1")
                print(f"Disk: {result[0].strip()}")
                result = self.cc.run_command("free -h | grep Mem")
                print(f"Memory: {result[0].strip()}")
            except:
                print("System info unavailable")

            # Network status
            print("\n🌐 Network Status:")
            try:
                result = self.cc.run_command("ping -c 1 8.8.8.8")
                status = "✓ Online" if result[2] == 0 else "✗ Offline"
                print(f"Internet: {status}")
            except:
                print("Network check failed")

            # Recent alerts
            print("\n🚨 Recent Alerts:")
            recent_alerts = self.alerts[-3:]
            for alert in recent_alerts:
                print(f"• {alert.get('type', 'Unknown')}: {alert.get('message', '')}")

            # Active operations
            print("\n⚙️ Active Operations:")
            print("Monitoring scans and background processes would be shown here")

            print("\nPress Ctrl+C to exit...")
            time.sleep(self.update_interval)

    def show_system_overview(self):
        """Show detailed system overview"""
        print("=== System Overview ===")

        checks = {
            "CPU Usage": "top -n 1 | grep 'CPU:' | awk '{print $2}'",
            "Memory Usage": "free | grep Mem | awk '{printf \"%.0f%%\", $3/$2 * 100.0}'",
            "Disk Usage": "df / | tail -1 | awk '{print $5}'",
            "Load Average": "uptime | awk -F'load average:' '{print $2}'",
            "Running Processes": "ps aux | wc -l",
            "Network Interfaces": "ip link show | grep -c UP",
            "Open Ports": "netstat -tuln | grep LISTEN | wc -l"
        }

        for check_name, command in checks.items():
            try:
                result = self.cc.run_command(command)
                value = result[0].strip()
                print(f"{check_name}: {value}")
            except Exception as e:
                print(f"{check_name}: Error - {e}")

    def monitor_network_status(self):
        """Monitor network status in real-time"""
        print("=== Network Status Monitor ===")
        print("Press Ctrl+C to stop")

        try:
            while True:
                print(f"\n--- {datetime.now().strftime('%H:%M:%S')} ---")

                # Internet connectivity
                result = self.cc.run_command("ping -c 1 8.8.8.8")
                status = "✓ Connected" if result[2] == 0 else "✗ Disconnected"
                print(f"Internet: {status}")

                # Local network
                network_info = self.get_current_network()
                if network_info:
                    print(f"Local IP: {network_info.get('ip', 'Unknown')}")
                    print(f"Network: {network_info.get('network', 'Unknown')}")

                    # Quick host count
                    result = self.cc.run_command(f"nmap -sn {network_info['network']} -T5 --host-timeout=1s")
                    host_count = result[0].count("Host is up")
                    print(f"Active hosts: {host_count}")
                else:
                    print("Local network: Unable to detect")

                time.sleep(10)  # Update every 10 seconds

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

    def view_recent_alerts(self):
        """View recent alerts"""
        print("=== Recent Alerts ===")

        if not self.alerts:
            print("No alerts generated yet.")
            return

        for i, alert in enumerate(self.alerts[-10:], 1):  # Show last 10
            timestamp = alert.get('timestamp', 'Unknown')
            alert_type = alert.get('type', 'Unknown')
            severity = alert.get('severity', 'Unknown')
            message = alert.get('message', 'No message')

            print(f"{i}. [{timestamp}] {severity.upper()} - {alert_type}: {message}")

    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        print("Generating dashboard report...")

        report = {
            'generated_at': datetime.now().isoformat(),
            'system_overview': self.get_system_overview_data(),
            'network_status': self.get_network_status_data(),
            'alerts_summary': self.get_alerts_summary(),
            'active_operations': self.get_active_operations_data(),
            'recommendations': self.generate_recommendations()
        }

        report_file = self.cc.data_dir / f"dashboard_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Report saved to: {report_file}")

        # Also generate a human-readable summary
        summary_file = self.cc.data_dir / f"dashboard_summary_{int(time.time())}.txt"
        with open(summary_file, 'w') as f:
            f.write("Termux Command Center - Dashboard Summary\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("System Overview:\n")
            for key, value in report['system_overview'].items():
                f.write(f"  {key}: {value}\n")

            f.write("\nNetwork Status:\n")
            for key, value in report['network_status'].items():
                f.write(f"  {key}: {value}\n")

            f.write(f"\nAlerts Summary: {report['alerts_summary']['total_alerts']} total alerts\n")
            f.write(f"  High: {report['alerts_summary']['high_severity']}\n")
            f.write(f"  Medium: {report['alerts_summary']['medium_severity']}\n")
            f.write(f"  Low: {report['alerts_summary']['low_severity']}\n")

            f.write("\nRecommendations:\n")
            for rec in report['recommendations']:
                f.write(f"  • {rec}\n")

        print(f"Summary saved to: {summary_file}")

    def configure_dashboard(self):
        """Configure dashboard settings"""
        print("Current dashboard configuration:")
        print(f"Update interval: {self.update_interval} seconds")

        new_interval = input(f"New update interval ({self.update_interval}): ").strip()
        if new_interval and new_interval.isdigit():
            self.update_interval = int(new_interval)
            print("Configuration updated.")
        else:
            print("Keeping current configuration.")

    def get_system_overview_data(self):
        """Get comprehensive system overview data"""
        data = {}
        try:
            commands = {
                'cpu_usage': "top -n 1 | grep 'CPU:' | awk '{print $2}'",
                'memory_total': "free -h | grep Mem | awk '{print $2}'",
                'memory_used': "free -h | grep Mem | awk '{print $3}'",
                'disk_total': "df -h / | tail -1 | awk '{print $2}'",
                'disk_used': "df -h / | tail -1 | awk '{print $3}'",
                'disk_available': "df -h / | tail -1 | awk '{print $4}'",
                'load_average': "uptime | awk -F'load average:' '{print $2}'",
                'uptime': "uptime -p"
            }

            for key, command in commands.items():
                result = self.cc.run_command(command)
                data[key] = result[0].strip() if result[0] else "Unknown"

        except Exception as e:
            data['error'] = str(e)

        return data

    def get_network_status_data(self):
        """Get comprehensive network status data"""
        data = {}
        try:
            # Internet connectivity
            result = self.cc.run_command("ping -c 3 8.8.8.8")
            data['internet_connectivity'] = 'up' if result[2] == 0 else 'down'

            # Network interfaces
            result = self.cc.run_command("ip addr show | grep 'inet ' | wc -l")
            data['active_interfaces'] = result[0].strip()

            # DNS resolution
            result = self.cc.run_command("nslookup google.com 2>/dev/null | grep -c 'Address:'")
            data['dns_working'] = 'yes' if int(result[0].strip()) > 0 else 'no'

            # Current network info
            network_info = self.get_current_network()
            if network_info:
                data.update(network_info)

        except Exception as e:
            data['error'] = str(e)

        return data

    def get_alerts_summary(self):
        """Get alerts summary"""
        summary = {
            'total_alerts': len(self.alerts),
            'high_severity': len([a for a in self.alerts if a.get('severity') == 'high']),
            'medium_severity': len([a for a in self.alerts if a.get('severity') == 'medium']),
            'low_severity': len([a for a in self.alerts if a.get('severity') == 'low']),
            'recent_alerts': self.alerts[-5:] if self.alerts else []
        }
        return summary

    def get_active_operations_data(self):
        """Get data about active operations"""
        data = {}
        try:
            # Check for running security tools
            tools = ['nmap', 'msfconsole', 'sqlmap', 'hydra', 'aircrack-ng']
            for tool in tools:
                result = self.cc.run_command(f"pgrep -f {tool}")
                data[f'{tool}_running'] = 'yes' if result[0].strip() else 'no'

            # Check monitoring status
            data['monitoring_active'] = 'yes' if hasattr(self.cc, 'modules') and 'automated_monitoring' in self.cc.modules and self.cc.modules['automated_monitoring'].is_monitoring else 'no'

        except Exception as e:
            data['error'] = str(e)

        return data

    def generate_recommendations(self):
        """Generate dashboard recommendations"""
        recommendations = []

        # Check system resources
        system_data = self.get_system_overview_data()
        try:
            # High CPU usage
            cpu_str = system_data.get('cpu_usage', '0%')
            cpu_usage = float(cpu_str.rstrip('%'))
            if cpu_usage > 80:
                recommendations.append("High CPU usage detected - consider optimizing running processes")

            # Low disk space
            disk_str = system_data.get('disk_available', '')
            if disk_str and disk_str.endswith('G'):
                disk_gb = float(disk_str.rstrip('G'))
                if disk_gb < 1:
                    recommendations.append("Low disk space - consider cleanup or expansion")
        except:
            pass

        # Check network status
        network_data = self.get_network_status_data()
        if network_data.get('internet_connectivity') == 'down':
            recommendations.append("Internet connectivity issues detected")

        # Check alerts
        alerts_summary = self.get_alerts_summary()
        if alerts_summary['high_severity'] > 5:
            recommendations.append("High number of critical alerts - review system security")

        if not recommendations:
            recommendations.append("System appears healthy - continue regular monitoring")

        return recommendations

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