"""
OSINT Module for Termux Command Center
Open Source Intelligence gathering tools and utilities.
"""

import json
import urllib.request
import urllib.parse
import re

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Open Source Intelligence gathering tools"

    def run(self):
        print("\n=== OSINT Tools ===")
        print("1. WHOIS lookup")
        print("2. DNS enumeration")
        print("3. IP geolocation")
        print("4. Email OSINT")
        print("5. Username search")
        print("6. Social media search")
        print("7. Google dorks")
        print("8. Shodan search")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.whois_lookup()
            elif choice == "2":
                self.dns_enum()
            elif choice == "3":
                self.ip_geolocate()
            elif choice == "4":
                self.email_osint()
            elif choice == "5":
                self.username_search()
            elif choice == "6":
                self.social_search()
            elif choice == "7":
                self.google_dorks()
            elif choice == "8":
                self.shodan_search()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def whois_lookup(self):
        domain = input("Enter domain: ").strip()
        print(f"Performing WHOIS lookup for {domain}...")
        stdout, stderr, code = self.cc.run_command(f"whois {domain}")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def dns_enum(self):
        domain = input("Enter domain: ").strip()
        print(f"DNS enumeration for {domain}...")
        stdout, stderr, code = self.cc.run_command(f"dig {domain} ANY")
        print(stdout)
        if stderr:
            print("Errors:", stderr)

    def ip_geolocate(self):
        ip = input("Enter IP address: ").strip()
        print(f"Geolocating {ip}...")
        try:
            url = f"http://ip-api.com/json/{ip}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error: {e}")

    def email_osint(self):
        email = input("Enter email: ").strip()
        print(f"OSINT for {email}...")
        # Basic email validation and domain check
        if '@' in email:
            domain = email.split('@')[1]
            print(f"Domain: {domain}")
            self.whois_lookup()  # Reuse whois for domain
        else:
            print("Invalid email format")

    def username_search(self):
        username = input("Enter username: ").strip()
        print(f"Searching for username: {username}")
        # Check common platforms
        platforms = ["https://github.com/", "https://twitter.com/", "https://instagram.com/"]
        for platform in platforms:
            url = platform + username
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    if response.getcode() == 200:
                        print(f"Found: {url}")
            except:
                print(f"Not found: {url}")

    def social_search(self):
        query = input("Enter search query: ").strip()
        print(f"Social media search for: {query}")
        # This would require API keys for real implementation
        print("Note: Real social media OSINT requires API access")
        print("Consider using tools like theHarvester or Maltego")

    def google_dorks(self):
        print("Common Google dorks:")
        dorks = [
            'site:example.com filetype:pdf',
            'inurl:admin login',
            'intitle:"index of" "parent directory"',
            'site:pastebin.com "password"',
            'inurl:php?id= site:.edu'
        ]
        for dork in dorks:
            print(f"- {dork}")
        print("\nUse: google 'dork here'")

    def shodan_search(self):
        query = input("Enter Shodan search query: ").strip()
        print(f"Shodan search for: {query}")
        print("Note: Requires Shodan API key")
        print("Install shodan: pip install shodan")
        print("Then: shodan search --key YOUR_API_KEY '{query}'")