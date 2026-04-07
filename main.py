#!/usr/bin/env python3
"""
Termux Command Center
A modular utility to manage and execute common Termux commands and features.
"""

import os
import subprocess
import sys
import importlib.util
from pathlib import Path

class CommandCenter:
    def __init__(self):
        self.base_dir = Path.home() / "termux_cmd_center"
        self.modules_dir = self.base_dir / "modules"
        self.config_dir = self.base_dir / "config"
        self.tools_dir = self.base_dir / "tools"
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"

        # Ensure directories exist
        for dir_path in [self.modules_dir, self.config_dir, self.tools_dir, self.data_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.modules = {}
        self.load_modules()

    def run_command(self, command, cwd=None):
        """Run a shell command and return the output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def load_modules(self):
        """Load available modules."""
        if not self.modules_dir.exists():
            return

        for module_file in self.modules_dir.glob("*.py"):
            if module_file.name == "__init__.py":
                continue
            module_name = module_file.stem
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'Module'):
                    self.modules[module_name] = module.Module(self)
                    print(f"Loaded module: {module_name}")
            except Exception as e:
                print(f"Failed to load module {module_name}: {e}")

    def show_menu(self):
        """Display the main menu."""
        print("\n=== Termux Command Center ===")
        print("Built-in commands:")
        print("1. Update packages")
        print("2. Install package")
        print("3. List installed packages")
        print("4. Check storage access")
        print("5. Show system info")
        print("6. Run custom command")

        # Show loaded modules
        if self.modules:
            print("\nLoaded modules:")
            for i, (name, module) in enumerate(self.modules.items(), 7):
                print(f"{i}. {name}: {getattr(module, 'description', 'No description')}")

        print("0. Exit")

    def handle_builtin(self, choice):
        """Handle built-in commands."""
        if choice == "1":
            print("Updating packages...")
            stdout, stderr, code = self.run_command("pkg update && pkg upgrade -y")
            print(stdout)
            if stderr:
                print("Errors:", stderr)
        elif choice == "2":
            package = input("Enter package name: ").strip()
            print(f"Installing {package}...")
            stdout, stderr, code = self.run_command(f"pkg install {package} -y")
            print(stdout)
            if stderr:
                print("Errors:", stderr)
        elif choice == "3":
            print("Listing installed packages...")
            stdout, stderr, code = self.run_command("pkg list-installed")
            print(stdout[:1000])  # Limit output
            if stderr:
                print("Errors:", stderr)
        elif choice == "4":
            print("Checking storage access...")
            stdout, stderr, code = self.run_command("ls ~/storage/shared")
            if code == 0:
                print("Storage access is set up.")
            else:
                print("Storage access not set up. Run 'termux-setup-storage'.")
        elif choice == "5":
            print("System info:")
            stdout, stderr, code = self.run_command("uname -a && echo 'Termux version:' $TERMUX_VERSION")
            print(stdout)
        elif choice == "6":
            command = input("Enter command to run: ").strip()
            print(f"Running: {command}")
            stdout, stderr, code = self.run_command(command)
            print(stdout)
            if stderr:
                print("Errors:", stderr)

    def run(self):
        """Main loop."""
        print("Welcome to Termux Command Center!")

        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Exiting...")
                break
            elif choice in ["1", "2", "3", "4", "5", "6"]:
                self.handle_builtin(choice)
            elif choice.isdigit() and int(choice) >= 7:
                module_index = int(choice) - 7
                if 0 <= module_index < len(self.modules):
                    module_name = list(self.modules.keys())[module_index]
                    module = self.modules[module_name]
                    if hasattr(module, 'run'):
                        try:
                            module.run()
                        except Exception as e:
                            print(f"Error running module {module_name}: {e}")
                    else:
                        print(f"Module {module_name} has no run method.")
                else:
                    print("Invalid module choice.")
            else:
                print("Invalid choice. Try again.")

            input("\nPress Enter to continue...")

def main():
    center = CommandCenter()
    center.run()

if __name__ == "__main__":
    main()