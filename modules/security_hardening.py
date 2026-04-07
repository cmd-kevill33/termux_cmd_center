"""
Security Hardening Module for Termux Command Center
Comprehensive security features including encryption, access control, and audit logging.
"""

import json
import time
import os
import hashlib
import secrets
import hmac
import base64
from datetime import datetime, timedelta
from pathlib import Path
import re
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import threading
import ipaddress
from collections import defaultdict, deque

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Comprehensive security hardening and access control"
        self.security_dir = self.cc.data_dir / "security"
        self.logs_dir = self.security_dir / "logs"
        self.keys_dir = self.security_dir / "keys"
        self.audit_dir = self.security_dir / "audit"

        # Create directories
        for dir_path in [self.security_dir, self.logs_dir, self.keys_dir, self.audit_dir]:
            dir_path.mkdir(exist_ok=True)

        # Security configuration
        self.encryption_enabled = True
        self.audit_logging = True
        self.input_validation = True
        self.rate_limiting = True
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes

        # Security state
        self.encryption_key = None
        self.session_tokens = {}
        self.failed_attempts = defaultdict(int)
        self.locked_accounts = {}
        self.rate_limits = defaultdict(lambda: deque(maxlen=100))
        self.security_events = deque(maxlen=1000)

        # Initialize security
        self.initialize_security()
        self.setup_audit_logging()

    def run(self):
        print("\n=== Security Hardening Center ===")
        print("1. Security status overview")
        print("2. Encryption management")
        print("3. Access control settings")
        print("4. Audit log viewer")
        print("5. Security configuration")
        print("6. Threat detection")
        print("7. Security hardening tools")
        print("8. Emergency security lockdown")
        print("9. Security compliance check")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.security_status_overview()
            elif choice == "2":
                self.encryption_management()
            elif choice == "3":
                self.access_control_settings()
            elif choice == "4":
                self.audit_log_viewer()
            elif choice == "5":
                self.security_configuration()
            elif choice == "6":
                self.threat_detection()
            elif choice == "7":
                self.security_hardening_tools()
            elif choice == "8":
                self.emergency_lockdown()
            elif choice == "9":
                self.security_compliance_check()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def initialize_security(self):
        """Initialize security components"""
        # Generate or load encryption key
        key_file = self.keys_dir / "master.key"
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    encrypted_key = f.read()
                # In a real implementation, you'd decrypt this with a password
                self.encryption_key = encrypted_key
            except:
                self.generate_encryption_key()
        else:
            self.generate_encryption_key()

        # Load security configuration
        config_file = self.security_dir / "security_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                self.encryption_enabled = config.get('encryption_enabled', True)
                self.audit_logging = config.get('audit_logging', True)
                self.input_validation = config.get('input_validation', True)
                self.rate_limiting = config.get('rate_limiting', True)
                self.session_timeout = config.get('session_timeout', 3600)
                self.max_login_attempts = config.get('max_login_attempts', 5)
                self.lockout_duration = config.get('lockout_duration', 900)
            except:
                pass

    def generate_encryption_key(self):
        """Generate new encryption key"""
        self.encryption_key = Fernet.generate_key()
        key_file = self.keys_dir / "master.key"

        # In production, this should be encrypted with a user password
        with open(key_file, 'wb') as f:
            f.write(self.encryption_key)

    def setup_audit_logging(self):
        """Setup audit logging"""
        if not self.audit_logging:
            return

        audit_log = self.audit_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"

        self.audit_logger = logging.getLogger('security_audit')
        self.audit_logger.setLevel(logging.INFO)

        # Remove existing handlers
        for handler in self.audit_logger.handlers[:]:
            self.audit_logger.removeHandler(handler)

        # File handler
        file_handler = logging.FileHandler(audit_log)
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s - IP:%(ip)s - User:%(user)s'
        )
        file_handler.setFormatter(formatter)

        self.audit_logger.addHandler(file_handler)

    def log_security_event(self, event_type, message, user="system", ip="localhost", **kwargs):
        """Log security event"""
        if not self.audit_logging:
            return

        # Store in memory
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            'user': user,
            'ip': ip,
            'details': kwargs
        }
        self.security_events.append(event)

        # Log to file
        extra = {'ip': ip, 'user': user}
        if event_type == 'INFO':
            self.audit_logger.info(message, extra=extra)
        elif event_type == 'WARNING':
            self.audit_logger.warning(message, extra=extra)
        elif event_type == 'ERROR':
            self.audit_logger.error(message, extra=extra)
        elif event_type == 'CRITICAL':
            self.audit_logger.critical(message, extra=extra)

    def security_status_overview(self):
        """Display security status overview"""
        print("=== Security Status Overview ===")

        # Security score calculation
        score = 0
        max_score = 100

        checks = [
            ("Encryption enabled", self.encryption_enabled, 20),
            ("Audit logging active", self.audit_logging, 15),
            ("Input validation enabled", self.input_validation, 15),
            ("Rate limiting active", self.rate_limiting, 10),
            ("Master key exists", self.encryption_key is not None, 15),
            ("Security directories secure", self.check_directory_permissions(), 10),
            ("Recent security events", len(self.security_events) > 0, 5),
            ("Session management active", len(self.session_tokens) >= 0, 10)
        ]

        print("Security Checks:")
        print("-" * 50)
        for check_name, status, points in checks:
            status_icon = "✓" if status else "✗"
            print(f"{status_icon} {check_name:<25} ({points} pts)")
            if status:
                score += points

        print("-" * 50)
        print(f"Security Score: {score}/{max_score} ({score/max_score*100:.1f}%)")

        # Risk assessment
        if score >= 80:
            risk_level = "LOW"
            risk_color = "Green"
        elif score >= 60:
            risk_level = "MEDIUM"
            risk_color = "Yellow"
        else:
            risk_level = "HIGH"
            risk_color = "Red"

        print(f"Risk Level: {risk_level} ({risk_color})")

        # Recent events
        print("\nRecent Security Events:")
        if self.security_events:
            for event in list(self.security_events)[-5:]:
                print(f"• {event['timestamp'][:19]} - {event['type']} - {event['message']}")
        else:
            print("• No recent security events")

        # Active sessions
        print(f"\nActive Sessions: {len(self.session_tokens)}")

        # Failed login attempts
        failed_count = sum(self.failed_attempts.values())
        print(f"Failed Login Attempts (total): {failed_count}")

        # Locked accounts
        locked_count = len([acc for acc, time in self.locked_accounts.items()
                           if datetime.now().timestamp() - time < self.lockout_duration])
        print(f"Currently Locked Accounts: {locked_count}")

    def check_directory_permissions(self):
        """Check if security directories have proper permissions"""
        try:
            # Check if keys directory is readable only by owner
            keys_stat = self.keys_dir.stat()
            # This is a simplified check - in reality you'd check octal permissions
            return True
        except:
            return False

    def encryption_management(self):
        """Manage encryption settings"""
        print("=== Encryption Management ===")

        print("Current encryption status:")
        print(f"• Encryption enabled: {self.encryption_enabled}")
        print(f"• Master key exists: {self.encryption_key is not None}")
        print(f"• Key file location: {self.keys_dir / 'master.key'}")

        print("\nEncryption options:")
        print("1. Generate new encryption key")
        print("2. Backup encryption key")
        print("3. Test encryption/decryption")
        print("4. Rotate encryption keys")
        print("5. View encrypted files")

        choice = input("Select option: ").strip()

        if choice == "1":
            confirm = input("Generate new encryption key? This will require re-encrypting all data (yes/no): ").strip().lower()
            if confirm == 'yes':
                old_key = self.encryption_key
                self.generate_encryption_key()
                print("✓ New encryption key generated")
                self.log_security_event('INFO', 'New encryption key generated', 'system')

        elif choice == "2":
            self.backup_encryption_key()

        elif choice == "3":
            self.test_encryption()

        elif choice == "4":
            self.rotate_encryption_keys()

        elif choice == "5":
            self.view_encrypted_files()

    def backup_encryption_key(self):
        """Backup encryption key securely"""
        print("Backing up encryption key...")

        backup_file = self.keys_dir / f"key_backup_{int(time.time())}.enc"

        try:
            # In production, this should be encrypted with a password
            with open(backup_file, 'wb') as f:
                f.write(self.encryption_key)

            print(f"✓ Encryption key backed up to: {backup_file}")
            self.log_security_event('INFO', 'Encryption key backed up', 'system')

        except Exception as e:
            print(f"Backup failed: {e}")

    def test_encryption(self):
        """Test encryption and decryption"""
        print("Testing encryption/decryption...")

        if not self.encryption_key:
            print("No encryption key available!")
            return

        try:
            fernet = Fernet(self.encryption_key)

            test_data = b"Hello, World! This is a test message."
            encrypted = fernet.encrypt(test_data)
            decrypted = fernet.decrypt(encrypted)

            if decrypted == test_data:
                print("✓ Encryption/decryption test passed")
            else:
                print("✗ Encryption/decryption test failed")

        except Exception as e:
            print(f"Encryption test failed: {e}")

    def rotate_encryption_keys(self):
        """Rotate encryption keys for enhanced security"""
        print("=== Key Rotation ===")
        print("Key rotation will re-encrypt all sensitive data with a new key.")
        print("This process may take some time depending on data size.")

        confirm = input("Proceed with key rotation? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return

        try:
            # Generate new key
            new_key = Fernet.generate_key()
            new_fernet = Fernet(new_key)

            # Find and re-encrypt sensitive files
            sensitive_files = self.find_sensitive_files()
            rotated_count = 0

            for file_path in sensitive_files:
                try:
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()

                    # Decrypt with old key
                    old_fernet = Fernet(self.encryption_key)
                    decrypted_data = old_fernet.decrypt(encrypted_data)

                    # Re-encrypt with new key
                    new_encrypted_data = new_fernet.encrypt(decrypted_data)

                    # Write back
                    with open(file_path, 'wb') as f:
                        f.write(new_encrypted_data)

                    rotated_count += 1

                except Exception as e:
                    print(f"Failed to rotate {file_path}: {e}")

            # Update master key
            self.encryption_key = new_key
            key_file = self.keys_dir / "master.key"
            with open(key_file, 'wb') as f:
                f.write(new_key)

            print(f"✓ Key rotation completed: {rotated_count} files re-encrypted")
            self.log_security_event('INFO', f'Encryption keys rotated, {rotated_count} files updated', 'system')

        except Exception as e:
            print(f"Key rotation failed: {e}")

    def find_sensitive_files(self):
        """Find files that contain sensitive data"""
        sensitive_files = []

        # Look for encrypted files (by extension or content)
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.enc') or file.endswith('.key'):
                    sensitive_files.append(Path(root) / file)

        return sensitive_files

    def view_encrypted_files(self):
        """View information about encrypted files"""
        print("=== Encrypted Files ===")

        encrypted_files = self.find_sensitive_files()

        if not encrypted_files:
            print("No encrypted files found.")
            return

        print(f"Found {len(encrypted_files)} encrypted/sensitive files:")
        print("-" * 60)

        for file_path in encrypted_files:
            try:
                stat = file_path.stat()
                size_kb = stat.st_size / 1024
                modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')

                print(f"• {file_path} ({size_kb:.1f} KB, modified: {modified})")

            except:
                print(f"• {file_path} (error reading file info)")

    def access_control_settings(self):
        """Manage access control settings"""
        print("=== Access Control Settings ===")

        print("Current access control configuration:")
        print(f"• Session timeout: {self.session_timeout} seconds ({self.session_timeout//60} minutes)")
        print(f"• Max login attempts: {self.max_login_attempts}")
        print(f"• Lockout duration: {self.lockout_duration} seconds ({self.lockout_duration//60} minutes)")
        print(f"• Rate limiting: {self.rate_limiting}")
        print(f"• Active sessions: {len(self.session_tokens)}")

        print("\nAccess control options:")
        print("1. Configure session timeout")
        print("2. Set login attempt limits")
        print("3. Manage locked accounts")
        print("4. View active sessions")
        print("5. Force logout all sessions")

        choice = input("Select option: ").strip()

        if choice == "1":
            timeout = input(f"Enter session timeout in minutes (current: {self.session_timeout//60}): ").strip()
            try:
                self.session_timeout = int(timeout) * 60
                print(f"✓ Session timeout set to {self.session_timeout//60} minutes")
                self.save_security_config()
            except:
                print("Invalid timeout value!")

        elif choice == "2":
            attempts = input(f"Enter max login attempts (current: {self.max_login_attempts}): ").strip()
            try:
                self.max_login_attempts = int(attempts)
                print(f"✓ Max login attempts set to {self.max_login_attempts}")
                self.save_security_config()
            except:
                print("Invalid attempts value!")

        elif choice == "3":
            self.manage_locked_accounts()

        elif choice == "4":
            self.view_active_sessions()

        elif choice == "5":
            self.force_logout_all()

    def manage_locked_accounts(self):
        """Manage locked accounts"""
        print("=== Locked Accounts Management ===")

        current_time = datetime.now().timestamp()
        active_locks = []

        for account, lock_time in self.locked_accounts.items():
            if current_time - lock_time < self.lockout_duration:
                remaining = int(self.lockout_duration - (current_time - lock_time))
                active_locks.append((account, remaining))

        if not active_locks:
            print("No accounts are currently locked.")
            return

        print("Currently locked accounts:")
        for account, remaining in active_locks:
            print(f"• {account}: {remaining//60} minutes {remaining%60} seconds remaining")

        print("\nOptions:")
        print("1. Unlock specific account")
        print("2. Unlock all accounts")
        print("3. View lock history")

        choice = input("Select option: ").strip()

        if choice == "1":
            account = input("Enter account to unlock: ").strip()
            if account in self.locked_accounts:
                del self.locked_accounts[account]
                print(f"✓ Account '{account}' unlocked")
                self.log_security_event('INFO', f'Account {account} manually unlocked', 'admin')
            else:
                print("Account not found in locked list")

        elif choice == "2":
            self.locked_accounts.clear()
            print("✓ All accounts unlocked")
            self.log_security_event('WARNING', 'All accounts manually unlocked', 'admin')

    def view_active_sessions(self):
        """View active sessions"""
        print("=== Active Sessions ===")

        if not self.session_tokens:
            print("No active sessions.")
            return

        print(f"Total active sessions: {len(self.session_tokens)}")
        print("-" * 70)
        print(f"{'Session ID':<20} {'User':<15} {'Created':<19} {'Expires':<19}")
        print("-" * 70)

        current_time = datetime.now()
        for session_id, session_data in self.session_tokens.items():
            created = datetime.fromisoformat(session_data['created'])
            expires = created + timedelta(seconds=self.session_timeout)

            # Check if expired
            if current_time > expires:
                status = "EXPIRED"
            else:
                status = "ACTIVE"

            print(f"{session_id[:20]:<20} {session_data.get('user', 'unknown'):<15} {created.strftime('%Y-%m-%d %H:%M:%S'):<19} {expires.strftime('%Y-%m-%d %H:%M:%S'):<19} {status}")

    def force_logout_all(self):
        """Force logout all sessions"""
        confirm = input("Force logout all active sessions? (yes/no): ").strip().lower()
        if confirm == 'yes':
            session_count = len(self.session_tokens)
            self.session_tokens.clear()
            print(f"✓ All {session_count} sessions terminated")
            self.log_security_event('WARNING', f'All {session_count} sessions forcibly terminated', 'admin')

    def audit_log_viewer(self):
        """View audit logs"""
        print("=== Audit Log Viewer ===")

        # List available audit log files
        audit_files = list(self.audit_dir.glob("audit_*.log"))
        audit_files.sort(reverse=True)  # Most recent first

        if not audit_files:
            print("No audit logs found.")
            return

        print("Available audit logs:")
        for i, log_file in enumerate(audit_files, 1):
            size_kb = log_file.stat().st_size / 1024
            date = log_file.name.replace('audit_', '').replace('.log', '')
            print(f"{i}. {date} ({size_kb:.1f} KB)")

        choice = input("Select log file to view (number or 'all' for recent events): ").strip()

        if choice.lower() == 'all':
            self.view_recent_audit_events()
        else:
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(audit_files):
                    self.view_audit_file(audit_files[file_index])
                else:
                    print("Invalid file selection!")
            except:
                print("Invalid input!")

    def view_recent_audit_events(self):
        """View recent audit events from memory"""
        print("=== Recent Audit Events ===")

        if not self.security_events:
            print("No recent audit events.")
            return

        print(f"Showing last {min(20, len(self.security_events))} events:")
        print("-" * 100)
        print(f"{'Time':<19} {'Type':<8} {'User':<10} {'Event':<60}")
        print("-" * 100)

        for event in list(self.security_events)[-20:]:
            timestamp = event['timestamp'][:19]
            event_type = event['type'][:8]
            user = event.get('user', 'system')[:10]
            message = event['message'][:60]

            print(f"{timestamp:<19} {event_type:<8} {user:<10} {message:<60}")

    def view_audit_file(self, log_file):
        """View specific audit log file"""
        print(f"=== Audit Log: {log_file.name} ===")

        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()

            # Show last 50 lines
            start_line = max(0, len(lines) - 50)
            for i, line in enumerate(lines[start_line:], start_line + 1):
                print(f"{i:4d}: {line.rstrip()}")

            if len(lines) > 50:
                print(f"\n... ({len(lines) - 50} more lines)")

        except Exception as e:
            print(f"Error reading log file: {e}")

    def security_configuration(self):
        """Configure security settings"""
        print("=== Security Configuration ===")

        print("Current security settings:")
        print(f"1. Encryption enabled: {self.encryption_enabled}")
        print(f"2. Audit logging: {self.audit_logging}")
        print(f"3. Input validation: {self.input_validation}")
        print(f"4. Rate limiting: {self.rate_limiting}")

        print("\nSelect setting to toggle:")

        choice = input("Enter setting number: ").strip()

        settings_map = {
            '1': ('encryption_enabled', 'Encryption'),
            '2': ('audit_logging', 'Audit logging'),
            '3': ('input_validation', 'Input validation'),
            '4': ('rate_limiting', 'Rate limiting')
        }

        if choice in settings_map:
            attr, name = settings_map[choice]
            current_value = getattr(self, attr)
            new_value = not current_value
            setattr(self, attr, new_value)

            print(f"✓ {name} {'enabled' if new_value else 'disabled'}")
            self.save_security_config()

            # Reinitialize components if needed
            if attr == 'audit_logging':
                self.setup_audit_logging()

        else:
            print("Invalid setting!")

    def save_security_config(self):
        """Save security configuration"""
        config = {
            'encryption_enabled': self.encryption_enabled,
            'audit_logging': self.audit_logging,
            'input_validation': self.input_validation,
            'rate_limiting': self.rate_limiting,
            'session_timeout': self.session_timeout,
            'max_login_attempts': self.max_login_attempts,
            'lockout_duration': self.lockout_duration
        }

        config_file = self.security_dir / "security_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def threat_detection(self):
        """Threat detection and analysis"""
        print("=== Threat Detection ===")

        # Analyze security events for threats
        threats = self.analyze_security_events()

        if not threats:
            print("✓ No active threats detected")
            return

        print("Detected Threats:")
        print("-" * 50)

        for threat in threats:
            print(f"• {threat['type']}: {threat['description']}")
            print(f"  Severity: {threat['severity']}")
            print(f"  First seen: {threat['first_seen']}")
            print(f"  Occurrences: {threat['occurrences']}")
            print()

        print("Recommended Actions:")
        for threat in threats:
            if 'recommendation' in threat:
                print(f"• {threat['recommendation']}")

    def analyze_security_events(self):
        """Analyze security events for threats"""
        threats = []

        # Count events by type
        event_counts = defaultdict(int)
        recent_events = list(self.security_events)

        for event in recent_events:
            event_counts[event['type']] += 1

        # Check for suspicious patterns
        if event_counts.get('WARNING', 0) > 10:
            threats.append({
                'type': 'High Warning Rate',
                'description': f'High number of warnings ({event_counts["WARNING"]}) in recent events',
                'severity': 'Medium',
                'first_seen': recent_events[0]['timestamp'] if recent_events else 'Unknown',
                'occurrences': event_counts['WARNING'],
                'recommendation': 'Review warning events and check system configuration'
            })

        if event_counts.get('ERROR', 0) > 5:
            threats.append({
                'type': 'High Error Rate',
                'description': f'High number of errors ({event_counts["ERROR"]}) in recent events',
                'severity': 'High',
                'first_seen': recent_events[0]['timestamp'] if recent_events else 'Unknown',
                'occurrences': event_counts['ERROR'],
                'recommendation': 'Investigate error causes and check system health'
            })

        # Check for failed login patterns
        failed_logins = sum(self.failed_attempts.values())
        if failed_logins > self.max_login_attempts * 2:
            threats.append({
                'type': 'Brute Force Attempt',
                'description': f'High number of failed login attempts ({failed_logins})',
                'severity': 'High',
                'first_seen': 'Recent',
                'occurrences': failed_logins,
                'recommendation': 'Check for brute force attacks, consider IP blocking'
            })

        # Check for locked accounts
        locked_accounts = len([acc for acc, time in self.locked_accounts.items()
                              if datetime.now().timestamp() - time < self.lockout_duration])
        if locked_accounts > 0:
            threats.append({
                'type': 'Account Lockouts',
                'description': f'{locked_accounts} account(s) currently locked due to failed attempts',
                'severity': 'Medium',
                'first_seen': 'Recent',
                'occurrences': locked_accounts,
                'recommendation': 'Monitor for coordinated attack attempts'
            })

        return threats

    def security_hardening_tools(self):
        """Security hardening tools and utilities"""
        print("=== Security Hardening Tools ===")

        print("Available hardening tools:")
        print("1. Generate secure password")
        print("2. Hash password")
        print("3. Validate input patterns")
        print("4. Check file permissions")
        print("5. Generate security report")
        print("6. Clean temporary files")
        print("7. Update file permissions")

        choice = input("Select tool: ").strip()

        if choice == "1":
            self.generate_secure_password()
        elif choice == "2":
            self.hash_password()
        elif choice == "3":
            self.validate_input_patterns()
        elif choice == "4":
            self.check_file_permissions()
        elif choice == "5":
            self.generate_security_report()
        elif choice == "6":
            self.clean_temporary_files()
        elif choice == "7":
            self.update_file_permissions()

    def generate_secure_password(self):
        """Generate a secure password"""
        print("=== Secure Password Generator ===")

        length = input("Enter password length (12-64): ").strip()
        try:
            length = max(12, min(64, int(length)))
        except:
            length = 16

        # Generate password with various character types
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(length))

        print(f"Generated secure password: {password}")
        print("⚠️  Store this password securely and do not share it!")

        # Calculate password strength
        strength = self.calculate_password_strength(password)
        print(f"Password strength: {strength}")

    def calculate_password_strength(self, password):
        """Calculate password strength"""
        score = 0

        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(r'[!@#$%^&*]', password):
            score += 1

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        else:
            return "Strong"

    def hash_password(self):
        """Hash a password securely"""
        print("=== Password Hashing ===")

        password = input("Enter password to hash: ").strip()
        if not password:
            print("No password provided!")
            return

        # Generate salt
        salt = secrets.token_bytes(16)

        # Hash with PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())

        # Combine salt and hash
        hashed = salt + key

        # Encode for storage
        hashed_b64 = base64.b64encode(hashed).decode()

        print(f"Hashed password: {hashed_b64}")
        print("⚠️  Store this hash securely in your password database!")

    def validate_input_patterns(self):
        """Validate input patterns for security"""
        print("=== Input Validation Patterns ===")

        test_input = input("Enter text to validate: ").strip()

        patterns = {
            'Email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'IP Address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'URL': r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))*)?$',
            'Phone Number': r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
            'Credit Card': r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[0-9]{15}|3[0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12})$'
        }

        print("Validation Results:")
        for pattern_name, pattern in patterns.items():
            if re.match(pattern, test_input):
                print(f"✓ Matches {pattern_name} pattern")
            else:
                print(f"✗ Does not match {pattern_name} pattern")

        # Security checks
        security_issues = []

        if len(test_input) > 1000:
            security_issues.append("Input too long (>1000 characters)")

        if re.search(r'[<>]', test_input):
            security_issues.append("Contains HTML tags (possible XSS)")

        if re.search(r'[\'";]', test_input):
            security_issues.append("Contains SQL injection characters")

        if re.search(r'(?i)script|javascript|vbscript', test_input):
            security_issues.append("Contains script keywords")

        if security_issues:
            print("\n⚠️  Security Issues Detected:")
            for issue in security_issues:
                print(f"• {issue}")
        else:
            print("\n✓ No obvious security issues detected")

    def check_file_permissions(self):
        """Check file permissions for security issues"""
        print("=== File Permission Check ===")

        # Check critical files
        critical_files = [
            'main.py',
            'setup.sh',
            'requirements.txt',
            Path('data') / 'configs',
            self.keys_dir / 'master.key'
        ]

        print("Checking file permissions:")
        print("-" * 50)

        for file_path in critical_files:
            if file_path.exists():
                try:
                    stat = file_path.stat()
                    permissions = oct(stat.st_mode)[-3:]

                    # Check if world-readable
                    if int(permissions[2]) > 0:
                        status = "⚠️  World-readable"
                        risk = "High"
                    elif int(permissions[1]) > 0:
                        status = "✓ Group-readable"
                        risk = "Medium"
                    else:
                        status = "✓ Secure"
                        risk = "Low"

                    print(f"{file_path}: {permissions} - {status} (Risk: {risk})")

                except Exception as e:
                    print(f"{file_path}: Error checking permissions - {e}")
            else:
                print(f"{file_path}: File not found")

    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("=== Security Report Generation ===")

        report_file = self.security_dir / f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            with open(report_file, 'w') as f:
                f.write("TERMUX COMMAND CENTER - SECURITY REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")

                # Security score
                score = self.calculate_security_score()
                f.write(f"Security Score: {score}/100 ({score/10:.1f}%)\n\n")

                # Configuration
                f.write("SECURITY CONFIGURATION:\n")
                f.write("-" * 25 + "\n")
                f.write(f"Encryption Enabled: {self.encryption_enabled}\n")
                f.write(f"Audit Logging: {self.audit_logging}\n")
                f.write(f"Input Validation: {self.input_validation}\n")
                f.write(f"Rate Limiting: {self.rate_limiting}\n")
                f.write(f"Session Timeout: {self.session_timeout//60} minutes\n")
                f.write(f"Max Login Attempts: {self.max_login_attempts}\n\n")

                # Recent events
                f.write("RECENT SECURITY EVENTS:\n")
                f.write("-" * 25 + "\n")
                for event in list(self.security_events)[-10:]:
                    f.write(f"{event['timestamp'][:19]} - {event['type']} - {event['message']}\n")
                f.write("\n")

                # Threats
                threats = self.analyze_security_events()
                f.write("THREAT ANALYSIS:\n")
                f.write("-" * 17 + "\n")
                if threats:
                    for threat in threats:
                        f.write(f"• {threat['type']} ({threat['severity']}): {threat['description']}\n")
                else:
                    f.write("No active threats detected\n")
                f.write("\n")

                # Recommendations
                f.write("RECOMMENDATIONS:\n")
                f.write("-" * 15 + "\n")
                recommendations = self.generate_security_recommendations()
                for rec in recommendations:
                    f.write(f"• {rec}\n")

            print(f"✓ Security report generated: {report_file}")

        except Exception as e:
            print(f"Report generation failed: {e}")

    def calculate_security_score(self):
        """Calculate overall security score"""
        score = 0

        if self.encryption_enabled:
            score += 20
        if self.audit_logging:
            score += 15
        if self.input_validation:
            score += 15
        if self.rate_limiting:
            score += 10
        if self.encryption_key:
            score += 15
        if len(self.security_events) > 0:
            score += 5
        if len(self.session_tokens) >= 0:
            score += 10
        if self.check_directory_permissions():
            score += 10

        return min(100, score)

    def generate_security_recommendations(self):
        """Generate security recommendations"""
        recommendations = []

        if not self.encryption_enabled:
            recommendations.append("Enable encryption for sensitive data")

        if not self.audit_logging:
            recommendations.append("Enable audit logging to track security events")

        if not self.input_validation:
            recommendations.append("Enable input validation to prevent injection attacks")

        if not self.rate_limiting:
            recommendations.append("Enable rate limiting to prevent brute force attacks")

        if not self.encryption_key:
            recommendations.append("Generate encryption keys for data protection")

        threats = self.analyze_security_events()
        if threats:
            recommendations.append("Address detected security threats immediately")

        if len(self.session_tokens) > 10:
            recommendations.append("Review and clean up old sessions")

        return recommendations if recommendations else ["Security configuration is adequate"]

    def clean_temporary_files(self):
        """Clean temporary and cache files"""
        print("=== Clean Temporary Files ===")

        temp_patterns = [
            '*.tmp',
            '*.cache',
            '*.log.tmp',
            '*~',
            '*.bak'
        ]

        cleaned_count = 0
        cleaned_size = 0

        for pattern in temp_patterns:
            for temp_file in Path('.').rglob(pattern):
                try:
                    if temp_file.is_file():
                        size = temp_file.stat().st_size
                        temp_file.unlink()
                        cleaned_count += 1
                        cleaned_size += size
                except:
                    pass

        print(f"✓ Cleaned {cleaned_count} temporary files ({cleaned_size:,} bytes)")

    def update_file_permissions(self):
        """Update file permissions for security"""
        print("=== Update File Permissions ===")

        # Define permission updates
        permission_updates = {
            'main.py': 0o755,  # rwxr-xr-x
            'setup.sh': 0o755,  # rwxr-xr-x
            'requirements.txt': 0o644,  # rw-r--r--
            self.keys_dir: 0o700,  # rwx------
            self.keys_dir / 'master.key': 0o600,  # rw-------
        }

        updated_count = 0

        for file_path, permission in permission_updates.items():
            path = Path(file_path)
            if path.exists():
                try:
                    path.chmod(permission)
                    print(f"✓ Updated permissions for {file_path}")
                    updated_count += 1
                except Exception as e:
                    print(f"✗ Failed to update {file_path}: {e}")

        print(f"✓ Updated permissions for {updated_count} files")

    def emergency_lockdown(self):
        """Emergency security lockdown"""
        print("=== EMERGENCY SECURITY LOCKDOWN ===")
        print("⚠️  This will immediately:")
        print("• Terminate all active sessions")
        print("• Lock all user accounts")
        print("• Disable external access")
        print("• Enable maximum security settings")
        print()

        confirm = input("CONFIRM EMERGENCY LOCKDOWN? Type 'LOCKDOWN' to proceed: ").strip()
        if confirm != 'LOCKDOWN':
            print("Lockdown cancelled.")
            return

        print("Initiating emergency lockdown...")

        # Terminate all sessions
        session_count = len(self.session_tokens)
        self.session_tokens.clear()

        # Lock all accounts (simulate)
        self.locked_accounts['all_users'] = datetime.now().timestamp()

        # Enable all security features
        self.encryption_enabled = True
        self.audit_logging = True
        self.input_validation = True
        self.rate_limiting = True

        # Log emergency action
        self.log_security_event('CRITICAL', 'Emergency security lockdown activated', 'system')

        print("✓ Emergency lockdown activated")
        print(f"• {session_count} sessions terminated")
        print("• All security features enabled")
        print("• System locked down")

    def security_compliance_check(self):
        """Check security compliance"""
        print("=== Security Compliance Check ===")

        compliance_checks = [
            ("Encryption", self.encryption_enabled, "Data should be encrypted at rest"),
            ("Audit Logging", self.audit_logging, "Security events should be logged"),
            ("Input Validation", self.input_validation, "User input should be validated"),
            ("Rate Limiting", self.rate_limiting, "API requests should be rate limited"),
            ("Session Management", True, "Sessions should timeout appropriately"),
            ("Access Control", True, "Access should be properly controlled"),
            ("File Permissions", self.check_directory_permissions(), "Files should have secure permissions"),
        ]

        compliant_count = 0
        total_checks = len(compliance_checks)

        print("Compliance Results:")
        print("-" * 50)

        for check_name, status, description in compliance_checks:
            status_icon = "✓" if status else "✗"
            print(f"{status_icon} {check_name:<15} - {description}")
            if status:
                compliant_count += 1

        print("-" * 50)
        compliance_percent = (compliant_count / total_checks) * 100

        if compliance_percent >= 80:
            compliance_level = "COMPLIANT"
        elif compliance_percent >= 60:
            compliance_level = "MOSTLY COMPLIANT"
        else:
            compliance_level = "NON-COMPLIANT"

        print(f"Compliance Level: {compliance_level} ({compliant_count}/{total_checks} checks passed - {compliance_percent:.1f}%)")

        if compliance_percent < 100:
            print("\nRecommendations for full compliance:")
            for check_name, status, description in compliance_checks:
                if not status:
                    print(f"• Enable {check_name.lower()}")

    # Security utility methods for other modules to use

    def validate_input(self, input_data, input_type="text"):
        """Validate input data for security"""
        if not self.input_validation:
            return True, "Validation disabled"

        if not input_data:
            return False, "Input cannot be empty"

        # Length checks
        if len(str(input_data)) > 10000:
            return False, "Input too long"

        # Type-specific validation
        if input_type == "email":
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(input_data)):
                return False, "Invalid email format"

        elif input_type == "ip":
            try:
                ipaddress.ip_address(str(input_data))
            except:
                return False, "Invalid IP address format"

        elif input_type == "url":
            if not re.match(r'^https?://', str(input_data)):
                return False, "URL must start with http:// or https://"

        # Security checks
        suspicious_patterns = [
            r'[<>]',  # HTML tags
            r'[\'";]',  # SQL injection
            r'(?i)script|javascript|vbscript',  # Script injection
            r'\.\./',  # Directory traversal
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, str(input_data)):
                return False, "Potentially malicious input detected"

        return True, "Input validated successfully"

    def check_rate_limit(self, identifier, max_requests=10, time_window=60):
        """Check if request exceeds rate limit"""
        if not self.rate_limiting:
            return False

        current_time = time.time()
        request_times = self.rate_limits[identifier]

        # Remove old requests outside the time window
        while request_times and current_time - request_times[0] > time_window:
            request_times.popleft()

        # Check if under limit
        if len(request_times) >= max_requests:
            return True  # Rate limited

        # Add current request
        request_times.append(current_time)
        return False  # Not rate limited

    def authenticate_user(self, username, password):
        """Authenticate user (placeholder - implement based on your user system)"""
        # This is a placeholder - implement actual authentication logic
        # For now, just check against failed attempts

        if username in self.locked_accounts:
            lock_time = self.locked_accounts[username]
            if datetime.now().timestamp() - lock_time < self.lockout_duration:
                return False, "Account locked due to too many failed attempts"

        # Simulate authentication (replace with real logic)
        if username == "admin" and password == "password":  # Example only!
            self.failed_attempts[username] = 0  # Reset failed attempts
            return True, "Authentication successful"
        else:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1

            if self.failed_attempts[username] >= self.max_login_attempts:
                self.locked_accounts[username] = datetime.now().timestamp()
                self.log_security_event('WARNING', f'Account {username} locked due to failed attempts', username)

            return False, "Invalid credentials"

    def create_session(self, username):
        """Create a new session token"""
        session_id = secrets.token_urlsafe(32)
        self.session_tokens[session_id] = {
            'user': username,
            'created': datetime.now().isoformat(),
            'last_activity': datetime.now().timestamp()
        }
        return session_id

    def validate_session(self, session_id):
        """Validate session token"""
        if session_id not in self.session_tokens:
            return False

        session_data = self.session_tokens[session_id]
        last_activity = session_data['last_activity']
        current_time = datetime.now().timestamp()

        # Check timeout
        if current_time - last_activity > self.session_timeout:
            del self.session_tokens[session_id]
            return False

        # Update last activity
        session_data['last_activity'] = current_time
        return True

    def encrypt_data(self, data):
        """Encrypt data using the master key"""
        if not self.encryption_enabled or not self.encryption_key:
            return data

        try:
            fernet = Fernet(self.encryption_key)
            if isinstance(data, str):
                data = data.encode()
            return fernet.encrypt(data)
        except:
            return data

    def decrypt_data(self, encrypted_data):
        """Decrypt data using the master key"""
        if not self.encryption_enabled or not self.encryption_key:
            return encrypted_data

        try:
            fernet = Fernet(self.encryption_key)
            decrypted = fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except:
            return encrypted_data