"""
Recon Module for Termux Command Center
Reconnaissance tools for information gathering.
"""

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Reconnaissance and information gathering"

    def run(self):
        print("\n=== Recon Tools ===")
        print("1. Nmap scan")
        print("2. Port scan")
        print("3. Service enumeration")
        print("4. Vulnerability scan")
        print("5. Web recon")
        print("6. Network mapping")
        print("7. Subdomain enumeration")
        print("8. Directory busting")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.nmap_scan()
            elif choice == "2":
                self.port_scan()
            elif choice == "3":
                self.service_enum()
            elif choice == "4":
                self.vuln_scan()
            elif choice == "5":
                self.web_recon()
            elif choice == "6":
                self.network_map()
            elif choice == "7":
                self.subdomain_enum()
            elif choice == "8":
                self.dir_busting()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def nmap_scan(self):
        target = input("Enter target (IP/domain): ").strip()
        scan_type = input("Scan type (quick/full/custom): ").strip().lower()
        if scan_type == "quick":
            cmd = f"nmap -T4 -F {target}"
        elif scan_type == "full":
            cmd = f"nmap -T4 -A -v {target}"
        else:
            options = input("Enter custom nmap options: ").strip()
            cmd = f"nmap {options} {target}"
        print(f"Running: {cmd}")
        stdout, stderr, code = self.cc.run_command(cmd)
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def port_scan(self):
        target = input("Enter target: ").strip()
        ports = input("Enter ports (default 1-1000): ").strip()
        if not ports:
            ports = "1-1000"
        print(f"Port scanning {target} on ports {ports}...")
        stdout, stderr, code = self.cc.run_command(f"nmap -p {ports} {target}")
        print(stdout)

    def service_enum(self):
        target = input("Enter target: ").strip()
        print("Service enumeration...")
        stdout, stderr, code = self.cc.run_command(f"nmap -sV -sC {target}")
        print(stdout)

    def vuln_scan(self):
        target = input("Enter target: ").strip()
        print("Vulnerability scanning with nmap...")
        stdout, stderr, code = self.cc.run_command(f"nmap --script vuln {target}")
        print(stdout)

    def web_recon(self):
        url = input("Enter URL: ").strip()
        print("Web reconnaissance...")
        # Use whatweb or similar
        stdout, stderr, code = self.cc.run_command(f"whatweb {url}")
        print(stdout)
        if code != 0:
            print("whatweb not found. Install with: pkg install whatweb")

    def network_map(self):
        network = input("Enter network (e.g., 192.168.1.0/24): ").strip()
        print(f"Network mapping for {network}...")
        stdout, stderr, code = self.cc.run_command(f"nmap -sn {network}")
        print(stdout)

    def subdomain_enum(self):
        domain = input("Enter domain: ").strip()
        wordlist = input("Wordlist file (default: /usr/share/wordlists/subdomains.txt): ").strip()
        if not wordlist:
            wordlist = "/usr/share/wordlists/subdomains.txt"
        print(f"Subdomain enumeration for {domain}...")
        # Use dnsrecon or similar
        stdout, stderr, code = self.cc.run_command(f"dnsrecon -d {domain} -t brt")
        print(stdout)
        if code != 0:
            print("dnsrecon not found. Install with: pkg install dnsrecon")

    def dir_busting(self):
        url = input("Enter URL: ").strip()
        wordlist = input("Wordlist file (default: /usr/share/wordlists/dirb/common.txt): ").strip()
        if not wordlist:
            wordlist = "/usr/share/wordlists/dirb/common.txt"
        print(f"Directory busting {url}...")
        stdout, stderr, code = self.cc.run_command(f"dirb {url} {wordlist}")
        print(stdout)
        if code != 0:
            print("dirb not found. Install with: pkg install dirb")