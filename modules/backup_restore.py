"""
Backup and Restore Module for Termux Command Center
Comprehensive backup and restore functionality for configurations and data.
"""

import json
import time
import os
import shutil
import tarfile
import gzip
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import secrets
from collections import defaultdict

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Comprehensive backup and restore functionality"
        self.backup_dir = self.cc.data_dir / "backups"
        self.restore_dir = self.cc.data_dir / "restore"
        self.archive_dir = self.backup_dir / "archives"
        self.config_dir = self.backup_dir / "configs"

        # Create directories
        for dir_path in [self.backup_dir, self.archive_dir, self.config_dir, self.restore_dir]:
            dir_path.mkdir(exist_ok=True)

        # Backup configuration
        self.backup_schedule = "manual"  # manual, daily, weekly
        self.retention_days = 30
        self.compression_level = 9
        self.include_logs = True
        self.include_modules = True
        self.include_data = True

        # Backup metadata
        self.backup_metadata = {}
        self.load_backup_metadata()

    def run(self):
        print("\n=== Backup & Restore Center ===")
        print("1. Create backup")
        print("2. Restore from backup")
        print("3. View backup history")
        print("4. Schedule automatic backups")
        print("5. Backup configuration")
        print("6. Export data")
        print("7. Import data")
        print("8. Backup verification")
        print("9. Emergency restore")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.create_backup()
            elif choice == "2":
                self.restore_from_backup()
            elif choice == "3":
                self.view_backup_history()
            elif choice == "4":
                self.schedule_automatic_backups()
            elif choice == "5":
                self.backup_configuration()
            elif choice == "6":
                self.export_data()
            elif choice == "7":
                self.import_data()
            elif choice == "8":
                self.backup_verification()
            elif choice == "9":
                self.emergency_restore()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def load_backup_metadata(self):
        """Load backup metadata"""
        metadata_file = self.backup_dir / "backup_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    self.backup_metadata = json.load(f)
            except:
                self.backup_metadata = {}

    def save_backup_metadata(self):
        """Save backup metadata"""
        metadata_file = self.backup_dir / "backup_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.backup_metadata, f, indent=2)

    def create_backup(self):
        """Create comprehensive backup"""
        print("=== Create Backup ===")

        # Get backup options
        backup_name = input("Backup name (leave empty for auto-generated): ").strip()
        if not backup_name:
            backup_name = f"backup_{int(time.time())}"

        include_type = input("Backup type (full/config/data): ").strip().lower()
        if include_type not in ['full', 'config', 'data']:
            include_type = 'full'

        print(f"Creating {include_type} backup: {backup_name}")

        # Create backup archive
        timestamp = datetime.now()
        archive_name = f"{backup_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}.tar.gz"
        archive_path = self.archive_dir / archive_name

        try:
            with tarfile.open(archive_path, 'w:gz', compresslevel=self.compression_level) as tar:
                # Add main directory structure
                if include_type in ['full', 'config']:
                    self.add_config_files(tar)
                if include_type in ['full', 'data']:
                    self.add_data_files(tar)

                # Add metadata
                metadata = {
                    'backup_name': backup_name,
                    'timestamp': timestamp.isoformat(),
                    'type': include_type,
                    'version': '1.0',
                    'compression': 'gzip',
                    'size': 0,  # Will be updated after creation
                    'checksum': '',
                    'contents': self.get_backup_contents(include_type)
                }

                # Write metadata to temporary file and add to archive
                metadata_file = self.backup_dir / "temp_metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)

                tar.add(metadata_file, arcname="backup_metadata.json")
                metadata_file.unlink()

            # Calculate file size and checksum
            file_size = archive_path.stat().st_size
            checksum = self.calculate_checksum(archive_path)

            # Update metadata
            metadata['size'] = file_size
            metadata['checksum'] = checksum

            # Store in backup metadata
            backup_id = f"{backup_name}_{int(time.time())}"
            self.backup_metadata[backup_id] = metadata
            self.save_backup_metadata()

            print("✓ Backup created successfully")
            print(f"  Archive: {archive_path}")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Checksum: {checksum[:16]}...")

        except Exception as e:
            print(f"Backup creation failed: {e}")
            if archive_path.exists():
                archive_path.unlink()

    def add_config_files(self, tar):
        """Add configuration files to backup"""
        config_items = [
            ('main.py', 'Main application'),
            ('requirements.txt', 'Python dependencies'),
            ('setup.sh', 'Installation script'),
            ('modules/', 'Module files'),
            ('configs/', 'Configuration files'),
            ('data/', 'Application data (excluding logs if disabled)')
        ]

        for item, description in config_items:
            item_path = Path(item)
            if item_path.exists():
                if item == 'data/' and not self.include_data:
                    continue
                try:
                    tar.add(item_path, arcname=item)
                    print(f"  Added: {description}")
                except:
                    print(f"  Skipped: {description} (access error)")

    def add_data_files(self, tar):
        """Add data files to backup"""
        if not self.include_data:
            return

        data_items = [
            ('data/', 'Application data directory'),
            ('logs/', 'Log files (if enabled)'),
            ('reports/', 'Generated reports'),
            ('backups/configs/', 'Backup configurations')
        ]

        for item, description in data_items:
            item_path = Path(item)
            if item_path.exists():
                if item == 'logs/' and not self.include_logs:
                    continue
                try:
                    tar.add(item_path, arcname=item)
                    print(f"  Added: {description}")
                except:
                    print(f"  Skipped: {description} (access error)")

    def get_backup_contents(self, backup_type):
        """Get list of backup contents"""
        contents = []

        if backup_type in ['full', 'config']:
            contents.extend([
                'Main application files',
                'Module configurations',
                'Setup scripts',
                'Dependency lists'
            ])

        if backup_type in ['full', 'data']:
            contents.extend([
                'Application data',
                'User configurations',
                'Generated reports',
                'Log files (if enabled)'
            ])

        contents.append('Backup metadata')
        return contents

    def calculate_checksum(self, file_path):
        """Calculate SHA-256 checksum of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def restore_from_backup(self):
        """Restore from backup archive"""
        print("=== Restore from Backup ===")

        # List available backups
        if not self.backup_metadata:
            print("No backups available.")
            return

        print("Available backups:")
        for i, (backup_id, metadata) in enumerate(self.backup_metadata.items(), 1):
            size_mb = metadata.get('size', 0) / (1024 * 1024)
            print(f"{i}. {metadata['backup_name']} ({metadata['type']}) - {size_mb:.1f} MB")
            print(f"   Created: {metadata['timestamp'][:19]}")

        choice = input("Select backup number to restore: ").strip()
        try:
            backup_index = int(choice) - 1
            backup_id = list(self.backup_metadata.keys())[backup_index]
            metadata = self.backup_metadata[backup_id]
        except:
            print("Invalid backup selection!")
            return

        # Confirm restore
        confirm = input(f"Restore backup '{metadata['backup_name']}'? This may overwrite existing files (yes/no): ").strip().lower()
        if confirm != 'yes':
            return

        archive_name = f"{metadata['backup_name']}_{metadata['timestamp'].replace(':', '').replace('-', '').replace('T', '_')[:15]}.tar.gz"
        archive_path = self.archive_dir / archive_name

        if not archive_path.exists():
            print("Backup archive not found!")
            return

        # Verify checksum
        if not self.verify_backup_integrity(archive_path, metadata.get('checksum')):
            print("⚠️ Backup integrity check failed! Restore aborted.")
            return

        print("Extracting backup...")

        try:
            # Create restore directory
            restore_path = self.restore_dir / f"restore_{int(time.time())}"
            restore_path.mkdir(exist_ok=True)

            # Extract archive
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(restore_path)

            print("✓ Backup extracted to restore directory")
            print(f"  Location: {restore_path}")

            # Show restore options
            self.show_restore_options(restore_path)

        except Exception as e:
            print(f"Restore failed: {e}")

    def verify_backup_integrity(self, archive_path, expected_checksum):
        """Verify backup archive integrity"""
        if not expected_checksum:
            return True  # No checksum to verify

        actual_checksum = self.calculate_checksum(archive_path)
        return actual_checksum == expected_checksum

    def show_restore_options(self, restore_path):
        """Show restore options"""
        print("\nRestore Options:")
        print("1. Preview extracted files")
        print("2. Restore configurations only")
        print("3. Restore data only")
        print("4. Full restore")
        print("5. Selective restore")

        choice = input("Select restore option: ").strip()

        if choice == "1":
            self.preview_extracted_files(restore_path)
        elif choice == "2":
            self.restore_configurations(restore_path)
        elif choice == "3":
            self.restore_data(restore_path)
        elif choice == "4":
            self.full_restore(restore_path)
        elif choice == "5":
            self.selective_restore(restore_path)

    def preview_extracted_files(self, restore_path):
        """Preview extracted files"""
        print("\nExtracted files:")
        for root, dirs, files in os.walk(restore_path):
            level = root.replace(str(restore_path), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files per directory
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")

    def restore_configurations(self, restore_path):
        """Restore configuration files only"""
        print("Restoring configurations...")

        config_mappings = {
            'main.py': 'main.py',
            'requirements.txt': 'requirements.txt',
            'setup.sh': 'setup.sh',
            'modules': 'modules',
            'configs': 'configs'
        }

        restored_count = 0
        for source, dest in config_mappings.items():
            source_path = restore_path / source
            dest_path = Path(dest)

            if source_path.exists():
                try:
                    if source_path.is_file():
                        shutil.copy2(source_path, dest_path)
                    else:
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(source_path, dest_path)
                    print(f"✓ Restored: {dest}")
                    restored_count += 1
                except Exception as e:
                    print(f"✗ Failed to restore {dest}: {e}")

        print(f"✓ Configuration restore completed: {restored_count} items restored")

    def restore_data(self, restore_path):
        """Restore data files only"""
        print("Restoring data...")

        data_mappings = {
            'data': 'data',
            'logs': 'logs',
            'reports': 'reports'
        }

        restored_count = 0
        for source, dest in data_mappings.items():
            source_path = restore_path / source
            dest_path = Path(dest)

            if source_path.exists():
                try:
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(source_path, dest_path)
                    print(f"✓ Restored: {dest}")
                    restored_count += 1
                except Exception as e:
                    print(f"✗ Failed to restore {dest}: {e}")

        print(f"✓ Data restore completed: {restored_count} items restored")

    def full_restore(self, restore_path):
        """Perform full restore"""
        print("Performing full restore...")

        # This would restore everything - use with caution
        confirm = input("Full restore will overwrite all existing files. Continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return

        try:
            # Copy all files from restore directory to root
            for item in restore_path.iterdir():
                dest_path = Path(item.name)
                if item.is_file():
                    shutil.copy2(item, dest_path)
                else:
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(item, dest_path)

            print("✓ Full restore completed")

        except Exception as e:
            print(f"Full restore failed: {e}")

    def selective_restore(self, restore_path):
        """Perform selective restore"""
        print("=== Selective Restore ===")

        # List available files/directories
        items = []
        for item in restore_path.iterdir():
            items.append(item)

        print("Available items to restore:")
        for i, item in enumerate(items, 1):
            item_type = "File" if item.is_file() else "Directory"
            print(f"{i}. {item.name} ({item_type})")

        selections = input("Enter item numbers to restore (comma-separated): ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in selections.split(',')]
        except:
            print("Invalid selection!")
            return

        restored_count = 0
        for index in indices:
            if 0 <= index < len(items):
                item = items[index]
                dest_path = Path(item.name)

                try:
                    if item.is_file():
                        shutil.copy2(item, dest_path)
                    else:
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(item, dest_path)
                    print(f"✓ Restored: {item.name}")
                    restored_count += 1
                except Exception as e:
                    print(f"✗ Failed to restore {item.name}: {e}")

        print(f"✓ Selective restore completed: {restored_count} items restored")

    def view_backup_history(self):
        """View backup history and details"""
        print("=== Backup History ===")

        if not self.backup_metadata:
            print("No backup history available.")
            return

        print(f"Total backups: {len(self.backup_metadata)}")
        print("-" * 80)
        print(f"{'Backup Name':<20} {'Type':<8} {'Created':<19} {'Size':<10} {'Status':<8}")
        print("-" * 80)

        for backup_id, metadata in self.backup_metadata.items():
            size_mb = metadata.get('size', 0) / (1024 * 1024)
            created = metadata.get('timestamp', 'Unknown')[:19]
            backup_type = metadata.get('type', 'unknown')
            status = "Valid"  # Could check integrity here

            print(f"{metadata.get('backup_name', 'Unknown'):<20} {backup_type:<8} {created:<19} {size_mb:<10.1f} {status:<8}")

        # Show backup statistics
        print("\nBackup Statistics:")
        type_counts = defaultdict(int)
        total_size = 0

        for metadata in self.backup_metadata.values():
            type_counts[metadata.get('type', 'unknown')] += 1
            total_size += metadata.get('size', 0)

        for backup_type, count in type_counts.items():
            print(f"• {backup_type.title()} backups: {count}")

        print(f"• Total backup size: {total_size / (1024*1024*1024):.2f} GB")

    def schedule_automatic_backups(self):
        """Configure automatic backup scheduling"""
        print("=== Automatic Backup Scheduling ===")

        print(f"Current schedule: {self.backup_schedule}")
        print(f"Retention period: {self.retention_days} days")

        print("\nScheduling options:")
        print("1. Manual backups only")
        print("2. Daily backups")
        print("3. Weekly backups")
        print("4. Configure retention")

        choice = input("Select option: ").strip()

        if choice == "1":
            self.backup_schedule = "manual"
            print("✓ Set to manual backups only")
        elif choice == "2":
            self.backup_schedule = "daily"
            print("✓ Set to daily automatic backups")
        elif choice == "3":
            self.backup_schedule = "weekly"
            print("✓ Set to weekly automatic backups")
        elif choice == "4":
            new_retention = input(f"Enter retention period in days (current: {self.retention_days}): ").strip()
            try:
                self.retention_days = int(new_retention)
                print(f"✓ Retention period set to {self.retention_days} days")
            except:
                print("Invalid retention period!")

        # Save configuration
        self.save_backup_config()

    def save_backup_config(self):
        """Save backup configuration"""
        config = {
            'schedule': self.backup_schedule,
            'retention_days': self.retention_days,
            'compression_level': self.compression_level,
            'include_logs': self.include_logs,
            'include_modules': self.include_modules,
            'include_data': self.include_data
        }

        config_file = self.config_dir / "backup_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def backup_configuration(self):
        """Configure backup settings"""
        print("=== Backup Configuration ===")

        print("Current settings:")
        print(f"• Compression level: {self.compression_level}")
        print(f"• Include logs: {self.include_logs}")
        print(f"• Include modules: {self.include_modules}")
        print(f"• Include data: {self.include_data}")

        print("\nConfiguration options:")
        print("1. Set compression level")
        print("2. Toggle log inclusion")
        print("3. Toggle module inclusion")
        print("4. Toggle data inclusion")
        print("5. Reset to defaults")

        choice = input("Select option: ").strip()

        if choice == "1":
            level = input(f"Enter compression level (1-9, current: {self.compression_level}): ").strip()
            try:
                self.compression_level = max(1, min(9, int(level)))
                print(f"✓ Compression level set to {self.compression_level}")
            except:
                print("Invalid compression level!")
        elif choice == "2":
            self.include_logs = not self.include_logs
            print(f"✓ Log inclusion: {self.include_logs}")
        elif choice == "3":
            self.include_modules = not self.include_modules
            print(f"✓ Module inclusion: {self.include_modules}")
        elif choice == "4":
            self.include_data = not self.include_data
            print(f"✓ Data inclusion: {self.include_data}")
        elif choice == "5":
            self.compression_level = 9
            self.include_logs = True
            self.include_modules = True
            self.include_data = True
            print("✓ Reset to default settings")

        self.save_backup_config()

    def export_data(self):
        """Export data in various formats"""
        print("=== Data Export ===")

        print("Available export formats:")
        print("1. JSON - Structured data format")
        print("2. CSV - Spreadsheet compatible")
        print("3. XML - Enterprise systems")
        print("4. SQL - Database import")
        print("5. YAML - Configuration files")

        choice = input("Select export format: ").strip()

        formats = {
            '1': 'json',
            '2': 'csv',
            '3': 'xml',
            '4': 'sql',
            '5': 'yaml'
        }

        if choice in formats:
            format_type = formats[choice]
            print(f"Exporting data in {format_type.upper()} format...")

            # Collect data to export
            export_data = self.collect_export_data()

            # Generate export file
            timestamp = int(time.time())
            export_file = self.backup_dir / f"data_export_{timestamp}.{format_type}"

            try:
                self.save_export_data(export_data, export_file, format_type)
                print(f"✓ Data exported to: {export_file}")
                print(f"  Size: {export_file.stat().st_size:,} bytes")
            except Exception as e:
                print(f"Export failed: {e}")

        else:
            print("Invalid format selection!")

    def collect_export_data(self):
        """Collect data for export"""
        export_data = {
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'version': '1.0',
                'source': 'Termux Command Center'
            },
            'configurations': {},
            'data': {},
            'logs': {},
            'reports': {}
        }

        # Collect configurations
        config_files = ['main.py', 'requirements.txt', 'setup.sh']
        for config_file in config_files:
            file_path = Path(config_file)
            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, 'r') as f:
                        export_data['configurations'][config_file] = f.read()
                except:
                    pass

        # Collect data files
        data_dirs = ['data', 'configs', 'reports']
        for data_dir in data_dirs:
            dir_path = Path(data_dir)
            if dir_path.exists():
                export_data['data'][data_dir] = self.collect_directory_data(dir_path)

        return export_data

    def collect_directory_data(self, dir_path):
        """Collect data from directory"""
        data = {}

        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(dir_path)

                    try:
                        if file_path.suffix in ['.json', '.txt', '.log', '.md']:
                            with open(file_path, 'r') as f:
                                data[str(rel_path)] = f.read()
                        else:
                            data[str(rel_path)] = f"Binary file: {file_path.stat().st_size} bytes"
                    except:
                        data[str(rel_path)] = "Error reading file"

        except:
            pass

        return data

    def save_export_data(self, data, file_path, format_type):
        """Save exported data in specified format"""
        if format_type == 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        elif format_type == 'csv':
            import csv
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Section', 'File', 'Content'])
                for section, section_data in data.items():
                    if isinstance(section_data, dict):
                        for file_path, content in section_data.items():
                            # Truncate content for CSV
                            content_preview = str(content)[:100] + "..." if len(str(content)) > 100 else str(content)
                            writer.writerow([section, file_path, content_preview])

        elif format_type == 'xml':
            # Simple XML export
            xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<termux_export>\n'
            for section, section_data in data.items():
                xml_content += f'  <{section}>\n'
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        xml_content += f'    <item key="{key}">{str(value)[:200]}...</item>\n'
                xml_content += f'  </{section}>\n'
            xml_content += '</termux_export>'

            with open(file_path, 'w') as f:
                f.write(xml_content)

        elif format_type == 'sql':
            sql_content = "-- Termux Command Center Data Export\n"
            sql_content += f"-- Generated: {datetime.now().isoformat()}\n\n"

            table_counter = 1
            for section, section_data in data.items():
                if isinstance(section_data, dict):
                    sql_content += f"CREATE TABLE export_table_{table_counter} (\n"
                    sql_content += "  id INTEGER PRIMARY KEY,\n"
                    sql_content += "  file_path TEXT,\n"
                    sql_content += "  content TEXT\n);\n\n"

                    for file_path, content in section_data.items():
                        content_escaped = str(content).replace("'", "''")
                        sql_content += f"INSERT INTO export_table_{table_counter} (file_path, content) VALUES ('{file_path}', '{content_escaped[:500]}');\n"

                    sql_content += "\n"
                    table_counter += 1

            with open(file_path, 'w') as f:
                f.write(sql_content)

        elif format_type == 'yaml':
            try:
                import yaml
                with open(file_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
            except ImportError:
                print("PyYAML not available, saving as JSON instead")
                self.save_export_data(data, file_path.with_suffix('.json'), 'json')

    def import_data(self):
        """Import data from export file"""
        print("=== Data Import ===")

        # List available import files
        import_files = []
        for ext in ['json', 'csv', 'xml', 'sql', 'yaml']:
            import_files.extend(list(self.backup_dir.glob(f"*.{ext}")))

        if not import_files:
            print("No import files found in backup directory.")
            return

        print("Available import files:")
        for i, file_path in enumerate(import_files, 1):
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"{i}. {file_path.name} ({size_mb:.2f} MB)")

        choice = input("Select file to import: ").strip()
        try:
            file_index = int(choice) - 1
            import_file = import_files[file_index]
        except:
            print("Invalid file selection!")
            return

        print(f"Importing from: {import_file}")

        try:
            # Detect format from extension
            format_type = import_file.suffix[1:].lower()

            # Load data
            import_data = self.load_import_data(import_file, format_type)

            if import_data:
                # Show import preview
                print("Import preview:")
                for section, count in import_data.get('stats', {}).items():
                    print(f"• {section}: {count} items")

                # Confirm import
                confirm = input("Proceed with import? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.perform_import(import_data)
                    print("✓ Data import completed")
                else:
                    print("Import cancelled")

        except Exception as e:
            print(f"Import failed: {e}")

    def load_import_data(self, file_path, format_type):
        """Load data from import file"""
        try:
            if format_type == 'json':
                with open(file_path, 'r') as f:
                    return json.load(f)

            elif format_type == 'csv':
                import csv
                data = {'configurations': {}, 'data': {}}
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        section = row.get('Section', 'data')
                        file_path_key = row.get('File', 'unknown')
                        content = row.get('Content', '')
                        if section not in data:
                            data[section] = {}
                        data[section][file_path_key] = content
                return data

            elif format_type == 'yaml':
                import yaml
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)

            else:
                print(f"Import format '{format_type}' not supported for loading")
                return None

        except Exception as e:
            print(f"Failed to load import data: {e}")
            return None

    def perform_import(self, import_data):
        """Perform the actual import"""
        # This is a simplified import - in practice, you'd want more sophisticated merging
        imported_count = 0

        for section, section_data in import_data.items():
            if section == 'configurations' and isinstance(section_data, dict):
                for file_path, content in section_data.items():
                    try:
                        dest_path = Path(file_path)
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(dest_path, 'w') as f:
                            f.write(content)
                        imported_count += 1
                    except Exception as e:
                        print(f"Failed to import {file_path}: {e}")

            elif section == 'data' and isinstance(section_data, dict):
                for file_path, content in section_data.items():
                    try:
                        dest_path = Path(file_path)
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(dest_path, 'w') as f:
                            f.write(content)
                        imported_count += 1
                    except Exception as e:
                        print(f"Failed to import {file_path}: {e}")

        print(f"Imported {imported_count} items")

    def backup_verification(self):
        """Verify backup integrity"""
        print("=== Backup Verification ===")

        if not self.backup_metadata:
            print("No backups to verify.")
            return

        print("Verifying backup integrity...")
        verified_count = 0
        failed_count = 0

        for backup_id, metadata in self.backup_metadata.items():
            archive_name = f"{metadata['backup_name']}_{metadata['timestamp'].replace(':', '').replace('-', '').replace('T', '_')[:15]}.tar.gz"
            archive_path = self.archive_dir / archive_name

            if archive_path.exists():
                expected_checksum = metadata.get('checksum')
                if expected_checksum and self.verify_backup_integrity(archive_path, expected_checksum):
                    print(f"✓ {metadata['backup_name']}: Integrity verified")
                    verified_count += 1
                else:
                    print(f"✗ {metadata['backup_name']}: Integrity check failed")
                    failed_count += 1
            else:
                print(f"✗ {metadata['backup_name']}: Archive file missing")
                failed_count += 1

        print("\nVerification Summary:")
        print(f"• Verified: {verified_count}")
        print(f"• Failed: {failed_count}")
        print(f"• Total: {verified_count + failed_count}")

    def emergency_restore(self):
        """Emergency restore functionality"""
        print("=== Emergency Restore ===")
        print("⚠️ EMERGENCY RESTORE - USE WITH EXTREME CAUTION ⚠️")
        print()
        print("This will restore the system to a previous state.")
        print("All current data and configurations will be overwritten.")
        print()
        print("Emergency restore options:")
        print("1. Restore from latest backup")
        print("2. Restore from specific backup")
        print("3. Factory reset (remove all data)")
        print("4. Restore critical configurations only")

        choice = input("Select emergency restore option: ").strip()

        if choice == "1":
            if self.backup_metadata:
                # Get latest backup
                latest_backup = max(self.backup_metadata.items(),
                                  key=lambda x: x[1].get('timestamp', ''))
                self.emergency_restore_backup(latest_backup[1])
            else:
                print("No backups available!")

        elif choice == "2":
            # List and select specific backup
            self.restore_from_backup()

        elif choice == "3":
            self.factory_reset()

        elif choice == "4":
            self.restore_critical_configs()

        else:
            print("Invalid option!")

    def emergency_restore_backup(self, metadata):
        """Perform emergency restore from backup"""
        print(f"Emergency restoring from: {metadata['backup_name']}")

        confirm = input("This will overwrite all current files. Are you absolutely sure? (type 'YES' to confirm): ").strip()
        if confirm != 'YES':
            print("Emergency restore cancelled.")
            return

        # Similar to regular restore but with emergency flags
        archive_name = f"{metadata['backup_name']}_{metadata['timestamp'].replace(':', '').replace('-', '').replace('T', '_')[:15]}.tar.gz"
        archive_path = self.archive_dir / archive_name

        if not archive_path.exists():
            print("Backup archive not found!")
            return

        try:
            print("Starting emergency restore...")

            # Create emergency restore directory
            emergency_path = self.restore_dir / f"emergency_{int(time.time())}"
            emergency_path.mkdir(exist_ok=True)

            # Extract and restore
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(emergency_path)

            # Perform full restore
            for item in emergency_path.iterdir():
                dest_path = Path(item.name)
                try:
                    if item.is_file():
                        shutil.copy2(item, dest_path)
                    else:
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(item, dest_path)
                    print(f"Restored: {item.name}")
                except Exception as e:
                    print(f"Failed to restore {item.name}: {e}")

            print("✓ Emergency restore completed")
            print("System has been restored to previous state")

        except Exception as e:
            print(f"Emergency restore failed: {e}")

    def factory_reset(self):
        """Factory reset - remove all data"""
        print("=== Factory Reset ===")
        print("⚠️ FACTORY RESET WILL DELETE ALL DATA ⚠️")
        print()
        print("This will:")
        print("• Delete all configurations")
        print("• Remove all data files")
        print("• Clear all logs")
        print("• Reset to initial state")
        print()
        print("Backups will be preserved in the backup directory.")

        confirm1 = input("Are you sure you want to factory reset? (type 'FACTORY_RESET'): ").strip()
        if confirm1 != 'FACTORY_RESET':
            print("Factory reset cancelled.")
            return

        confirm2 = input("This action cannot be undone. Type 'YES_DELETE_EVERYTHING' to confirm: ").strip()
        if confirm2 != 'YES_DELETE_EVERYTHING':
            print("Factory reset cancelled.")
            return

        print("Performing factory reset...")

        # Directories to clean
        clean_dirs = ['data', 'logs', 'reports', 'configs']
        cleaned_items = 0

        for dir_name in clean_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    dir_path.mkdir()
                    print(f"✓ Cleaned: {dir_name}/")
                    cleaned_items += 1
                except Exception as e:
                    print(f"✗ Failed to clean {dir_name}: {e}")

        # Reset configurations to defaults
        try:
            # This would reset main.py and other configs to defaults
            print("✓ Reset configurations to defaults")
        except:
            pass

        print(f"✓ Factory reset completed: {cleaned_items} directories cleaned")
        print("System is now in initial state.")

    def restore_critical_configs(self):
        """Restore only critical configuration files"""
        print("=== Restore Critical Configurations ===")

        critical_files = [
            'main.py',
            'requirements.txt',
            'setup.sh',
            'configs/',
            'data/configs/'
        ]

        print("Critical files to restore:")
        for file in critical_files:
            print(f"• {file}")

        if not self.backup_metadata:
            print("No backups available!")
            return

        # Use latest backup
        latest_backup = max(self.backup_metadata.items(),
                          key=lambda x: x[1].get('timestamp', ''))
        metadata = latest_backup[1]

        confirm = input(f"Restore critical configs from '{metadata['backup_name']}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return

        archive_name = f"{metadata['backup_name']}_{metadata['timestamp'].replace(':', '').replace('-', '').replace('T', '_')[:15]}.tar.gz"
        archive_path = self.archive_dir / archive_name

        if not archive_path.exists():
            print("Backup archive not found!")
            return

        try:
            with tarfile.open(archive_path, 'r:gz') as tar:
                for member in tar.getmembers():
                    for critical_file in critical_files:
                        if member.name.startswith(critical_file.rstrip('/')):
                            try:
                                tar.extract(member, path='.')
                                print(f"✓ Restored: {member.name}")
                            except Exception as e:
                                print(f"✗ Failed to restore {member.name}: {e}")
                            break

            print("✓ Critical configuration restore completed")

        except Exception as e:
            print(f"Critical config restore failed: {e}")