"""
Network Tools Module for Termux Command Center
Provides network utilities and information.
"""

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Network utilities and information"

    def run(self):
        print("\n=== Network Tools ===")
        print("1. Show IP address")
        print("2. Ping host")
        print("3. Check internet connection")
        print("4. Show network interfaces")
        print("5. Port scan (basic)")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.show_ip()
            elif choice == "2":
                self.ping_host()
            elif choice == "3":
                self.check_internet()
            elif choice == "4":
                self.show_interfaces()
            elif choice == "5":
                self.port_scan()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def show_ip(self):
        print("IP Addresses:")
        stdout, stderr, code = self.cc.run_command("ip addr show | grep 'inet ' | awk '{print $2}'")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def ping_host(self):
        host = input("Enter host to ping: ").strip()
        print(f"Pinging {host}...")
        stdout, stderr, code = self.cc.run_command(f"ping -c 4 {host}")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def check_internet(self):
        print("Checking internet connection...")
        stdout, stderr, code = self.cc.run_command("ping -c 1 8.8.8.8")
        if code == 0:
            print("Internet connection is available.")
        else:
            print("No internet connection.")

    def show_interfaces(self):
        print("Network interfaces:")
        stdout, stderr, code = self.cc.run_command("ip link show")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def port_scan(self):
        host = input("Enter host to scan: ").strip()
        ports = input("Enter ports (e.g., 22,80,443): ").strip()
        if not ports:
            ports = "22,80,443"
        print(f"Scanning {host} on ports {ports}...")
        # Basic port scan using nc
        for port in ports.split(','):
            port = port.strip()
            stdout, stderr, code = self.cc.run_command(f"nc -z -w1 {host} {port}")
            if code == 0:
                print(f"Port {port}: Open")
            else:
                print(f"Port {port}: Closed")