"""
Reporting and Visualization Module for Termux Command Center
Generate charts, reports, and visual analytics for security data.
"""

import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import statistics
from collections import defaultdict, Counter

# Optional visualization dependencies
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available - visualization features disabled")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Advanced reporting and data visualization"
        self.reports_dir = self.cc.data_dir / "reports"
        self.charts_dir = self.cc.data_dir / "charts"
        self.reports_dir.mkdir(exist_ok=True)
        self.charts_dir.mkdir(exist_ok=True)

        # Set up matplotlib style if available
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('default')
        if SEABORN_AVAILABLE:
            sns.set_palette("husl")

    def run(self):
        print("\n=== Reporting & Visualization Center ===")
        print("1. Generate security overview report")
        print("2. Create network traffic charts")
        print("3. System performance visualization")
        print("4. Security incident timeline")
        print("5. Vulnerability assessment report")
        print("6. Threat intelligence summary")
        print("7. Executive dashboard report")
        print("8. Custom data visualization")
        print("9. Export data for external analysis")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.generate_security_overview()
            elif choice == "2":
                self.create_network_charts()
            elif choice == "3":
                self.system_performance_viz()
            elif choice == "4":
                self.security_incident_timeline()
            elif choice == "5":
                self.vulnerability_assessment_report()
            elif choice == "6":
                self.threat_intelligence_summary()
            elif choice == "7":
                self.executive_dashboard()
            elif choice == "8":
                self.custom_visualization()
            elif choice == "9":
                self.export_data()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def generate_security_overview(self):
        """Generate comprehensive security overview report"""
        print("=== Generating Security Overview Report ===")

        report_data = self.collect_security_data()

        # Generate text report
        report_file = self.reports_dir / f"security_overview_{int(time.time())}.txt"
        with open(report_file, 'w') as f:
            f.write("TERMUX COMMAND CENTER - SECURITY OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total security events: {report_data['total_events']}\n")
            f.write(f"Critical vulnerabilities: {report_data['critical_vulns']}\n")
            f.write(f"Active threats: {report_data['active_threats']}\n")
            f.write(f"System health score: {report_data['health_score']}/100\n\n")

            f.write("NETWORK SECURITY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Open ports: {report_data['network']['open_ports']}\n")
            f.write(f"Active connections: {report_data['network']['connections']}\n")
            f.write(f"Firewall status: {report_data['network']['firewall']}\n")
            f.write(f"IDS alerts: {report_data['network']['ids_alerts']}\n\n")

            f.write("SYSTEM SECURITY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Running services: {report_data['system']['services']}\n")
            f.write(f"User accounts: {report_data['system']['users']}\n")
            f.write(f"Failed logins (24h): {report_data['system']['failed_logins']}\n")
            f.write(f"System updates: {report_data['system']['updates']}\n\n")

            f.write("RECOMMENDATIONS\n")
            f.write("-" * 20 + "\n")
            for rec in report_data['recommendations']:
                f.write(f"• {rec}\n")

        print(f"✓ Security overview report saved: {report_file}")

        # Generate charts
        self.create_overview_charts(report_data)

    def collect_security_data(self):
        """Collect security data for reporting"""
        # In a real implementation, this would gather actual data
        # For now, we'll simulate comprehensive security data

        return {
            'total_events': 247,
            'critical_vulns': 3,
            'active_threats': 12,
            'health_score': 78,
            'network': {
                'open_ports': 23,
                'connections': 45,
                'firewall': 'Active',
                'ids_alerts': 7
            },
            'system': {
                'services': 18,
                'users': 3,
                'failed_logins': 2,
                'updates': '12 pending'
            },
            'recommendations': [
                'Update system packages immediately',
                'Review firewall rules for port 3389',
                'Enable two-factor authentication',
                'Configure intrusion detection alerts',
                'Regular security audits recommended'
            ]
        }

    def create_overview_charts(self, data):
        """Create overview charts"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available - skipping chart generation")
            return

        print("Generating overview charts...")

        # Security score gauge chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie([data['health_score'], 100-data['health_score']],
               colors=['green', 'red'], startangle=90)
        ax.text(0, 0, f"{data['health_score']}/100",
                ha='center', va='center', fontsize=20, fontweight='bold')
        plt.title('System Security Health Score')
        plt.savefig(self.charts_dir / f"security_score_{int(time.time())}.png")
        plt.close()

        # Threats and vulnerabilities bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = ['Critical Vulns', 'Active Threats', 'IDS Alerts', 'Failed Logins']
        values = [data['critical_vulns'], data['active_threats'],
                 data['network']['ids_alerts'], data['system']['failed_logins']]
        bars = ax.bar(categories, values, color=['red', 'orange', 'yellow', 'blue'])
        ax.set_ylabel('Count')
        ax.set_title('Security Metrics Overview')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        plt.savefig(self.charts_dir / f"security_metrics_{int(time.time())}.png")
        plt.close()

        print("✓ Overview charts generated")

    def create_network_charts(self):
        """Create network traffic visualization"""
        print("=== Network Traffic Visualization ===")

        # Simulate network data
        timestamps = [datetime.now() - timedelta(minutes=i) for i in range(60)]
        bytes_sent = [random.randint(1000, 50000) for _ in range(60)]
        bytes_received = [random.randint(1000, 50000) for _ in range(60)]
        connections = [random.randint(1, 20) for _ in range(60)]

        # Create time series chart
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Traffic over time
        ax1.plot(timestamps, bytes_sent, label='Sent', color='blue')
        ax1.plot(timestamps, bytes_received, label='Received', color='green')
        ax1.set_title('Network Traffic (Bytes)')
        ax1.set_ylabel('Bytes')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)

        # Connections over time
        ax2.plot(timestamps, connections, color='red')
        ax2.set_title('Active Connections')
        ax2.set_ylabel('Connections')
        ax2.tick_params(axis='x', rotation=45)

        # Traffic distribution
        ax3.hist(bytes_sent, alpha=0.7, label='Sent', color='blue', bins=20)
        ax3.hist(bytes_received, alpha=0.7, label='Received', color='green', bins=20)
        ax3.set_title('Traffic Distribution')
        ax3.set_xlabel('Bytes')
        ax3.set_ylabel('Frequency')
        ax3.legend()

        # Protocol breakdown (simulated)
        protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'Other']
        protocol_counts = [35, 15, 25, 20, 5]
        ax4.pie(protocol_counts, labels=protocols, autopct='%1.1f%%')
        ax4.set_title('Protocol Distribution')

        plt.tight_layout()
        chart_file = self.charts_dir / f"network_traffic_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Network traffic charts saved: {chart_file}")

        # Generate network report
        self.generate_network_report(timestamps, bytes_sent, bytes_received, connections)

    def generate_network_report(self, timestamps, sent, received, connections):
        """Generate network traffic report"""
        report_file = self.reports_dir / f"network_report_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("NETWORK TRAFFIC ANALYSIS REPORT\n")
            f.write("=" * 35 + "\n\n")
            f.write(f"Period: {timestamps[-1].strftime('%Y-%m-%d %H:%M')} to {timestamps[0].strftime('%Y-%m-%d %H:%M')}\n\n")

            f.write("TRAFFIC STATISTICS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total bytes sent: {sum(sent):,}\n")
            f.write(f"Total bytes received: {sum(received):,}\n")
            f.write(f"Average bytes sent/min: {statistics.mean(sent):.0f}\n")
            f.write(f"Average bytes received/min: {statistics.mean(received):.0f}\n")
            f.write(f"Peak connections: {max(connections)}\n")
            f.write(f"Average connections: {statistics.mean(connections):.1f}\n\n")

            f.write("ANOMALY DETECTION\n")
            f.write("-" * 20 + "\n")
            sent_mean = statistics.mean(sent)
            sent_stdev = statistics.stdev(sent)
            anomalies = sum(1 for x in sent if abs(x - sent_mean) > 2 * sent_stdev)
            f.write(f"Traffic anomalies detected: {anomalies}\n")
            f.write(f"Traffic variance: {statistics.variance(sent):.0f}\n\n")

            f.write("RECOMMENDATIONS\n")
            f.write("-" * 20 + "\n")
            if anomalies > 5:
                f.write("• High traffic variance detected - investigate potential security issues\n")
            if max(connections) > 15:
                f.write("• Peak connection count is high - monitor for DDoS attempts\n")
            if statistics.mean(sent) > statistics.mean(received) * 2:
                f.write("• Outbound traffic significantly higher - check for data exfiltration\n")

        print(f"✓ Network report saved: {report_file}")

    def system_performance_viz(self):
        """Create system performance visualization"""
        print("=== System Performance Visualization ===")

        # Simulate system performance data
        timestamps = [datetime.now() - timedelta(minutes=i) for i in range(60)]
        cpu_usage = [random.uniform(10, 90) for _ in range(60)]
        memory_usage = [random.uniform(20, 95) for _ in range(60)]
        disk_io = [random.randint(100, 5000) for _ in range(60)]
        network_io = [random.randint(1000, 25000) for _ in range(60)]

        # Create performance dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # CPU and Memory usage
        ax1.plot(timestamps, cpu_usage, label='CPU', color='red')
        ax1.plot(timestamps, memory_usage, label='Memory', color='blue')
        ax1.set_title('CPU & Memory Usage (%)')
        ax1.set_ylabel('Usage %')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)

        # CPU usage distribution
        ax2.hist(cpu_usage, bins=20, color='red', alpha=0.7)
        ax2.axvline(statistics.mean(cpu_usage), color='black', linestyle='--', label='Mean')
        ax2.set_title('CPU Usage Distribution')
        ax2.set_xlabel('CPU %')
        ax2.set_ylabel('Frequency')
        ax2.legend()

        # Disk and Network I/O
        ax3.plot(timestamps, disk_io, label='Disk I/O', color='green')
        ax3.plot(timestamps, network_io, label='Network I/O', color='purple')
        ax3.set_title('I/O Operations')
        ax3.set_ylabel('Operations/sec')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)

        # Performance correlation heatmap
        data = pd.DataFrame({
            'CPU': cpu_usage,
            'Memory': memory_usage,
            'Disk_IO': disk_io,
            'Network_IO': network_io
        })
        correlation = data.corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax4)
        ax4.set_title('Performance Correlation Matrix')

        plt.tight_layout()
        chart_file = self.charts_dir / f"system_performance_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ System performance charts saved: {chart_file}")

        # Generate performance report
        self.generate_performance_report(cpu_usage, memory_usage, disk_io, network_io)

    def generate_performance_report(self, cpu, memory, disk, network):
        """Generate system performance report"""
        report_file = self.reports_dir / f"performance_report_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("SYSTEM PERFORMANCE ANALYSIS REPORT\n")
            f.write("=" * 35 + "\n\n")
            f.write(f"Analysis Period: Last 60 minutes\n\n")

            f.write("PERFORMANCE METRICS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Average CPU usage: {statistics.mean(cpu):.1f}%\n")
            f.write(f"Peak CPU usage: {max(cpu):.1f}%\n")
            f.write(f"Average memory usage: {statistics.mean(memory):.1f}%\n")
            f.write(f"Peak memory usage: {max(memory):.1f}%\n")
            f.write(f"Average disk I/O: {statistics.mean(disk):.0f} ops/sec\n")
            f.write(f"Average network I/O: {statistics.mean(network):.0f} ops/sec\n\n")

            f.write("PERFORMANCE ANALYSIS\n")
            f.write("-" * 20 + "\n")
            if max(cpu) > 85:
                f.write("⚠️ Critical: CPU usage exceeded 85% - potential bottleneck\n")
            if statistics.mean(memory) > 80:
                f.write("⚠️ Warning: High average memory usage detected\n")
            if statistics.mean(cpu) < 20:
                f.write("✓ Good: CPU utilization is efficient\n")
            if statistics.mean(memory) < 70:
                f.write("✓ Good: Memory usage is within normal range\n\n")

            f.write("RECOMMENDATIONS\n")
            f.write("-" * 20 + "\n")
            if max(cpu) > 90:
                f.write("• Investigate high CPU usage processes\n")
                f.write("• Consider CPU optimization or upgrade\n")
            if statistics.mean(memory) > 85:
                f.write("• Monitor memory-intensive applications\n")
                f.write("• Consider memory optimization or increase RAM\n")
            f.write("• Schedule regular performance monitoring\n")
            f.write("• Implement automated alerts for performance thresholds\n")

        print(f"✓ Performance report saved: {report_file}")

    def security_incident_timeline(self):
        """Create security incident timeline visualization"""
        print("=== Security Incident Timeline ===")

        # Simulate incident data
        incidents = [
            {'date': datetime.now() - timedelta(days=7), 'type': 'Brute Force', 'severity': 'Medium'},
            {'date': datetime.now() - timedelta(days=5), 'type': 'Malware', 'severity': 'High'},
            {'date': datetime.now() - timedelta(days=3), 'type': 'DDoS', 'severity': 'Critical'},
            {'date': datetime.now() - timedelta(days=1), 'type': 'Data Breach', 'severity': 'High'},
            {'date': datetime.now() - timedelta(hours=12), 'type': 'Phishing', 'severity': 'Low'},
        ]

        # Create timeline chart
        fig, ax = plt.subplots(figsize=(12, 6))

        severity_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red', 'Critical': 'darkred'}
        severity_levels = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}

        for incident in incidents:
            y_pos = severity_levels[incident['severity']]
            ax.scatter(incident['date'], y_pos,
                      color=severity_colors[incident['severity']],
                      s=100, alpha=0.7)
            ax.text(incident['date'], y_pos + 0.1, incident['type'],
                   ha='center', va='bottom', fontsize=8, rotation=45)

        ax.set_yticks(list(severity_levels.values()))
        ax.set_yticklabels(list(severity_levels.keys()))
        ax.set_title('Security Incident Timeline')
        ax.set_xlabel('Date')
        ax.set_ylabel('Severity')
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_file = self.charts_dir / f"incident_timeline_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Incident timeline chart saved: {chart_file}")

        # Generate incident report
        self.generate_incident_report(incidents)

    def generate_incident_report(self, incidents):
        """Generate security incident report"""
        report_file = self.reports_dir / f"incident_report_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("SECURITY INCIDENT TIMELINE REPORT\n")
            f.write("=" * 35 + "\n\n")
            f.write(f"Report Period: Last 7 days\n")
            f.write(f"Total Incidents: {len(incidents)}\n\n")

            f.write("INCIDENT SUMMARY\n")
            f.write("-" * 20 + "\n")
            severity_count = Counter(incident['severity'] for incident in incidents)
            for severity, count in severity_count.items():
                f.write(f"{severity}: {count} incidents\n")

            f.write("\nINCIDENT DETAILS\n")
            f.write("-" * 20 + "\n")
            for incident in sorted(incidents, key=lambda x: x['date'], reverse=True):
                f.write(f"{incident['date'].strftime('%Y-%m-%d %H:%M')} - {incident['type']} ({incident['severity']})\n")

            f.write("\nTREND ANALYSIS\n")
            f.write("-" * 20 + "\n")
            recent_incidents = [i for i in incidents if i['date'] > datetime.now() - timedelta(days=1)]
            f.write(f"Incidents in last 24 hours: {len(recent_incidents)}\n")

            high_severity = [i for i in incidents if i['severity'] in ['High', 'Critical']]
            f.write(f"High/Critical incidents: {len(high_severity)}\n")

            if len(recent_incidents) > 2:
                f.write("⚠️ Warning: Increased incident frequency detected\n")
            if len(high_severity) > 0:
                f.write("⚠️ Critical: High-severity incidents require immediate attention\n")

        print(f"✓ Incident report saved: {report_file}")

    def vulnerability_assessment_report(self):
        """Generate vulnerability assessment report"""
        print("=== Vulnerability Assessment Report ===")

        # Simulate vulnerability data
        vulnerabilities = [
            {'id': 'CVE-2023-1234', 'severity': 'Critical', 'cvss': 9.8, 'affected': 'OpenSSH', 'status': 'Unpatched'},
            {'id': 'CVE-2023-2345', 'severity': 'High', 'cvss': 8.2, 'affected': 'Apache', 'status': 'Patched'},
            {'id': 'CVE-2023-3456', 'severity': 'Medium', 'cvss': 6.5, 'affected': 'Kernel', 'status': 'Unpatched'},
            {'id': 'CVE-2023-4567', 'severity': 'Low', 'cvss': 3.1, 'affected': 'LibSSL', 'status': 'Patched'},
        ]

        # Create vulnerability charts
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Severity distribution
        severity_counts = Counter(v['severity'] for v in vulnerabilities)
        ax1.pie(severity_counts.values(), labels=severity_counts.keys(), autopct='%1.1f%%')
        ax1.set_title('Vulnerability Severity Distribution')

        # CVSS scores
        cvss_scores = [v['cvss'] for v in vulnerabilities]
        ax2.hist(cvss_scores, bins=10, color='red', alpha=0.7)
        ax2.set_title('CVSS Score Distribution')
        ax2.set_xlabel('CVSS Score')
        ax2.set_ylabel('Count')

        # Status distribution
        status_counts = Counter(v['status'] for v in vulnerabilities)
        bars = ax3.bar(status_counts.keys(), status_counts.values(),
                      color=['red', 'green'])
        ax3.set_title('Patch Status')
        ax3.set_ylabel('Count')
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')

        # Affected components
        affected_counts = Counter(v['affected'] for v in vulnerabilities)
        ax4.barh(list(affected_counts.keys()), list(affected_counts.values()),
                color='orange')
        ax4.set_title('Most Affected Components')
        ax4.set_xlabel('Vulnerability Count')

        plt.tight_layout()
        chart_file = self.charts_dir / f"vulnerability_assessment_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Vulnerability assessment charts saved: {chart_file}")

        # Generate vulnerability report
        self.generate_vulnerability_report(vulnerabilities)

    def generate_vulnerability_report(self, vulnerabilities):
        """Generate detailed vulnerability report"""
        report_file = self.reports_dir / f"vulnerability_report_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("VULNERABILITY ASSESSMENT REPORT\n")
            f.write("=" * 35 + "\n\n")
            f.write(f"Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Vulnerabilities: {len(vulnerabilities)}\n\n")

            f.write("VULNERABILITY SUMMARY\n")
            f.write("-" * 25 + "\n")
            severity_count = Counter(v['severity'] for v in vulnerabilities)
            for severity, count in severity_count.items():
                f.write(f"{severity}: {count}\n")

            status_count = Counter(v['status'] for v in vulnerabilities)
            f.write(f"\nPatch Status:\n")
            for status, count in status_count.items():
                f.write(f"{status}: {count}\n")

            f.write(f"\nAverage CVSS Score: {statistics.mean(v['cvss'] for v in vulnerabilities):.1f}\n\n")

            f.write("DETAILED VULNERABILITIES\n")
            f.write("-" * 25 + "\n")
            for vuln in sorted(vulnerabilities, key=lambda x: x['cvss'], reverse=True):
                f.write(f"ID: {vuln['id']}\n")
                f.write(f"Severity: {vuln['severity']} (CVSS: {vuln['cvss']})\n")
                f.write(f"Affected: {vuln['affected']}\n")
                f.write(f"Status: {vuln['status']}\n\n")

            f.write("RECOMMENDATIONS\n")
            f.write("-" * 15 + "\n")
            unpatched_critical = [v for v in vulnerabilities if v['severity'] == 'Critical' and v['status'] == 'Unpatched']
            if unpatched_critical:
                f.write(f"• CRITICAL: Patch {len(unpatched_critical)} critical vulnerabilities immediately\n")

            unpatched_high = [v for v in vulnerabilities if v['severity'] == 'High' and v['status'] == 'Unpatched']
            if unpatched_high:
                f.write(f"• HIGH PRIORITY: Patch {len(unpatched_high)} high-severity vulnerabilities\n")

            f.write("• Schedule regular vulnerability scans\n")
            f.write("• Implement automated patch management\n")
            f.write("• Review vulnerability management policies\n")

        print(f"✓ Vulnerability report saved: {report_file}")

    def threat_intelligence_summary(self):
        """Generate threat intelligence summary"""
        print("=== Threat Intelligence Summary ===")

        # Simulate threat intelligence data
        threats = {
            'malware_families': ['Ransomware', 'Trojan', 'Spyware', 'Rootkit'],
            'threat_actors': ['APT28', 'Lazarus', 'Unknown'],
            'targeted_industries': ['Finance', 'Healthcare', 'Technology'],
            'attack_vectors': ['Phishing', 'Web Exploitation', 'RDP', 'Supply Chain']
        }

        threat_counts = {
            'malware_families': [15, 8, 12, 3],
            'threat_actors': [5, 3, 20],
            'targeted_industries': [25, 18, 22],
            'attack_vectors': [35, 15, 10, 5]
        }

        # Create threat intelligence dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Malware families
        ax1.bar(threats['malware_families'], threat_counts['malware_families'],
               color='darkred')
        ax1.set_title('Malware Family Distribution')
        ax1.tick_params(axis='x', rotation=45)

        # Threat actors
        ax2.pie(threat_counts['threat_actors'], labels=threats['threat_actors'],
               autopct='%1.1f%%')
        ax2.set_title('Threat Actor Activity')

        # Targeted industries
        ax3.barh(threats['targeted_industries'], threat_counts['targeted_industries'],
                color='orange')
        ax3.set_title('Targeted Industries')

        # Attack vectors
        ax4.bar(threats['attack_vectors'], threat_counts['attack_vectors'],
               color='purple')
        ax4.set_title('Attack Vector Distribution')
        ax4.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        chart_file = self.charts_dir / f"threat_intelligence_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Threat intelligence charts saved: {chart_file}")

        # Generate threat intelligence report
        self.generate_threat_report(threats, threat_counts)

    def generate_threat_report(self, threats, counts):
        """Generate threat intelligence report"""
        report_file = self.reports_dir / f"threat_intelligence_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("THREAT INTELLIGENCE SUMMARY REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Intelligence Period: Last 30 days\n\n")

            f.write("THREAT LANDSCAPE OVERVIEW\n")
            f.write("-" * 30 + "\n")
            f.write(f"Active Malware Families: {len(threats['malware_families'])}\n")
            f.write(f"Identified Threat Actors: {len(threats['threat_actors'])}\n")
            f.write(f"Targeted Industries: {len(threats['targeted_industries'])}\n")
            f.write(f"Primary Attack Vectors: {len(threats['attack_vectors'])}\n\n")

            f.write("TOP THREATS\n")
            f.write("-" * 15 + "\n")
            f.write("Malware Families:\n")
            for family, count in zip(threats['malware_families'], counts['malware_families']):
                f.write(f"• {family}: {count} incidents\n")

            f.write("\nAttack Vectors:\n")
            for vector, count in zip(threats['attack_vectors'], counts['attack_vectors']):
                f.write(f"• {vector}: {count} attacks\n")

            f.write("\nINDUSTRY TARGETING\n")
            f.write("-" * 20 + "\n")
            for industry, count in zip(threats['targeted_industries'], counts['targeted_industries']):
                f.write(f"• {industry}: {count} targeted attacks\n")

            f.write("\nRECOMMENDATIONS\n")
            f.write("-" * 15 + "\n")
            f.write("• Enhance phishing awareness training\n")
            f.write("• Implement multi-factor authentication\n")
            f.write("• Regular security assessments\n")
            f.write("• Monitor for emerging malware signatures\n")
            f.write("• Update incident response procedures\n")

        print(f"✓ Threat intelligence report saved: {report_file}")

    def executive_dashboard(self):
        """Generate executive dashboard report"""
        print("=== Executive Security Dashboard ===")

        # Simulate executive metrics
        metrics = {
            'security_score': 82,
            'threat_level': 'Moderate',
            'compliance_score': 94,
            'incident_response_time': 45,  # minutes
            'uptime_percentage': 99.7,
            'data_loss_prevention': 98
        }

        kpis = {
            'Total Incidents': 23,
            'Resolved Incidents': 21,
            'Active Threats': 2,
            'Critical Assets': 156,
            'Protected Assets': 152,
            'Security Training': 89  # percentage completion
        }

        # Create executive dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Security score gauge
        ax1.pie([metrics['security_score'], 100-metrics['security_score']],
               colors=['green', 'lightgray'], startangle=90)
        ax1.text(0, 0, f"{metrics['security_score']}%",
                ha='center', va='center', fontsize=24, fontweight='bold')
        ax1.set_title('Overall Security Score')

        # KPI dashboard
        kpi_names = list(kpis.keys())
        kpi_values = list(kpis.values())
        bars = ax2.barh(kpi_names, kpi_values, color='skyblue')
        ax2.set_title('Key Performance Indicators')
        ax2.set_xlabel('Value')
        for bar in bars:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center')

        # Threat level indicator
        threat_colors = {'Low': 'green', 'Moderate': 'yellow', 'High': 'red', 'Critical': 'darkred'}
        ax3.bar(['Threat Level'], [1], color=threat_colors[metrics['threat_level']])
        ax3.set_title(f'Current Threat Level: {metrics["threat_level"]}')
        ax3.set_ylim(0, 1)
        ax3.set_yticks([])

        # Compliance and uptime
        categories = ['Compliance', 'Uptime', 'DLP']
        values = [metrics['compliance_score'], metrics['uptime_percentage'], metrics['data_loss_prevention']]
        bars = ax4.bar(categories, values, color=['blue', 'green', 'orange'])
        ax4.set_title('Compliance & Availability Metrics')
        ax4.set_ylabel('Percentage')
        ax4.set_ylim(0, 100)
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')

        plt.tight_layout()
        chart_file = self.charts_dir / f"executive_dashboard_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Executive dashboard saved: {chart_file}")

        # Generate executive report
        self.generate_executive_report(metrics, kpis)

    def generate_executive_report(self, metrics, kpis):
        """Generate executive summary report"""
        report_file = self.reports_dir / f"executive_summary_{int(time.time())}.txt"

        with open(report_file, 'w') as f:
            f.write("EXECUTIVE SECURITY SUMMARY\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")

            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Overall Security Score: {metrics['security_score']}/100\n")
            f.write(f"Current Threat Level: {metrics['threat_level']}\n")
            f.write(f"Compliance Score: {metrics['compliance_score']}%\n")
            f.write(f"System Uptime: {metrics['uptime_percentage']}%\n\n")

            f.write("KEY PERFORMANCE INDICATORS\n")
            f.write("-" * 30 + "\n")
            for kpi, value in kpis.items():
                f.write(f"{kpi}: {value}\n")

            f.write("\nINCIDENT RESPONSE METRICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Average Response Time: {metrics['incident_response_time']} minutes\n")
            f.write(f"Resolution Rate: {(kpis['Resolved Incidents']/kpis['Total Incidents']*100):.1f}%\n")
            f.write(f"Active Threats: {kpis['Active Threats']}\n\n")

            f.write("ASSET PROTECTION STATUS\n")
            f.write("-" * 25 + "\n")
            f.write(f"Total Critical Assets: {kpis['Critical Assets']}\n")
            f.write(f"Protected Assets: {kpis['Protected Assets']} ({kpis['Protected Assets']/kpis['Critical Assets']*100:.1f}%)\n")
            f.write(f"Data Loss Prevention: {metrics['data_loss_prevention']}%\n\n")

            f.write("RECOMMENDATIONS FOR EXECUTIVE ACTION\n")
            f.write("-" * 40 + "\n")
            if metrics['security_score'] < 85:
                f.write("• Increase security investment to improve overall score\n")
            if kpis['Active Threats'] > 0:
                f.write("• Address active threats with immediate priority\n")
            if metrics['compliance_score'] < 95:
                f.write("• Review compliance requirements and remediation plans\n")
            f.write("• Continue security awareness training program\n")
            f.write("• Schedule quarterly security posture review\n")

        print(f"✓ Executive summary report saved: {report_file}")

    def custom_visualization(self):
        """Create custom data visualization"""
        print("=== Custom Data Visualization ===")

        print("Available data sources:")
        print("1. Security logs")
        print("2. Network traffic")
        print("3. System performance")
        print("4. Vulnerability scans")
        print("5. Threat intelligence")

        choice = input("Select data source (1-5): ").strip()

        data_sources = {
            '1': 'security_logs',
            '2': 'network_traffic',
            '3': 'system_performance',
            '4': 'vulnerability_scans',
            '5': 'threat_intelligence'
        }

        if choice in data_sources:
            data_source = data_sources[choice]
            print(f"Selected: {data_source}")

            # Generate custom visualization based on selection
            self.generate_custom_chart(data_source)
        else:
            print("Invalid choice.")

    def generate_custom_chart(self, data_source):
        """Generate custom chart based on data source"""
        # Simulate custom data based on source
        if data_source == 'security_logs':
            # Security events over time
            dates = [datetime.now() - timedelta(days=i) for i in range(30)]
            events = [random.randint(1, 50) for _ in range(30)]

            plt.figure(figsize=(12, 6))
            plt.plot(dates, events, marker='o')
            plt.title('Security Events Over Time')
            plt.xlabel('Date')
            plt.ylabel('Number of Events')
            plt.xticks(rotation=45)

        elif data_source == 'network_traffic':
            # Network traffic heatmap
            hours = range(24)
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            traffic = [[random.randint(100, 1000) for _ in hours] for _ in days]

            plt.figure(figsize=(12, 8))
            sns.heatmap(traffic, xticklabels=hours, yticklabels=days, cmap='YlOrRd')
            plt.title('Network Traffic Heatmap')
            plt.xlabel('Hour of Day')
            plt.ylabel('Day of Week')

        elif data_source == 'system_performance':
            # Performance radar chart
            categories = ['CPU', 'Memory', 'Disk', 'Network', 'Security']
            values = [random.uniform(60, 95) for _ in categories]

            angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
            angles += angles[:1]
            values += values[:1]

            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values)
            ax.fill(angles, values, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_title('System Performance Radar')

        elif data_source == 'vulnerability_scans':
            # Vulnerability severity treemap
            severities = ['Critical', 'High', 'Medium', 'Low']
            counts = [5, 15, 25, 35]

            plt.figure(figsize=(10, 6))
            plt.bar(severities, counts, color=['darkred', 'red', 'orange', 'yellow'])
            plt.title('Vulnerability Severity Distribution')
            plt.xlabel('Severity')
            plt.ylabel('Count')

        elif data_source == 'threat_intelligence':
            # Threat actor activity timeline
            actors = ['APT28', 'Lazarus', 'Unknown', 'State-sponsored']
            activity = [random.randint(1, 20) for _ in actors]

            plt.figure(figsize=(10, 6))
            plt.barh(actors, activity, color='darkred')
            plt.title('Threat Actor Activity Levels')
            plt.xlabel('Activity Level')

        plt.tight_layout()
        chart_file = self.charts_dir / f"custom_{data_source}_{int(time.time())}.png"
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Custom visualization saved: {chart_file}")

    def export_data(self):
        """Export data for external analysis"""
        print("=== Data Export for External Analysis ===")

        print("Available export formats:")
        print("1. CSV (Spreadsheet analysis)")
        print("2. JSON (API integration)")
        print("3. XML (Legacy systems)")
        print("4. Excel (Business intelligence)")

        choice = input("Select export format (1-4): ").strip()

        formats = {
            '1': 'csv',
            '2': 'json',
            '3': 'xml',
            '4': 'xlsx'
        }

        if choice in formats:
            format_type = formats[choice]
            print(f"Exporting data in {format_type.upper()} format...")

            # Simulate data export
            export_data = {
                'security_events': [
                    {'timestamp': '2024-01-01T10:00:00', 'type': 'login', 'severity': 'low'},
                    {'timestamp': '2024-01-01T10:15:00', 'type': 'file_access', 'severity': 'medium'},
                ],
                'network_traffic': [
                    {'timestamp': '2024-01-01T10:00:00', 'bytes_sent': 1500, 'bytes_received': 2000},
                    {'timestamp': '2024-01-01T10:01:00', 'bytes_sent': 1800, 'bytes_received': 2200},
                ],
                'system_metrics': [
                    {'timestamp': '2024-01-01T10:00:00', 'cpu': 45.2, 'memory': 67.8},
                    {'timestamp': '2024-01-01T10:01:00', 'cpu': 52.1, 'memory': 71.3},
                ]
            }

            export_file = self.cc.data_dir / f"security_data_export_{int(time.time())}.{format_type}"
            self.save_export_data(export_data, export_file, format_type)

            print(f"✓ Data exported to: {export_file}")
        else:
            print("Invalid choice.")

    def save_export_data(self, data, file_path, format_type):
        """Save exported data in specified format"""
        if format_type == 'json':
            import json
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        elif format_type == 'csv':
            import csv
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write security events
                writer.writerow(['Section', 'Timestamp', 'Type', 'Severity/Value'])
                for event in data['security_events']:
                    writer.writerow(['security_events', event['timestamp'], event['type'], event['severity']])
                for traffic in data['network_traffic']:
                    writer.writerow(['network_traffic', traffic['timestamp'], 'bytes_sent', traffic['bytes_sent']])
                    writer.writerow(['network_traffic', traffic['timestamp'], 'bytes_received', traffic['bytes_received']])

        elif format_type == 'xml':
            # Simple XML export
            xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<security_data>\n'
            for section, items in data.items():
                xml_content += f'  <{section}>\n'
                for item in items:
                    xml_content += '    <item>\n'
                    for key, value in item.items():
                        xml_content += f'      <{key}>{value}</{key}>\n'
                    xml_content += '    </item>\n'
                xml_content += f'  </{section}>\n'
            xml_content += '</security_data>'

            with open(file_path, 'w') as f:
                f.write(xml_content)

        elif format_type == 'xlsx':
            try:
                import pandas as pd
                # Convert to DataFrames and save as Excel
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for section, items in data.items():
                        df = pd.DataFrame(items)
                        df.to_excel(writer, sheet_name=section, index=False)
            except ImportError:
                print("pandas/openpyxl not available, saving as CSV instead")
                self.save_export_data(data, file_path.with_suffix('.csv'), 'csv')