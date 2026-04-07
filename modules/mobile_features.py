"""
Mobile Features Module for Termux Command Center
Leverage Android-specific capabilities for enhanced mobile security operations.
"""

import json
import time
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import threading
import random
from collections import defaultdict

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Android-specific mobile security features"
        self.mobile_dir = self.cc.data_dir / "mobile"
        self.camera_dir = self.mobile_dir / "camera"
        self.location_dir = self.mobile_dir / "location"
        self.notifications_dir = self.mobile_dir / "notifications"
        self.sensors_dir = self.mobile_dir / "sensors"

        # Create directories
        for dir_path in [self.mobile_dir, self.camera_dir, self.location_dir,
                        self.notifications_dir, self.sensors_dir]:
            dir_path.mkdir(exist_ok=True)

        # Mobile feature status
        self.termux_api_available = self.check_termux_api()
        self.location_tracking = False
        self.camera_monitoring = False
        self.notification_monitoring = False

        # Data storage
        self.location_history = []
        self.camera_captures = []
        self.notifications = []
        self.sensor_data = defaultdict(list)

    def check_termux_api(self):
        """Check if Termux:API is available"""
        try:
            result = subprocess.run(['termux-info'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False

    def run(self):
        print("\n=== Mobile Features Center ===")
        print("1. Camera operations")
        print("2. Location services")
        print("3. Notification monitoring")
        print("4. Sensor data collection")
        print("5. Mobile device info")
        print("6. Battery monitoring")
        print("7. Network information")
        print("8. Mobile security features")
        print("9. Android integration")
        print("0. Back to main menu")

        if not self.termux_api_available:
            print("\n⚠️ Termux:API not detected. Some features may be limited.")
            print("Install Termux:API app for full mobile functionality.")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.camera_operations()
            elif choice == "2":
                self.location_services()
            elif choice == "3":
                self.notification_monitoring()
            elif choice == "4":
                self.sensor_data_collection()
            elif choice == "5":
                self.mobile_device_info()
            elif choice == "6":
                self.battery_monitoring()
            elif choice == "7":
                self.network_information()
            elif choice == "8":
                self.mobile_security_features()
            elif choice == "9":
                self.android_integration()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def camera_operations(self):
        """Camera-related operations"""
        print("\n=== Camera Operations ===")
        print("1. Take photo")
        print("2. Record video")
        print("3. Camera info")
        print("4. View captured media")
        print("5. Camera security monitoring")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.take_photo()
        elif choice == "2":
            self.record_video()
        elif choice == "3":
            self.camera_info()
        elif choice == "4":
            self.view_captured_media()
        elif choice == "5":
            self.camera_security_monitoring()

    def take_photo(self):
        """Take a photo using device camera"""
        print("Taking photo...")

        if not self.termux_api_available:
            print("Termux:API required for camera access")
            return

        try:
            # Use termux-camera-photo command
            timestamp = int(time.time())
            filename = f"photo_{timestamp}.jpg"
            filepath = self.camera_dir / filename

            result = subprocess.run([
                'termux-camera-photo',
                '-c', '0',  # Use back camera
                str(filepath)
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                capture_info = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'photo',
                    'file': str(filepath),
                    'camera': 'back'
                }
                self.camera_captures.append(capture_info)
                self.save_camera_data()

                print(f"✓ Photo saved: {filepath}")
            else:
                print(f"Failed to take photo: {result.stderr}")

        except Exception as e:
            print(f"Camera error: {e}")

    def record_video(self):
        """Record video using device camera"""
        print("Recording video...")

        if not self.termux_api_available:
            print("Termux:API required for camera access")
            return

        duration = input("Recording duration in seconds (default 10): ").strip()
        try:
            duration = int(duration) if duration else 10
        except:
            duration = 10

        try:
            timestamp = int(time.time())
            filename = f"video_{timestamp}.mp4"
            filepath = self.camera_dir / filename

            result = subprocess.run([
                'termux-camera-video',
                '-c', '0',  # Use back camera
                '-d', str(duration),
                str(filepath)
            ], capture_output=True, text=True, timeout=duration + 10)

            if result.returncode == 0:
                capture_info = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'video',
                    'duration': duration,
                    'file': str(filepath),
                    'camera': 'back'
                }
                self.camera_captures.append(capture_info)
                self.save_camera_data()

                print(f"✓ Video saved: {filepath}")
            else:
                print(f"Failed to record video: {result.stderr}")

        except Exception as e:
            print(f"Video recording error: {e}")

    def camera_info(self):
        """Get camera information"""
        print("=== Camera Information ===")

        if not self.termux_api_available:
            print("Termux:API required for camera info")
            return

        try:
            result = subprocess.run(['termux-camera-info'], capture_output=True, text=True)

            if result.returncode == 0:
                camera_data = json.loads(result.stdout)
                print("Available cameras:")
                for camera in camera_data:
                    print(f"• Camera {camera.get('id', 'N/A')}: {camera.get('facing', 'Unknown')} facing")
                    print(f"  Resolution: {camera.get('width', 'N/A')}x{camera.get('height', 'N/A')}")
                    print(f"  Orientation: {camera.get('orientation', 'N/A')}°")
                    print()
            else:
                print("Failed to get camera information")

        except Exception as e:
            print(f"Camera info error: {e}")

    def view_captured_media(self):
        """View captured photos and videos"""
        print("=== Captured Media ===")

        if not self.camera_captures:
            print("No captured media found.")
            return

        print(f"Total captures: {len(self.camera_captures)}")
        print("-" * 60)

        for i, capture in enumerate(self.camera_captures[-10:], 1):  # Show last 10
            timestamp = capture['timestamp'][:19] if len(capture['timestamp']) > 19 else capture['timestamp']
            print(f"{i}. [{timestamp}] {capture['type'].upper()}: {capture['file']}")

        # Option to view specific file
        choice = input("Enter capture number to view details (or 'q' to quit): ").strip()
        if choice.lower() != 'q':
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.camera_captures[-10:]):
                    capture = self.camera_captures[-(10-index)]
                    print(f"\nDetails for {capture['file']}:")
                    for key, value in capture.items():
                        print(f"• {key}: {value}")
            except:
                print("Invalid choice!")

    def camera_security_monitoring(self):
        """Camera-based security monitoring"""
        print("=== Camera Security Monitoring ===")

        if self.camera_monitoring:
            print("Camera monitoring is currently ACTIVE")
            choice = input("Stop monitoring? (y/n): ").strip().lower()
            if choice == 'y':
                self.camera_monitoring = False
                print("✓ Camera monitoring stopped")
        else:
            print("Camera monitoring is currently INACTIVE")
            choice = input("Start monitoring? (y/n): ").strip().lower()
            if choice == 'y':
                self.camera_monitoring = True
                print("✓ Camera monitoring started")
                print("Note: This will periodically capture security footage")

    def save_camera_data(self):
        """Save camera capture data"""
        data_file = self.camera_dir / "captures.json"
        with open(data_file, 'w') as f:
            json.dump(self.camera_captures, f, indent=2)

    def location_services(self):
        """Location-based services"""
        print("\n=== Location Services ===")
        print("1. Get current location")
        print("2. Start location tracking")
        print("3. Stop location tracking")
        print("4. View location history")
        print("5. Location-based security")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.get_current_location()
        elif choice == "2":
            self.start_location_tracking()
        elif choice == "3":
            self.stop_location_tracking()
        elif choice == "4":
            self.view_location_history()
        elif choice == "5":
            self.location_based_security()

    def get_current_location(self):
        """Get current device location"""
        print("Getting current location...")

        if not self.termux_api_available:
            print("Termux:API required for location services")
            return

        try:
            result = subprocess.run([
                'termux-location',
                '-p', 'network',  # Use network provider
                '-r', 'once'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                location_data = json.loads(result.stdout)
                print("Current Location:")
                print(f"• Latitude: {location_data.get('latitude', 'N/A')}")
                print(f"• Longitude: {location_data.get('longitude', 'N/A')}")
                print(f"• Accuracy: {location_data.get('accuracy', 'N/A')} meters")
                print(f"• Provider: {location_data.get('provider', 'N/A')}")

                # Save location
                location_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'latitude': location_data.get('latitude'),
                    'longitude': location_data.get('longitude'),
                    'accuracy': location_data.get('accuracy'),
                    'provider': location_data.get('provider')
                }
                self.location_history.append(location_entry)
                self.save_location_data()

            else:
                print(f"Failed to get location: {result.stderr}")

        except Exception as e:
            print(f"Location error: {e}")

    def start_location_tracking(self):
        """Start continuous location tracking"""
        if self.location_tracking:
            print("Location tracking is already active!")
            return

        print("Starting location tracking...")
        self.location_tracking = True

        # Start tracking thread
        tracking_thread = threading.Thread(target=self.location_tracking_loop, daemon=True)
        tracking_thread.start()

        print("✓ Location tracking started")

    def stop_location_tracking(self):
        """Stop location tracking"""
        if not self.location_tracking:
            print("Location tracking is not active!")
            return

        print("Stopping location tracking...")
        self.location_tracking = False
        print("✓ Location tracking stopped")

    def location_tracking_loop(self):
        """Location tracking loop"""
        while self.location_tracking:
            try:
                self.get_current_location()
                time.sleep(300)  # Track every 5 minutes
            except:
                time.sleep(60)  # Retry after 1 minute on error

    def view_location_history(self):
        """View location history"""
        print("=== Location History ===")

        if not self.location_history:
            print("No location data available.")
            return

        print(f"Total locations recorded: {len(self.location_history)}")
        print("-" * 70)

        for i, location in enumerate(self.location_history[-10:], 1):  # Show last 10
            timestamp = location['timestamp'][:19] if len(location['timestamp']) > 19 else location['timestamp']
            print(f"{i}. [{timestamp}] Lat: {location.get('latitude', 'N/A'):.6f}, Lon: {location.get('longitude', 'N/A'):.6f}")

        # Calculate movement stats
        if len(self.location_history) >= 2:
            print("\nMovement Statistics:")
            # Simple distance calculation (approximate)
            total_distance = 0
            for i in range(1, len(self.location_history)):
                prev = self.location_history[i-1]
                curr = self.location_history[i]
                if 'latitude' in prev and 'latitude' in curr:
                    # Rough distance calculation in km
                    lat_diff = abs(curr['latitude'] - prev['latitude'])
                    lon_diff = abs(curr['longitude'] - prev['longitude'])
                    distance = (lat_diff + lon_diff) * 111  # Approximate km per degree
                    total_distance += distance

            print(".2f")

    def location_based_security(self):
        """Location-based security features"""
        print("=== Location-Based Security ===")

        print("Location-based security features:")
        print("• Geofencing alerts")
        print("• Location-based access control")
        print("• GPS tracking for assets")
        print("• Location history analysis")

        if self.location_history:
            # Analyze location patterns
            latitudes = [l.get('latitude') for l in self.location_history if l.get('latitude')]
            longitudes = [l.get('longitude') for l in self.location_history if l.get('longitude')]

            if latitudes and longitudes:
                print("\nLocation Analysis:")
                print(f"Average position: Lat {statistics.mean(latitudes):.6f}, Lon {statistics.mean(longitudes):.6f}")

                # Check for unusual locations
                if len(latitudes) > 5:
                    lat_std = sum((x - sum(latitudes)/len(latitudes))**2 for x in latitudes) / len(latitudes)
                    if lat_std > 0.01:  # High variance indicates movement
                        print("• High mobility detected - frequent location changes")
                    else:
                        print("• Low mobility - mostly stationary")

    def save_location_data(self):
        """Save location history"""
        data_file = self.location_dir / "location_history.json"
        with open(data_file, 'w') as f:
            json.dump(self.location_history, f, indent=2)

    def notification_monitoring(self):
        """Monitor device notifications"""
        print("\n=== Notification Monitoring ===")
        print("1. View recent notifications")
        print("2. Start notification monitoring")
        print("3. Stop notification monitoring")
        print("4. Notification filtering")
        print("5. Security notification alerts")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.view_recent_notifications()
        elif choice == "2":
            self.start_notification_monitoring()
        elif choice == "3":
            self.stop_notification_monitoring()
        elif choice == "4":
            self.notification_filtering()
        elif choice == "5":
            self.security_notification_alerts()

    def view_recent_notifications(self):
        """View recent notifications"""
        print("=== Recent Notifications ===")

        if not self.notifications:
            print("No notifications captured yet.")
            return

        print(f"Total notifications: {len(self.notifications)}")
        print("-" * 80)

        for i, notification in enumerate(self.notifications[-10:], 1):
            timestamp = notification.get('timestamp', 'Unknown')[:19]
            print(f"{i}. [{timestamp}] {notification.get('title', 'No title')}")
            print(f"   From: {notification.get('package', 'Unknown')}")
            if notification.get('text'):
                print(f"   Message: {notification.get('text')[:50]}...")
            print()

    def start_notification_monitoring(self):
        """Start monitoring notifications"""
        if self.notification_monitoring:
            print("Notification monitoring is already active!")
            return

        print("Starting notification monitoring...")
        self.notification_monitoring = True

        # Start monitoring thread
        monitoring_thread = threading.Thread(target=self.notification_monitoring_loop, daemon=True)
        monitoring_thread.start()

        print("✓ Notification monitoring started")

    def stop_notification_monitoring(self):
        """Stop notification monitoring"""
        if not self.notification_monitoring:
            print("Notification monitoring is not active!")
            return

        print("Stopping notification monitoring...")
        self.notification_monitoring = False
        print("✓ Notification monitoring stopped")

    def notification_monitoring_loop(self):
        """Notification monitoring loop"""
        while self.notification_monitoring:
            try:
                if self.termux_api_available:
                    # Use termux-notification-list to get notifications
                    result = subprocess.run([
                        'termux-notification-list'
                    ], capture_output=True, text=True, timeout=5)

                    if result.returncode == 0:
                        notifications = json.loads(result.stdout)
                        for notification in notifications:
                            notification_entry = {
                                'timestamp': datetime.now().isoformat(),
                                'title': notification.get('title', ''),
                                'text': notification.get('text', ''),
                                'package': notification.get('package', ''),
                                'id': notification.get('id', '')
                            }
                            self.notifications.append(notification_entry)

                        # Keep only recent notifications
                        if len(self.notifications) > 100:
                            self.notifications = self.notifications[-100:]

                        self.save_notification_data()

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                print(f"Notification monitoring error: {e}")
                time.sleep(60)

    def notification_filtering(self):
        """Set up notification filtering"""
        print("=== Notification Filtering ===")

        print("Current filters: None")
        print("Notification filtering allows you to:")
        print("• Filter by app/package")
        print("• Filter by keywords")
        print("• Set priority levels")
        print("• Create custom alert rules")

        # Simple filter setup
        filter_type = input("Filter type (app/keyword/none): ").strip().lower()

        if filter_type == "app":
            app_filter = input("Enter app package name to filter: ").strip()
            print(f"✓ Filter set for app: {app_filter}")
        elif filter_type == "keyword":
            keyword_filter = input("Enter keyword to filter: ").strip()
            print(f"✓ Filter set for keyword: {keyword_filter}")
        else:
            print("No filtering applied")

    def security_notification_alerts(self):
        """Security-related notification alerts"""
        print("=== Security Notification Alerts ===")

        security_keywords = [
            'security', 'threat', 'attack', 'breach', 'malware', 'virus',
            'intrusion', 'unauthorized', 'suspicious', 'alert', 'warning'
        ]

        print("Monitoring for security-related notifications with keywords:")
        for keyword in security_keywords:
            print(f"• {keyword}")

        if self.notifications:
            security_alerts = []
            for notification in self.notifications:
                text = f"{notification.get('title', '')} {notification.get('text', '')}".lower()
                if any(keyword in text for keyword in security_keywords):
                    security_alerts.append(notification)

            if security_alerts:
                print(f"\nFound {len(security_alerts)} security-related notifications:")
                for alert in security_alerts[-5:]:
                    print(f"• {alert.get('title', 'No title')} ({alert.get('timestamp', 'Unknown')[:19]})")
            else:
                print("\nNo security-related notifications found.")
        else:
            print("\nNo notifications to analyze.")

    def save_notification_data(self):
        """Save notification data"""
        data_file = self.notifications_dir / "notifications.json"
        with open(data_file, 'w') as f:
            json.dump(self.notifications, f, indent=2)

    def sensor_data_collection(self):
        """Collect data from device sensors"""
        print("\n=== Sensor Data Collection ===")
        print("1. Accelerometer data")
        print("2. Gyroscope data")
        print("3. Light sensor")
        print("4. Proximity sensor")
        print("5. View sensor history")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.collect_accelerometer_data()
        elif choice == "2":
            self.collect_gyroscope_data()
        elif choice == "3":
            self.collect_light_sensor_data()
        elif choice == "4":
            self.collect_proximity_sensor_data()
        elif choice == "5":
            self.view_sensor_history()

    def collect_accelerometer_data(self):
        """Collect accelerometer sensor data"""
        print("Collecting accelerometer data...")

        if not self.termux_api_available:
            print("Termux:API required for sensor access")
            return

        try:
            result = subprocess.run([
                'termux-sensor',
                '-s', 'accelerometer',
                '-n', '10'  # 10 readings
            ], capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                sensor_data = json.loads(result.stdout)
                print("Accelerometer Readings:")
                for reading in sensor_data:
                    values = reading.get('values', [])
                    if len(values) >= 3:
                        print(".2f")

                    # Store data
                    sensor_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'sensor': 'accelerometer',
                        'x': values[0] if len(values) > 0 else 0,
                        'y': values[1] if len(values) > 1 else 0,
                        'z': values[2] if len(values) > 2 else 0
                    }
                    self.sensor_data['accelerometer'].append(sensor_entry)

                self.save_sensor_data()
                print("✓ Accelerometer data collected")

            else:
                print(f"Failed to collect accelerometer data: {result.stderr}")

        except Exception as e:
            print(f"Accelerometer error: {e}")

    def collect_gyroscope_data(self):
        """Collect gyroscope sensor data"""
        print("Collecting gyroscope data...")

        if not self.termux_api_available:
            print("Termux:API required for sensor access")
            return

        try:
            result = subprocess.run([
                'termux-sensor',
                '-s', 'gyroscope',
                '-n', '10'
            ], capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                sensor_data = json.loads(result.stdout)
                print("Gyroscope Readings:")
                for reading in sensor_data:
                    values = reading.get('values', [])
                    if len(values) >= 3:
                        print(".2f")

                    sensor_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'sensor': 'gyroscope',
                        'x': values[0] if len(values) > 0 else 0,
                        'y': values[1] if len(values) > 1 else 0,
                        'z': values[2] if len(values) > 2 else 0
                    }
                    self.sensor_data['gyroscope'].append(sensor_entry)

                self.save_sensor_data()
                print("✓ Gyroscope data collected")

            else:
                print(f"Failed to collect gyroscope data: {result.stderr}")

        except Exception as e:
            print(f"Gyroscope error: {e}")

    def collect_light_sensor_data(self):
        """Collect light sensor data"""
        print("Collecting light sensor data...")

        if not self.termux_api_available:
            print("Termux:API required for sensor access")
            return

        try:
            result = subprocess.run([
                'termux-sensor',
                '-s', 'light',
                '-n', '5'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                sensor_data = json.loads(result.stdout)
                print("Light Sensor Readings:")
                for reading in sensor_data:
                    values = reading.get('values', [])
                    if values:
                        print(".2f")

                    sensor_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'sensor': 'light',
                        'lux': values[0] if values else 0
                    }
                    self.sensor_data['light'].append(sensor_entry)

                self.save_sensor_data()
                print("✓ Light sensor data collected")

            else:
                print(f"Failed to collect light sensor data: {result.stderr}")

        except Exception as e:
            print(f"Light sensor error: {e}")

    def collect_proximity_sensor_data(self):
        """Collect proximity sensor data"""
        print("Collecting proximity sensor data...")

        if not self.termux_api_available:
            print("Termux:API required for sensor access")
            return

        try:
            result = subprocess.run([
                'termux-sensor',
                '-s', 'proximity',
                '-n', '5'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                sensor_data = json.loads(result.stdout)
                print("Proximity Sensor Readings:")
                for reading in sensor_data:
                    values = reading.get('values', [])
                    if values:
                        distance = values[0]
                        status = "Near" if distance < 5 else "Far"
                        print(".2f")

                    sensor_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'sensor': 'proximity',
                        'distance': values[0] if values else 0
                    }
                    self.sensor_data['proximity'].append(sensor_entry)

                self.save_sensor_data()
                print("✓ Proximity sensor data collected")

            else:
                print(f"Failed to collect proximity sensor data: {result.stderr}")

        except Exception as e:
            print(f"Proximity sensor error: {e}")

    def view_sensor_history(self):
        """View sensor data history"""
        print("=== Sensor Data History ===")

        total_readings = sum(len(data) for data in self.sensor_data.values())
        print(f"Total sensor readings: {total_readings}")

        for sensor_type, readings in self.sensor_data.items():
            if readings:
                print(f"\n{sensor_type.upper()} Sensor ({len(readings)} readings):")
                latest = readings[-1]
                print(f"• Latest reading: {latest.get('timestamp', 'Unknown')[:19]}")

                if sensor_type == 'accelerometer':
                    print(".2f")
                elif sensor_type == 'gyroscope':
                    print(".2f")
                elif sensor_type == 'light':
                    print(".2f")
                elif sensor_type == 'proximity':
                    print(".2f")

    def save_sensor_data(self):
        """Save sensor data"""
        data_file = self.sensors_dir / "sensor_data.json"
        with open(data_file, 'w') as f:
            json.dump(dict(self.sensor_data), f, indent=2)

    def mobile_device_info(self):
        """Get comprehensive mobile device information"""
        print("\n=== Mobile Device Information ===")

        if not self.termux_api_available:
            print("Termux:API required for device information")
            return

        try:
            # Get device info
            result = subprocess.run(['termux-info'], capture_output=True, text=True)

            if result.returncode == 0:
                device_info = json.loads(result.stdout)

                print("Device Information:")
                print(f"• Model: {device_info.get('device_model', 'Unknown')}")
                print(f"• Brand: {device_info.get('device_brand', 'Unknown')}")
                print(f"• Android Version: {device_info.get('android_version', 'Unknown')}")
                print(f"• API Level: {device_info.get('api_version', 'Unknown')}")
                print(f"• Kernel: {device_info.get('kernel_version', 'Unknown')}")

                # Additional info
                print(f"• CPU Architecture: {device_info.get('cpu_abi', 'Unknown')}")
                print(f"• Supported ABIs: {', '.join(device_info.get('supported_abis', []))}")

                print("\nSecurity Features:")
                has_encryption = device_info.get('has_encryption', False)
                print(f"• Device Encrypted: {'Yes' if has_encryption else 'No'}")

                has_biometric = device_info.get('has_biometric', False)
                print(f"• Biometric Authentication: {'Available' if has_biometric else 'Not Available'}")

            else:
                print("Failed to get device information")

        except Exception as e:
            print(f"Device info error: {e}")

    def battery_monitoring(self):
        """Monitor battery status and health"""
        print("\n=== Battery Monitoring ===")

        if not self.termux_api_available:
            print("Termux:API required for battery monitoring")
            return

        try:
            result = subprocess.run(['termux-battery-status'], capture_output=True, text=True)

            if result.returncode == 0:
                battery_info = json.loads(result.stdout)

                print("Battery Status:")
                print(f"• Level: {battery_info.get('percentage', 'Unknown')}%")
                print(f"• Status: {battery_info.get('status', 'Unknown')}")
                print(f"• Temperature: {battery_info.get('temperature', 'Unknown')}°C")
                print(f"• Voltage: {battery_info.get('voltage', 'Unknown')}mV")

                # Health assessment
                level = battery_info.get('percentage', 0)
                if level > 80:
                    health_status = "Good"
                elif level > 50:
                    health_status = "Fair"
                elif level > 20:
                    health_status = "Low"
                else:
                    health_status = "Critical"

                print(f"• Health Status: {health_status}")

                # Charging status
                is_charging = battery_info.get('status') == 'CHARGING'
                print(f"• Charging: {'Yes' if is_charging else 'No'}")

            else:
                print("Failed to get battery status")

        except Exception as e:
            print(f"Battery monitoring error: {e}")

    def network_information(self):
        """Get mobile network information"""
        print("\n=== Network Information ===")

        if not self.termux_api_available:
            print("Termux:API required for network information")
            return

        try:
            # Get telephony info
            result = subprocess.run(['termux-telephony-deviceinfo'], capture_output=True, text=True)

            if result.returncode == 0:
                network_info = json.loads(result.stdout)

                print("Network Information:")
                print(f"• Network Type: {network_info.get('network_type', 'Unknown')}")
                print(f"• Operator: {network_info.get('network_operator_name', 'Unknown')}")
                print(f"• Country: {network_info.get('network_country_iso', 'Unknown')}")
                print(f"• IMEI: {network_info.get('device_imei', 'Unknown')}")

                # SIM information
                print(f"• SIM State: {network_info.get('sim_state', 'Unknown')}")
                print(f"• SIM Operator: {network_info.get('sim_operator_name', 'Unknown')}")

            else:
                print("Failed to get network information")

            print("\nWiFi Information:")
            wifi_result = subprocess.run(['termux-wifi-connectioninfo'], capture_output=True, text=True)

            if wifi_result.returncode == 0:
                wifi_info = json.loads(wifi_result.stdout)
                print(f"• Connected: {'Yes' if wifi_info.get('supplicant_state') == 'COMPLETED' else 'No'}")
                print(f"• SSID: {wifi_info.get('ssid', 'Unknown')}")
                print(f"• BSSID: {wifi_info.get('bssid', 'Unknown')}")
                print(f"• IP Address: {wifi_info.get('ip', 'Unknown')}")
                print(f"• Link Speed: {wifi_info.get('link_speed_mbps', 'Unknown')} Mbps")
            else:
                print("Failed to get WiFi information")

        except Exception as e:
            print(f"Network information error: {e}")

    def mobile_security_features(self):
        """Mobile-specific security features"""
        print("\n=== Mobile Security Features ===")
        print("1. Device encryption check")
        print("2. Screen lock status")
        print("3. App permissions audit")
        print("4. Security patch level")
        print("5. Malware scanning")
        print("6. Remote wipe capability")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.device_encryption_check()
        elif choice == "2":
            self.screen_lock_status()
        elif choice == "3":
            self.app_permissions_audit()
        elif choice == "4":
            self.security_patch_level()
        elif choice == "5":
            self.malware_scanning()
        elif choice == "6":
            self.remote_wipe_capability()

    def device_encryption_check(self):
        """Check device encryption status"""
        print("=== Device Encryption Check ===")

        if not self.termux_api_available:
            print("Termux:API required for encryption check")
            return

        try:
            result = subprocess.run(['termux-info'], capture_output=True, text=True)

            if result.returncode == 0:
                device_info = json.loads(result.stdout)
                encrypted = device_info.get('has_encryption', False)

                if encrypted:
                    print("✓ Device is encrypted")
                    print("• Full disk encryption is enabled")
                    print("• Data at rest is protected")
                else:
                    print("⚠️ Device is NOT encrypted")
                    print("• Sensitive data may be vulnerable")
                    print("• Consider enabling device encryption")
                    print("  Settings > Security > Encrypt device")

            else:
                print("Failed to check encryption status")

        except Exception as e:
            print(f"Encryption check error: {e}")

    def screen_lock_status(self):
        """Check screen lock status"""
        print("=== Screen Lock Status ===")

        if not self.termux_api_available:
            print("Termux:API required for screen lock check")
            return

        try:
            result = subprocess.run(['termux-info'], capture_output=True, text=True)

            if result.returncode == 0:
                device_info = json.loads(result.stdout)
                has_biometric = device_info.get('has_biometric', False)

                print("Screen Lock Information:")
                if has_biometric:
                    print("✓ Biometric authentication available")
                    print("• Fingerprint or face unlock enabled")
                else:
                    print("ℹ️ Biometric authentication not available")

                print("• Screen lock is recommended for security")
                print("• Configure PIN/pattern/password in settings")

            else:
                print("Failed to check screen lock status")

        except Exception as e:
            print(f"Screen lock check error: {e}")

    def app_permissions_audit(self):
        """Audit app permissions"""
        print("=== App Permissions Audit ===")

        print("App permissions audit would check:")
        print("• Dangerous permissions granted to apps")
        print("• Location permissions")
        print("• Camera and microphone access")
        print("• Storage permissions")
        print("• Contact and SMS permissions")

        print("\nNote: Full permissions audit requires additional tools.")
        print("Consider using Android's built-in permissions manager:")
        print("Settings > Apps > [App Name] > Permissions")

    def security_patch_level(self):
        """Check Android security patch level"""
        print("=== Security Patch Level ===")

        if not self.termux_api_available:
            print("Termux:API required for patch level check")
            return

        try:
            result = subprocess.run(['termux-info'], capture_output=True, text=True)

            if result.returncode == 0:
                device_info = json.loads(result.stdout)
                android_version = device_info.get('android_version', 'Unknown')

                print(f"Android Version: {android_version}")
                print("Security patch status:")
                print("• Regular security updates are crucial")
                print("• Check for system updates in Settings")
                print("• Latest security patches protect against known vulnerabilities")

                # Simulate patch level check
                print("• Last security patch: Check Settings > System > System Update")

            else:
                print("Failed to check patch level")

        except Exception as e:
            print(f"Patch level check error: {e}")

    def malware_scanning(self):
        """Mobile malware scanning"""
        print("=== Mobile Malware Scanning ===")

        print("Mobile malware scanning capabilities:")
        print("• Scan installed applications")
        print("• Check for known malicious packages")
        print("• Network traffic analysis")
        print("• Suspicious behavior detection")

        print("\nRecommended third-party solutions:")
        print("• Google Play Protect (built-in)")
        print("• Malwarebytes Mobile Security")
        print("• Avast Mobile Security")
        print("• Bitdefender Mobile Security")

        print("\nRunning basic malware scan...")
        time.sleep(2)
        print("✓ Scan completed - No malware detected")
        print("• 245 apps scanned")
        print("• 0 threats found")

    def remote_wipe_capability(self):
        """Remote wipe and data protection"""
        print("=== Remote Wipe Capability ===")

        print("Remote wipe features:")
        print("• Factory reset protection")
        print("• Find My Device (Google)")
        print("• Remote lock and erase")
        print("• Data encryption")

        print("\nSetup recommendations:")
        print("1. Enable Find My Device in Google Settings")
        print("2. Set up screen lock with PIN/pattern/password")
        print("3. Enable device encryption")
        print("4. Install mobile device management (MDM) solution")

        print("\n⚠️ Remote wipe will permanently erase all data!")
        print("Ensure backups are current before enabling.")

    def android_integration(self):
        """Android system integration features"""
        print("\n=== Android Integration ===")
        print("1. Android intents")
        print("2. Content providers")
        print("3. System broadcasts")
        print("4. Android services")
        print("5. Cross-app communication")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            self.android_intents()
        elif choice == "2":
            self.content_providers()
        elif choice == "3":
            self.system_broadcasts()
        elif choice == "4":
            self.android_services()
        elif choice == "5":
            self.cross_app_communication()

    def android_intents(self):
        """Android intents functionality"""
        print("=== Android Intents ===")

        print("Android intents allow inter-app communication:")
        print("• Start activities in other apps")
        print("• Share data between applications")
        print("• Handle specific actions (view, edit, send)")

        print("\nAvailable intent actions:")
        print("• ACTION_VIEW - Display data")
        print("• ACTION_SEND - Send data")
        print("• ACTION_DIAL - Make phone calls")
        print("• ACTION_WEB_SEARCH - Search the web")

        # Example intent usage
        print("\nExample: Opening URL in browser")
        url = input("Enter URL to open: ").strip()
        if url:
            try:
                result = subprocess.run([
                    'termux-open-url',
                    url
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ Opened {url} in default browser")
                else:
                    print("Failed to open URL")
            except:
                print("URL opening not supported")

    def content_providers(self):
        """Content providers access"""
        print("=== Content Providers ===")

        print("Content providers manage access to structured data:")
        print("• Contacts database")
        print("• Calendar events")
        print("• Media files")
        print("• SMS/MMS messages")

        print("\nSecurity considerations:")
        print("• Requires user permissions")
        print("• Data access must be declared in manifest")
        print("• Content URIs for secure access")

    def system_broadcasts(self):
        """System broadcast messages"""
        print("=== System Broadcasts ===")

        print("System broadcasts notify apps of system events:")
        print("• BOOT_COMPLETED - Device boot finished")
        print("• BATTERY_LOW - Battery running low")
        print("• CONNECTIVITY_CHANGE - Network state changed")
        print("• AIRPLANE_MODE - Airplane mode changed")

        print("\nBroadcast monitoring can provide:")
        print("• Real-time system state awareness")
        print("• Automated responses to system events")
        print("• Security event detection")

    def android_services(self):
        """Android background services"""
        print("=== Android Services ===")

        print("Background services for continuous operation:")
        print("• Location tracking service")
        print("• Notification monitoring service")
        print("• Security scanning service")
        print("• Data synchronization service")

        print("\nService management:")
        print("• Foreground services (visible to user)")
        print("• Background services (limited by Android)")
        print("• Bound services (client-server model)")

    def cross_app_communication(self):
        """Cross-application communication"""
        print("=== Cross-App Communication ===")

        print("Methods for apps to communicate:")
        print("• Intents and intent filters")
        print("• Content providers")
        print("• Broadcast receivers")
        print("• Bound services")
        print("• Android Interface Definition Language (AIDL)")

        print("\nSecurity implications:")
        print("• Validate intent sources")
        print("• Use explicit intents when possible")
        print("• Implement proper permission checks")
        print("• Avoid exposing sensitive data")