"""
File Manager Module for Termux Command Center
Provides file management utilities using Termux capabilities.
"""

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "File management utilities"

    def run(self):
        print("\n=== File Manager ===")
        print("1. List files in current directory")
        print("2. Create directory")
        print("3. Create file")
        print("4. Show file contents")
        print("5. Copy file")
        print("6. Move file")
        print("7. Delete file/directory")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.list_files()
            elif choice == "2":
                self.create_directory()
            elif choice == "3":
                self.create_file()
            elif choice == "4":
                self.show_file()
            elif choice == "5":
                self.copy_file()
            elif choice == "6":
                self.move_file()
            elif choice == "7":
                self.delete_file()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def list_files(self):
        print("Files in current directory:")
        stdout, stderr, code = self.cc.run_command("ls -la")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def create_directory(self):
        dirname = input("Enter directory name: ").strip()
        stdout, stderr, code = self.cc.run_command(f"mkdir -p '{dirname}'")
        if code == 0:
            print(f"Directory '{dirname}' created.")
        else:
            print("Error:", stderr)

    def create_file(self):
        filename = input("Enter file name: ").strip()
        content = input("Enter file content (press Enter twice to finish):\n")
        try:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"File '{filename}' created.")
        except Exception as e:
            print(f"Error creating file: {e}")

    def show_file(self):
        filename = input("Enter file name: ").strip()
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(f"Contents of '{filename}':")
            print(content)
        except Exception as e:
            print(f"Error reading file: {e}")

    def copy_file(self):
        src = input("Source file: ").strip()
        dst = input("Destination: ").strip()
        stdout, stderr, code = self.cc.run_command(f"cp '{src}' '{dst}'")
        if code == 0:
            print("File copied.")
        else:
            print("Error:", stderr)

    def move_file(self):
        src = input("Source file: ").strip()
        dst = input("Destination: ").strip()
        stdout, stderr, code = self.cc.run_command(f"mv '{src}' '{dst}'")
        if code == 0:
            print("File moved.")
        else:
            print("Error:", stderr)

    def delete_file(self):
        path = input("Enter file/directory to delete: ").strip()
        confirm = input(f"Are you sure you want to delete '{path}'? (y/N): ").strip().lower()
        if confirm == 'y':
            stdout, stderr, code = self.cc.run_command(f"rm -rf '{path}'")
            if code == 0:
                print("Deleted.")
            else:
                print("Error:", stderr)
        else:
            print("Cancelled.")