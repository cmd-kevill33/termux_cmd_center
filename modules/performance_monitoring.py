"""
Performance Monitoring Module for Termux Command Center
Monitor system performance, resource usage, and optimize operations.
"""

import json
import time
import psutil
import os
from datetime import datetime, timedelta
from pathlib import Path
import threading
import statistics
from collections import defaultdict, deque

# Optional visualization dependencies
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available - chart features disabled")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "System performance monitoring and optimization"
        self.monitoring_dir = self.cc.data_dir / "monitoring"
        self.metrics_dir = self.monitoring_dir / "metrics"
        self.alerts_dir = self.monitoring_dir / "alerts"

        # Create directories
        self.monitoring_dir.mkdir(exist_ok=True)
        self.metrics_dir.mkdir(exist_ok=True)
        self.alerts_dir.mkdir(exist_ok=True)

        # Monitoring configuration
        self.monitoring_active = False
        self.collection_interval = 30  # seconds
        self.retention_days = 7
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'network_connections': 100
        }

        # Data storage
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.alerts = []
        self.performance_baseline = {}

        # Monitoring thread
        self.monitor_thread = None

        # Set up matplotlib style if available
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('default')
        if SEABORN_AVAILABLE:
            sns.set_palette("husl")

    def run(self):
        print("\n=== Performance Monitoring Center ===")
        print("1. Start performance monitoring")
        print("2. Stop performance monitoring")
        print("3. View real-time metrics")
        print("4. Performance analytics")
        print("5. System health check")
        print("6. Resource usage reports")
        print("7. Performance alerts")
        print("8. Optimization recommendations")
        print("9. Monitoring configuration")
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
                self.view_realtime_metrics()
            elif choice == "4":
                self.performance_analytics()
            elif choice == "5":
                self.system_health_check()
            elif choice == "6":
                self.resource_usage_reports()
            elif choice == "7":
                self.performance_alerts()
            elif choice == "8":
                self.optimization_recommendations()
            elif choice == "9":
                self.monitoring_configuration()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            print("Monitoring is already active!")
            return

        print("Starting performance monitoring...")
        self.monitoring_active = True

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()

        print("✓ Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring_active:
            print("Monitoring is not active!")
            return

        print("Stopping performance monitoring...")
        self.monitoring_active = False

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        print("✓ Performance monitoring stopped")

    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect metrics
                metrics = self.collect_system_metrics()

                # Store metrics
                timestamp = datetime.now()
                for metric_name, value in metrics.items():
                    self.metrics_history[metric_name].append({
                        'timestamp': timestamp,
                        'value': value
                    })

                # Check for alerts
                self.check_alerts(metrics, timestamp)

                # Save metrics periodically (every 5 minutes)
                if int(time.time()) % 300 == 0:
                    self.save_metrics_snapshot()

                time.sleep(self.collection_interval)

            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)

    def collect_system_metrics(self):
        """Collect comprehensive system metrics"""
        metrics = {}

        try:
            # CPU metrics
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['cpu_count'] = psutil.cpu_count()
            metrics['cpu_freq'] = psutil.cpu_freq().current if psutil.cpu_freq() else 0

            # Memory metrics
            memory = psutil.virtual_memory()
            metrics['memory_percent'] = memory.percent
            metrics['memory_used'] = memory.used
            metrics['memory_total'] = memory.total

            # Disk metrics
            disk = psutil.disk_usage('/')
            metrics['disk_percent'] = disk.percent
            metrics['disk_used'] = disk.used
            metrics['disk_total'] = disk.total

            # Network metrics
            network = psutil.net_io_counters()
            metrics['network_bytes_sent'] = network.bytes_sent
            metrics['network_bytes_recv'] = network.bytes_recv
            metrics['network_packets_sent'] = network.packets_sent
            metrics['network_packets_recv'] = network.packets_recv

            # Process metrics
            metrics['process_count'] = len(psutil.pids())

            # System load
            load = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
            metrics['system_load_1'] = load[0]
            metrics['system_load_5'] = load[1]
            metrics['system_load_15'] = load[2]

            # Battery (if available)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    metrics['battery_percent'] = battery.percent
                    metrics['battery_plugged'] = battery.power_plugged
            except:
                pass

        except Exception as e:
            print(f"Error collecting metrics: {e}")

        return metrics

    def check_alerts(self, metrics, timestamp):
        """Check metrics against alert thresholds"""
        alerts_triggered = []

        # CPU alert
        if metrics.get('cpu_percent', 0) > self.alert_thresholds['cpu_percent']:
            alerts_triggered.append({
                'type': 'cpu',
                'message': f"High CPU usage: {metrics['cpu_percent']:.1f}%",
                'severity': 'warning' if metrics['cpu_percent'] < 90 else 'critical',
                'value': metrics['cpu_percent'],
                'threshold': self.alert_thresholds['cpu_percent']
            })

        # Memory alert
        if metrics.get('memory_percent', 0) > self.alert_thresholds['memory_percent']:
            alerts_triggered.append({
                'type': 'memory',
                'message': f"High memory usage: {metrics['memory_percent']:.1f}%",
                'severity': 'warning' if metrics['memory_percent'] < 95 else 'critical',
                'value': metrics['memory_percent'],
                'threshold': self.alert_thresholds['memory_percent']
            })

        # Disk alert
        if metrics.get('disk_percent', 0) > self.alert_thresholds['disk_percent']:
            alerts_triggered.append({
                'type': 'disk',
                'message': f"High disk usage: {metrics['disk_percent']:.1f}%",
                'severity': 'warning',
                'value': metrics['disk_percent'],
                'threshold': self.alert_thresholds['disk_percent']
            })

        # Add alerts to list
        for alert in alerts_triggered:
            alert['timestamp'] = timestamp.isoformat()
            self.alerts.append(alert)

            # Keep only recent alerts (last 100)
            if len(self.alerts) > 100:
                self.alerts.pop(0)

        # Save alerts if any were triggered
        if alerts_triggered:
            self.save_alert_snapshot()

    def save_metrics_snapshot(self):
        """Save current metrics snapshot"""
        timestamp = datetime.now()
        filename = f"metrics_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.metrics_dir / filename

        snapshot = {
            'timestamp': timestamp.isoformat(),
            'metrics': dict(self.metrics_history)
        }

        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2, default=str)

    def save_alert_snapshot(self):
        """Save current alerts"""
        timestamp = datetime.now()
        filename = f"alerts_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.alerts_dir / filename

        with open(filepath, 'w') as f:
            json.dump(self.alerts[-10:], f, indent=2)  # Save last 10 alerts

    def view_realtime_metrics(self):
        """View real-time system metrics"""
        print("=== Real-Time System Metrics ===")

        if not self.metrics_history:
            print("No metrics available. Start monitoring first.")
            return

        # Get latest metrics
        latest_metrics = {}
        for metric_name, history in self.metrics_history.items():
            if history:
                latest_metrics[metric_name] = history[-1]['value']

        if not latest_metrics:
            print("No recent metrics available.")
            return

        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        # CPU Metrics
        print("CPU:")
        print(".1f")
        print(f"  Cores: {latest_metrics.get('cpu_count', 'N/A')}")
        if 'cpu_freq' in latest_metrics:
            print(".0f")

        # Memory Metrics
        print("\nMemory:")
        print(".1f")
        print(".1f")
        print(".1f")

        # Disk Metrics
        print("\nDisk:")
        print(".1f")
        print(".1f")
        print(".1f")

        # Network Metrics
        print("\nNetwork (Total):")
        print(",.0f")
        print(",.0f")

        # System Load
        print("\nSystem Load:")
        print(".2f")
        print(".2f")
        print(".2f")

        # Process Count
        print(f"\nProcess Count: {latest_metrics.get('process_count', 'N/A')}")

        # Battery (if available)
        if 'battery_percent' in latest_metrics:
            print("\nBattery:")
            print(f"  Level: {latest_metrics.get('battery_percent', 0):.1f}%")
            print(f"  Plugged in: {latest_metrics.get('battery_plugged', 'N/A')}")

    def performance_analytics(self):
        """Performance analytics and trends"""
        print("=== Performance Analytics ===")

        if not self.metrics_history:
            print("No historical data available.")
            return

        # Analyze CPU trends
        self.analyze_cpu_trends()

        # Analyze memory patterns
        self.analyze_memory_patterns()

        # Analyze resource correlations
        self.analyze_resource_correlations()

        # Generate performance report
        self.generate_performance_report()

    def analyze_cpu_trends(self):
        """Analyze CPU usage trends"""
        print("\nCPU Usage Analysis:")

        cpu_history = [m['value'] for m in self.metrics_history.get('cpu_percent', [])]
        if not cpu_history:
            print("No CPU data available.")
            return

        print(".1f")
        print(".1f")
        print(".1f")

        # Trend analysis
        if len(cpu_history) >= 10:
            recent_avg = statistics.mean(cpu_history[-10:])
            older_avg = statistics.mean(cpu_history[:-10]) if len(cpu_history) > 10 else recent_avg

            if older_avg > 0:
                trend = (recent_avg - older_avg) / older_avg * 100
                if trend > 5:
                    print(".1f")
                elif trend < -5:
                    print(".1f")
                else:
                    print("  Trend: Stable")

    def analyze_memory_patterns(self):
        """Analyze memory usage patterns"""
        print("\nMemory Usage Analysis:")

        memory_history = [m['value'] for m in self.metrics_history.get('memory_percent', [])]
        if not memory_history:
            print("No memory data available.")
            return

        print(".1f")
        print(".1f")
        print(".1f")

        # Memory pressure analysis
        high_usage_count = sum(1 for m in memory_history if m > 80)
        high_usage_percent = high_usage_count / len(memory_history) * 100

        print(".1f")
        if high_usage_percent > 50:
            print("  ⚠️ High memory pressure detected")
        elif high_usage_percent > 20:
            print("  ⚠️ Moderate memory pressure")
        else:
            print("  ✓ Memory usage normal")

    def analyze_resource_correlations(self):
        """Analyze correlations between resources"""
        print("\nResource Correlation Analysis:")

        cpu_data = [m['value'] for m in self.metrics_history.get('cpu_percent', [])]
        memory_data = [m['value'] for m in self.metrics_history.get('memory_percent', [])]

        if len(cpu_data) >= 10 and len(memory_data) >= 10:
            try:
                correlation = statistics.correlation(cpu_data[-50:], memory_data[-50:])
                print(".3f")

                if correlation > 0.7:
                    print("  💡 Strong positive correlation - CPU and memory usage tend to increase together")
                elif correlation > 0.3:
                    print("  💡 Moderate correlation between CPU and memory usage")
                else:
                    print("  💡 Low correlation between CPU and memory usage")

            except:
                print("  Unable to calculate correlation")

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print("\nGenerating Performance Report...")

        report_data = {
            'generated_at': datetime.now().isoformat(),
            'period': f"Last {len(list(self.metrics_history.values())[0]) if self.metrics_history else 0} measurements",
            'summary': self.generate_performance_summary(),
            'recommendations': self.generate_performance_recommendations(),
            'trends': self.analyze_performance_trends()
        }

        report_file = self.monitoring_dir / f"performance_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"✓ Performance report saved: {report_file}")

        # Print summary
        print("\nPerformance Summary:")
        for key, value in report_data['summary'].items():
            print(f"• {key}: {value}")

    def generate_performance_summary(self):
        """Generate performance summary statistics"""
        summary = {}

        for metric_name, history in self.metrics_history.items():
            if history:
                values = [m['value'] for m in history]
                summary[f"{metric_name}_avg"] = round(statistics.mean(values), 2)
                summary[f"{metric_name}_max"] = round(max(values), 2)
                summary[f"{metric_name}_min"] = round(min(values), 2)

        return summary

    def generate_performance_recommendations(self):
        """Generate performance optimization recommendations"""
        recommendations = []

        # CPU recommendations
        cpu_avg = self.get_metric_average('cpu_percent')
        if cpu_avg and cpu_avg > 70:
            recommendations.append("Consider optimizing CPU-intensive processes or upgrading CPU")
        elif cpu_avg and cpu_avg < 20:
            recommendations.append("CPU utilization is low - consider consolidating workloads")

        # Memory recommendations
        memory_avg = self.get_metric_average('memory_percent')
        if memory_avg and memory_avg > 80:
            recommendations.append("High memory usage detected - consider memory optimization or upgrade")
        elif memory_avg and memory_avg < 30:
            recommendations.append("Memory utilization is low - resources may be underutilized")

        # Disk recommendations
        disk_avg = self.get_metric_average('disk_percent')
        if disk_avg and disk_avg > 85:
            recommendations.append("Disk space is running low - consider cleanup or expansion")

        # General recommendations
        recommendations.extend([
            "Implement regular performance monitoring",
            "Set up automated alerts for performance thresholds",
            "Consider load balancing for high-traffic periods",
            "Regular system maintenance and updates"
        ])

        return recommendations

    def analyze_performance_trends(self):
        """Analyze performance trends over time"""
        trends = {}

        for metric_name, history in self.metrics_history.items():
            if len(history) >= 20:
                # Compare recent vs older data
                midpoint = len(history) // 2
                recent = [m['value'] for m in history[midpoint:]]
                older = [m['value'] for m in history[:midpoint]]

                if recent and older:
                    recent_avg = statistics.mean(recent)
                    older_avg = statistics.mean(older)

                    if older_avg > 0:
                        change_percent = (recent_avg - older_avg) / older_avg * 100
                        trends[metric_name] = {
                            'change_percent': round(change_percent, 2),
                            'direction': 'increasing' if change_percent > 5 else 'decreasing' if change_percent < -5 else 'stable'
                        }

        return trends

    def get_metric_average(self, metric_name):
        """Get average value for a metric"""
        history = self.metrics_history.get(metric_name, [])
        if history:
            return statistics.mean([m['value'] for m in history])
        return None

    def system_health_check(self):
        """Comprehensive system health check"""
        print("=== System Health Check ===")

        health_score = 100
        issues = []

        # Check CPU health
        cpu_avg = self.get_metric_average('cpu_percent')
        if cpu_avg:
            if cpu_avg > 90:
                health_score -= 30
                issues.append("Critical: Extremely high CPU usage")
            elif cpu_avg > 80:
                health_score -= 20
                issues.append("Warning: High CPU usage")
            elif cpu_avg < 10:
                health_score -= 5
                issues.append("Notice: Very low CPU utilization")

        # Check memory health
        memory_avg = self.get_metric_average('memory_percent')
        if memory_avg:
            if memory_avg > 95:
                health_score -= 30
                issues.append("Critical: Extremely high memory usage")
            elif memory_avg > 85:
                health_score -= 20
                issues.append("Warning: High memory usage")

        # Check disk health
        disk_avg = self.get_metric_average('disk_percent')
        if disk_avg:
            if disk_avg > 95:
                health_score -= 25
                issues.append("Critical: Disk space critically low")
            elif disk_avg > 90:
                health_score -= 15
                issues.append("Warning: Low disk space")

        # Check system load
        load_avg = self.get_metric_average('system_load_1')
        if load_avg and load_avg > 5:
            health_score -= 10
            issues.append("Warning: High system load")

        health_score = max(0, health_score)

        print(f"Overall Health Score: {health_score}/100")

        if health_score >= 90:
            print("Status: Excellent ✓")
        elif health_score >= 75:
            print("Status: Good ✓")
        elif health_score >= 60:
            print("Status: Fair ⚠️")
        elif health_score >= 40:
            print("Status: Poor ⚠️")
        else:
            print("Status: Critical ❌")

        if issues:
            print("\nIssues Found:")
            for issue in issues:
                print(f"• {issue}")
        else:
            print("\nNo significant issues detected.")

        return health_score

    def resource_usage_reports(self):
        """Generate resource usage reports"""
        print("=== Resource Usage Reports ===")

        # CPU usage report
        self.generate_cpu_report()

        # Memory usage report
        self.generate_memory_report()

        # Network usage report
        self.generate_network_report()

        # Storage usage report
        self.generate_storage_report()

        print("✓ All resource reports generated")

    def generate_cpu_report(self):
        """Generate CPU usage report"""
        cpu_history = self.metrics_history.get('cpu_percent', [])
        if not cpu_history:
            return

        # Create CPU usage chart
        timestamps = [m['timestamp'] for m in cpu_history]
        values = [m['value'] for m in cpu_history]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, values, color='red', linewidth=2)
        plt.title('CPU Usage Over Time')
        plt.xlabel('Time')
        plt.ylabel('CPU %')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        chart_file = self.monitoring_dir / "charts" / f"cpu_usage_{int(time.time())}.png"
        chart_file.parent.mkdir(exist_ok=True)
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ CPU usage chart saved: {chart_file}")

    def generate_memory_report(self):
        """Generate memory usage report"""
        memory_history = self.metrics_history.get('memory_percent', [])
        if not memory_history:
            return

        # Create memory usage chart
        timestamps = [m['timestamp'] for m in memory_history]
        values = [m['value'] for m in memory_history]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, values, color='blue', linewidth=2)
        plt.title('Memory Usage Over Time')
        plt.xlabel('Time')
        plt.ylabel('Memory %')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        chart_file = self.monitoring_dir / "charts" / f"memory_usage_{int(time.time())}.png"
        chart_file.parent.mkdir(exist_ok=True)
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Memory usage chart saved: {chart_file}")

    def generate_network_report(self):
        """Generate network usage report"""
        sent_history = self.metrics_history.get('network_bytes_sent', [])
        recv_history = self.metrics_history.get('network_bytes_recv', [])

        if not sent_history or not recv_history:
            return

        # Create network usage chart
        timestamps = [m['timestamp'] for m in sent_history]
        sent_values = [m['value'] for m in sent_history]
        recv_values = [m['value'] for m in recv_history]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, sent_values, label='Sent', color='green', linewidth=2)
        plt.plot(timestamps, recv_values, label='Received', color='orange', linewidth=2)
        plt.title('Network Traffic Over Time')
        plt.xlabel('Time')
        plt.ylabel('Bytes')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        chart_file = self.monitoring_dir / "charts" / f"network_usage_{int(time.time())}.png"
        chart_file.parent.mkdir(exist_ok=True)
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Network usage chart saved: {chart_file}")

    def generate_storage_report(self):
        """Generate storage usage report"""
        disk_history = self.metrics_history.get('disk_percent', [])
        if not disk_history:
            return

        # Create disk usage chart
        timestamps = [m['timestamp'] for m in disk_history]
        values = [m['value'] for m in disk_history]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, values, color='purple', linewidth=2)
        plt.title('Disk Usage Over Time')
        plt.xlabel('Time')
        plt.ylabel('Disk %')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        chart_file = self.monitoring_dir / "charts" / f"disk_usage_{int(time.time())}.png"
        chart_file.parent.mkdir(exist_ok=True)
        plt.savefig(chart_file)
        plt.close()

        print(f"✓ Disk usage chart saved: {chart_file}")

    def performance_alerts(self):
        """View and manage performance alerts"""
        print("=== Performance Alerts ===")

        if not self.alerts:
            print("No alerts generated yet.")
            return

        print(f"Total alerts: {len(self.alerts)}")
        print("-" * 80)

        # Show recent alerts (last 10)
        for alert in self.alerts[-10:]:
            timestamp = alert.get('timestamp', 'Unknown')
            if len(timestamp) > 19:
                timestamp = timestamp[:19]
            severity_icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}.get(alert.get('severity', 'info'), '🔵')
            print(f"{severity_icon} [{timestamp}] {alert.get('type', 'unknown').upper()}: {alert.get('message', 'No message')}")

        # Alert summary
        alert_types = defaultdict(int)
        severities = defaultdict(int)

        for alert in self.alerts:
            alert_types[alert.get('type', 'unknown')] += 1
            severities[alert.get('severity', 'info')] += 1

        print("\nAlert Summary:")
        print(f"By Type: {dict(alert_types)}")
        print(f"By Severity: {dict(severities)}")

    def optimization_recommendations(self):
        """Provide optimization recommendations"""
        print("=== Performance Optimization Recommendations ===")

        recommendations = []

        # Analyze current metrics for optimization opportunities
        cpu_avg = self.get_metric_average('cpu_percent')
        memory_avg = self.get_metric_average('memory_percent')
        disk_avg = self.get_metric_average('disk_percent')

        if cpu_avg and cpu_avg > 70:
            recommendations.extend([
                "🔧 Optimize CPU-intensive processes",
                "🔧 Consider using CPU affinity for critical processes",
                "🔧 Implement CPU usage limits for background tasks",
                "🔧 Upgrade to faster CPU if persistent high usage"
            ])

        if memory_avg and memory_avg > 80:
            recommendations.extend([
                "🔧 Increase system memory (RAM)",
                "🔧 Optimize memory usage in applications",
                "🔧 Implement memory monitoring and alerts",
                "🔧 Use memory-efficient data structures"
            ])

        if disk_avg and disk_avg > 85:
            recommendations.extend([
                "🗂️ Clean up unnecessary files and logs",
                "🗂️ Implement log rotation policies",
                "🗂️ Move data to external storage",
                "🗂️ Consider disk space monitoring alerts"
            ])

        # General optimization recommendations
        recommendations.extend([
            "⚡ Enable system caching where possible",
            "⚡ Use SSD storage for better I/O performance",
            "⚡ Implement regular system maintenance",
            "⚡ Monitor and optimize network connections",
            "⚡ Use background job scheduling for non-critical tasks"
        ])

        print("Optimization Recommendations:")
        for rec in recommendations:
            print(f"• {rec}")

        # Save recommendations
        rec_file = self.monitoring_dir / f"optimization_recommendations_{int(time.time())}.txt"
        with open(rec_file, 'w') as f:
            f.write("PERFORMANCE OPTIMIZATION RECOMMENDATIONS\n")
            f.write("=" * 45 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for rec in recommendations:
                f.write(f"{rec}\n")

        print(f"\n✓ Recommendations saved: {rec_file}")

    def monitoring_configuration(self):
        """Configure monitoring settings"""
        print("=== Monitoring Configuration ===")

        print(f"Current settings:")
        print(f"• Collection interval: {self.collection_interval} seconds")
        print(f"• Data retention: {self.retention_days} days")
        print(f"• Monitoring active: {self.monitoring_active}")

        print("\nAlert thresholds:")
        for metric, threshold in self.alert_thresholds.items():
            print(f"• {metric}: {threshold}")

        print("\nConfiguration options:")
        print("1. Change collection interval")
        print("2. Modify alert thresholds")
        print("3. Set data retention period")
        print("4. Reset monitoring data")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            new_interval = input(f"Enter new collection interval in seconds (current: {self.collection_interval}): ").strip()
            try:
                self.collection_interval = int(new_interval)
                print(f"✓ Collection interval updated to {self.collection_interval} seconds")
            except:
                print("Invalid interval!")

        elif choice == "2":
            print("Modify alert thresholds:")
            for metric, threshold in self.alert_thresholds.items():
                new_threshold = input(f"Enter new threshold for {metric} (current: {threshold}): ").strip()
                try:
                    self.alert_thresholds[metric] = float(new_threshold)
                    print(f"✓ {metric} threshold updated to {new_threshold}")
                except:
                    print(f"Invalid threshold for {metric}!")

        elif choice == "3":
            new_retention = input(f"Enter new retention period in days (current: {self.retention_days}): ").strip()
            try:
                self.retention_days = int(new_retention)
                print(f"✓ Data retention updated to {self.retention_days} days")
            except:
                print("Invalid retention period!")

        elif choice == "4":
            confirm = input("Are you sure you want to reset all monitoring data? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.metrics_history.clear()
                self.alerts.clear()
                print("✓ Monitoring data reset")

        else:
            print("Invalid choice!")