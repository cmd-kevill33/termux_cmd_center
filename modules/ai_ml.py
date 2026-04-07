"""
AI/ML Module for Termux Command Center
Machine learning-powered anomaly detection and automated analysis.
"""

import json
import time
import statistics
import math
from datetime import datetime, timedelta
from pathlib import Path
import random
from collections import defaultdict, deque

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "AI-powered anomaly detection and automated analysis"
        self.models = {}
        self.training_data = defaultdict(list)
        self.anomalies = []
        self.predictions = {}
        self.model_file = self.cc.data_dir / "ai_models.json"
        self.load_models()

    def run(self):
        print("\n=== AI/ML Analysis Engine ===")
        print("1. Train anomaly detection models")
        print("2. Run anomaly detection on current data")
        print("3. Analyze network traffic patterns")
        print("4. Predict security threats")
        print("5. Automated incident analysis")
        print("6. Generate AI insights report")
        print("7. Configure AI settings")
        print("8. View detected anomalies")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.train_models()
            elif choice == "2":
                self.run_anomaly_detection()
            elif choice == "3":
                self.analyze_traffic_patterns()
            elif choice == "4":
                self.predict_threats()
            elif choice == "5":
                self.automated_incident_analysis()
            elif choice == "6":
                self.generate_insights_report()
            elif choice == "7":
                self.configure_ai_settings()
            elif choice == "8":
                self.view_anomalies()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def load_models(self):
        """Load trained AI models"""
        if self.model_file.exists():
            try:
                with open(self.model_file, 'r') as f:
                    self.models = json.load(f)
            except:
                self.models = {}

    def save_models(self):
        """Save trained models"""
        with open(self.model_file, 'w') as f:
            json.dump(self.models, f, indent=2)

    def train_models(self):
        """Train AI models on historical data"""
        print("=== Training AI Models ===")

        # Collect training data from various sources
        print("Collecting training data...")

        # Network traffic patterns
        self.collect_network_training_data()

        # System resource patterns
        self.collect_system_training_data()

        # Security event patterns
        self.collect_security_training_data()

        print("Training anomaly detection models...")

        # Train network anomaly model
        self.train_network_anomaly_model()

        # Train system resource model
        self.train_system_resource_model()

        # Train security event model
        self.train_security_event_model()

        self.save_models()
        print("✓ AI models trained and saved")

    def collect_network_training_data(self):
        """Collect network traffic training data"""
        print("Collecting network traffic patterns...")

        # Simulate collecting network data (in real implementation, this would use actual logs)
        for i in range(100):  # Generate sample data
            timestamp = datetime.now() - timedelta(minutes=i)
            data_point = {
                'timestamp': timestamp.isoformat(),
                'bytes_sent': random.randint(1000, 100000),
                'bytes_received': random.randint(1000, 100000),
                'connections': random.randint(1, 50),
                'ports_used': random.randint(1, 20),
                'unique_ips': random.randint(1, 10)
            }
            self.training_data['network'].append(data_point)

    def collect_system_training_data(self):
        """Collect system resource training data"""
        print("Collecting system resource patterns...")

        for i in range(100):
            timestamp = datetime.now() - timedelta(minutes=i)
            data_point = {
                'timestamp': timestamp.isoformat(),
                'cpu_usage': random.uniform(10, 90),
                'memory_usage': random.uniform(20, 95),
                'disk_io': random.randint(100, 10000),
                'network_io': random.randint(1000, 50000),
                'process_count': random.randint(50, 200)
            }
            self.training_data['system'].append(data_point)

    def collect_security_training_data(self):
        """Collect security event training data"""
        print("Collecting security event patterns...")

        event_types = ['login', 'file_access', 'network_connection', 'process_start', 'system_call']
        severities = ['low', 'medium', 'high']

        for i in range(100):
            timestamp = datetime.now() - timedelta(minutes=i)
            data_point = {
                'timestamp': timestamp.isoformat(),
                'event_type': random.choice(event_types),
                'severity': random.choice(severities),
                'source_ip': f"192.168.1.{random.randint(1, 255)}",
                'user': f"user{random.randint(1, 10)}",
                'success': random.choice([True, False])
            }
            self.training_data['security'].append(data_point)

    def train_network_anomaly_model(self):
        """Train network anomaly detection model"""
        print("Training network anomaly model...")

        if not self.training_data['network']:
            print("No network training data available")
            return

        # Simple statistical model - calculate baselines
        bytes_sent = [dp['bytes_sent'] for dp in self.training_data['network']]
        bytes_received = [dp['bytes_received'] for dp in self.training_data['network']]
        connections = [dp['connections'] for dp in self.training_data['network']]

        model = {
            'bytes_sent': {
                'mean': statistics.mean(bytes_sent),
                'stdev': statistics.stdev(bytes_sent),
                'threshold': 3  # Standard deviations
            },
            'bytes_received': {
                'mean': statistics.mean(bytes_received),
                'stdev': statistics.stdev(bytes_received),
                'threshold': 3
            },
            'connections': {
                'mean': statistics.mean(connections),
                'stdev': statistics.stdev(connections),
                'threshold': 3
            }
        }

        self.models['network_anomaly'] = model

    def train_system_resource_model(self):
        """Train system resource anomaly model"""
        print("Training system resource model...")

        if not self.training_data['system']:
            print("No system training data available")
            return

        cpu_usage = [dp['cpu_usage'] for dp in self.training_data['system']]
        memory_usage = [dp['memory_usage'] for dp in self.training_data['system']]

        model = {
            'cpu_usage': {
                'mean': statistics.mean(cpu_usage),
                'stdev': statistics.stdev(cpu_usage),
                'threshold': 2.5
            },
            'memory_usage': {
                'mean': statistics.mean(memory_usage),
                'stdev': statistics.stdev(memory_usage),
                'threshold': 2.5
            }
        }

        self.models['system_resource'] = model

    def train_security_event_model(self):
        """Train security event anomaly model"""
        print("Training security event model...")

        if not self.training_data['security']:
            print("No security training data available")
            return

        # Analyze patterns in security events
        event_counts = defaultdict(int)
        severity_counts = defaultdict(int)

        for event in self.training_data['security']:
            event_counts[event['event_type']] += 1
            severity_counts[event['severity']] += 1

        # Calculate expected frequencies
        total_events = len(self.training_data['security'])
        model = {
            'event_frequencies': dict(event_counts),
            'severity_frequencies': dict(severity_counts),
            'total_events': total_events,
            'unusual_threshold': 0.1  # 10% deviation from normal
        }

        self.models['security_event'] = model

    def run_anomaly_detection(self):
        """Run anomaly detection on current data"""
        print("=== Running Anomaly Detection ===")

        anomalies_found = []

        # Check network anomalies
        network_anomalies = self.detect_network_anomalies()
        anomalies_found.extend(network_anomalies)

        # Check system anomalies
        system_anomalies = self.detect_system_anomalies()
        anomalies_found.extend(system_anomalies)

        # Check security anomalies
        security_anomalies = self.detect_security_anomalies()
        anomalies_found.extend(security_anomalies)

        if anomalies_found:
            print(f"Found {len(anomalies_found)} anomalies:")
            for anomaly in anomalies_found:
                print(f"• {anomaly['type']}: {anomaly['description']} (confidence: {anomaly['confidence']:.2f})")
                self.anomalies.append(anomaly)
        else:
            print("No anomalies detected.")

    def detect_network_anomalies(self):
        """Detect network traffic anomalies"""
        anomalies = []

        if 'network_anomaly' not in self.models:
            return anomalies

        model = self.models['network_anomaly']

        # Get current network stats (simplified)
        try:
            # In real implementation, get actual current stats
            current_bytes_sent = random.randint(1000, 100000)
            current_bytes_received = random.randint(1000, 100000)
            current_connections = random.randint(1, 50)

            # Check for anomalies
            for metric, value in [('bytes_sent', current_bytes_sent),
                                ('bytes_received', current_bytes_received),
                                ('connections', current_connections)]:
                if metric in model:
                    mean = model[metric]['mean']
                    stdev = model[metric]['stdev']
                    threshold = model[metric]['threshold']

                    z_score = abs(value - mean) / stdev if stdev > 0 else 0
                    if z_score > threshold:
                        confidence = min(z_score / threshold, 1.0)
                        anomalies.append({
                            'type': 'network',
                            'metric': metric,
                            'description': f"Unusual {metric}: {value} (expected ~{mean:.0f})",
                            'confidence': confidence,
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'high' if confidence > 0.8 else 'medium'
                        })

        except Exception as e:
            print(f"Network anomaly detection error: {e}")

        return anomalies

    def detect_system_anomalies(self):
        """Detect system resource anomalies"""
        anomalies = []

        if 'system_resource' not in self.models:
            return anomalies

        model = self.models['system_resource']

        try:
            # Get current system stats
            result = self.cc.run_command("top -n 1 | grep 'CPU:' | awk '{print $2}'")
            cpu_str = result[0].strip().rstrip('%') if result[0] else '0'
            current_cpu = float(cpu_str)

            result = self.cc.run_command("free | grep Mem | awk '{printf $3/$2 * 100}'")
            current_memory = float(result[0]) if result[0] else 0

            # Check for anomalies
            for metric, value in [('cpu_usage', current_cpu), ('memory_usage', current_memory)]:
                if metric in model:
                    mean = model[metric]['mean']
                    stdev = model[metric]['stdev']
                    threshold = model[metric]['threshold']

                    z_score = abs(value - mean) / stdev if stdev > 0 else 0
                    if z_score > threshold:
                        confidence = min(z_score / threshold, 1.0)
                        anomalies.append({
                            'type': 'system',
                            'metric': metric,
                            'description': f"Abnormal {metric}: {value:.1f}% (normal ~{mean:.1f}%)",
                            'confidence': confidence,
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'high' if value > 90 else 'medium'
                        })

        except Exception as e:
            print(f"System anomaly detection error: {e}")

        return anomalies

    def detect_security_anomalies(self):
        """Detect security event anomalies"""
        anomalies = []

        if 'security_event' not in self.models:
            return anomalies

        model = self.models['security_event']

        # Analyze recent security events (simplified)
        try:
            # In real implementation, analyze actual logs
            recent_events = [
                {'event_type': 'login', 'severity': 'low', 'source_ip': '192.168.1.100'},
                {'event_type': 'file_access', 'severity': 'medium', 'source_ip': '192.168.1.100'},
            ]

            for event in recent_events:
                event_type = event['event_type']
                expected_freq = model['event_frequencies'].get(event_type, 0) / model['total_events']

                # Simple anomaly detection based on frequency
                if expected_freq < model['unusual_threshold']:
                    anomalies.append({
                        'type': 'security',
                        'event_type': event_type,
                        'description': f"Unusual security event: {event_type} from {event['source_ip']}",
                        'confidence': 0.8,
                        'timestamp': datetime.now().isoformat(),
                        'severity': event['severity']
                    })

        except Exception as e:
            print(f"Security anomaly detection error: {e}")

        return anomalies

    def analyze_traffic_patterns(self):
        """Analyze network traffic patterns using AI"""
        print("=== AI Traffic Pattern Analysis ===")

        if not self.training_data['network']:
            print("No training data available. Please train models first.")
            return

        # Analyze patterns
        bytes_sent = [dp['bytes_sent'] for dp in self.training_data['network']]
        bytes_received = [dp['bytes_received'] for dp in self.training_data['network']]

        print("Traffic Pattern Analysis:")
        print(f"Average bytes sent: {statistics.mean(bytes_sent):.0f}")
        print(f"Average bytes received: {statistics.mean(bytes_received):.0f}")
        print(f"Traffic variance: {statistics.variance(bytes_sent):.0f}")

        # Detect patterns
        if statistics.mean(bytes_sent) > statistics.mean(bytes_received) * 2:
            print("⚠️ Outbound traffic significantly higher than inbound - possible data exfiltration")
        elif statistics.mean(bytes_received) > statistics.mean(bytes_sent) * 2:
            print("⚠️ Inbound traffic significantly higher than outbound - possible download activity")

        # Predict future traffic
        self.predict_future_traffic()

    def predict_future_traffic(self):
        """Predict future traffic patterns"""
        print("\nTraffic Prediction (next hour):")

        if len(self.training_data['network']) < 10:
            print("Insufficient data for prediction")
            return

        # Simple linear regression for prediction
        bytes_sent = [dp['bytes_sent'] for dp in self.training_data['network'][-20:]]  # Last 20 points

        if len(bytes_sent) >= 2:
            # Calculate trend
            recent_avg = statistics.mean(bytes_sent[-5:])
            older_avg = statistics.mean(bytes_sent[:-5]) if len(bytes_sent) > 5 else recent_avg

            trend = (recent_avg - older_avg) / older_avg if older_avg > 0 else 0

            prediction = recent_avg * (1 + trend)
            print(f"Predicted bytes sent: {prediction:.0f} ({trend*100:+.1f}% change)")

    def predict_threats(self):
        """Predict potential security threats"""
        print("=== AI Threat Prediction ===")

        predictions = []

        # Analyze current system state for threat indicators
        try:
            # Check for suspicious processes
            result = self.cc.run_command("ps aux | grep -E '(nc|netcat|ncat|backdoor|trojan)' | grep -v grep")
            if result[0].strip():
                predictions.append({
                    'threat': 'Suspicious processes detected',
                    'confidence': 0.9,
                    'description': 'Network utilities running that could indicate compromise'
                })

            # Check for unusual network connections
            result = self.cc.run_command("netstat -tuln | grep -c LISTEN")
            listen_count = int(result[0].strip()) if result[0].strip().isdigit() else 0
            if listen_count > 10:
                predictions.append({
                    'threat': 'High number of listening ports',
                    'confidence': 0.7,
                    'description': f'{listen_count} ports listening - potential backdoors'
                })

            # Check system resource usage
            result = self.cc.run_command("free | grep Mem | awk '{print $3/$2 * 100}'")
            mem_usage = float(result[0]) if result[0] else 0
            if mem_usage > 95:
                predictions.append({
                    'threat': 'Critical memory usage',
                    'confidence': 0.8,
                    'description': 'System memory nearly exhausted - possible memory-based attack'
                })

        except Exception as e:
            print(f"Threat prediction error: {e}")

        if predictions:
            print("Predicted Threats:")
            for pred in predictions:
                print(f"• {pred['threat']} (confidence: {pred['confidence']:.1f})")
                print(f"  {pred['description']}")
        else:
            print("No immediate threats predicted.")

        self.predictions = predictions

    def automated_incident_analysis(self):
        """Automated incident analysis using AI"""
        print("=== Automated Incident Analysis ===")

        # Simulate incident data
        incident_data = {
            'type': 'potential_intrusion',
            'indicators': [
                'Unusual login from external IP',
                'High CPU usage spike',
                'Suspicious file modifications',
                'Network connection to known malicious domain'
            ],
            'severity': 'high',
            'affected_systems': ['web_server', 'database']
        }

        print("Analyzing incident...")
        print(f"Incident Type: {incident_data['type']}")
        print(f"Severity: {incident_data['severity']}")
        print(f"Affected Systems: {', '.join(incident_data['affected_systems'])}")

        print("\nIndicators of Compromise:")
        for indicator in incident_data['indicators']:
            print(f"• {indicator}")

        # AI-powered analysis
        analysis = self.analyze_incident(incident_data)
        print(f"\nAI Analysis: {analysis['assessment']}")
        print(f"Confidence: {analysis['confidence']:.1f}")
        print(f"Recommended Actions: {', '.join(analysis['actions'])}")

    def analyze_incident(self, incident_data):
        """AI-powered incident analysis"""
        # Simple rule-based analysis (could be enhanced with ML)
        indicators = len(incident_data['indicators'])
        severity_score = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        severity = severity_score.get(incident_data['severity'], 2)

        confidence = min((indicators * severity) / 10, 1.0)

        if confidence > 0.8:
            assessment = "High confidence of security incident"
            actions = ["Isolate affected systems", "Collect forensics", "Notify security team", "Implement containment"]
        elif confidence > 0.5:
            assessment = "Moderate confidence of security incident"
            actions = ["Monitor closely", "Review logs", "Check for additional indicators"]
        else:
            assessment = "Low confidence - likely false positive"
            actions = ["Continue monitoring", "Document for reference"]

        return {
            'assessment': assessment,
            'confidence': confidence,
            'actions': actions
        }

    def generate_insights_report(self):
        """Generate AI insights report"""
        print("Generating AI insights report...")

        report = {
            'generated_at': datetime.now().isoformat(),
            'anomalies_detected': len(self.anomalies),
            'predictions': len(self.predictions),
            'model_status': {
                'network_model': 'trained' if 'network_anomaly' in self.models else 'not_trained',
                'system_model': 'trained' if 'system_resource' in self.models else 'not_trained',
                'security_model': 'trained' if 'security_event' in self.models else 'not_trained'
            },
            'key_insights': self.generate_key_insights(),
            'recommendations': self.generate_ai_recommendations()
        }

        report_file = self.cc.data_dir / f"ai_insights_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"AI insights report saved to: {report_file}")

        # Print summary
        print("\n=== AI Insights Summary ===")
        print(f"Anomalies Detected: {report['anomalies_detected']}")
        print(f"Threat Predictions: {report['predictions']}")
        print(f"Models Trained: {sum(1 for v in report['model_status'].values() if v == 'trained')}/3")

        print("\nKey Insights:")
        for insight in report['key_insights'][:5]:
            print(f"• {insight}")

    def generate_key_insights(self):
        """Generate key insights from AI analysis"""
        insights = []

        if self.anomalies:
            high_anomalies = [a for a in self.anomalies if a.get('severity') == 'high']
            insights.append(f"Detected {len(high_anomalies)} high-severity anomalies requiring immediate attention")

        if self.predictions:
            insights.append(f"Generated {len(self.predictions)} threat predictions for proactive defense")

        # Model training status
        trained_models = sum(1 for model in ['network_anomaly', 'system_resource', 'security_event'] if model in self.models)
        insights.append(f"{trained_models}/3 AI models are trained and operational")

        # Data analysis insights
        if self.training_data['network']:
            avg_connections = statistics.mean([dp['connections'] for dp in self.training_data['network']])
            insights.append(f"Average network connections: {avg_connections:.1f} per monitoring interval")

        return insights

    def generate_ai_recommendations(self):
        """Generate AI-powered recommendations"""
        recommendations = []

        # Model training recommendations
        if 'network_anomaly' not in self.models:
            recommendations.append("Train network anomaly detection model for better threat detection")

        if 'system_resource' not in self.models:
            recommendations.append("Train system resource model to detect performance anomalies")

        # Anomaly-based recommendations
        if self.anomalies:
            high_severity = len([a for a in self.anomalies if a.get('severity') == 'high'])
            if high_severity > 0:
                recommendations.append("Review high-severity anomalies immediately")

        # Data collection recommendations
        total_data_points = sum(len(data) for data in self.training_data.values())
        if total_data_points < 100:
            recommendations.append("Collect more training data for improved AI accuracy")

        return recommendations

    def configure_ai_settings(self):
        """Configure AI settings"""
        print("=== AI Configuration ===")
        print("Current settings:")
        print("- Models are automatically trained on available data")
        print("- Anomaly detection uses statistical analysis")
        print("- Predictions are based on pattern recognition")

        print("\nAI configuration options would be implemented here.")
        print("This could include:")
        print("- Model sensitivity settings")
        print("- Training data retention policies")
        print("- Alert thresholds")
        print("- Prediction confidence levels")

    def view_anomalies(self):
        """View detected anomalies"""
        print("=== Detected Anomalies ===")

        if not self.anomalies:
            print("No anomalies detected yet.")
            print("Run anomaly detection or train models to get started.")
            return

        print(f"Total anomalies: {len(self.anomalies)}")

        # Group by type
        by_type = defaultdict(list)
        for anomaly in self.anomalies:
            by_type[anomaly['type']].append(anomaly)

        for anomaly_type, anomalies in by_type.items():
            print(f"\n{anomaly_type.upper()} Anomalies ({len(anomalies)}):")
            for anomaly in anomalies[-5:]:  # Show last 5
                print(f"• {anomaly['description']} (confidence: {anomaly['confidence']:.2f})")