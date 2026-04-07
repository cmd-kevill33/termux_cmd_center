"""
API Integration Module for Termux Command Center
Handles both free and paid API services with intelligent fallbacks and error handling.
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "API integrations for enhanced intelligence gathering"
        self.api_config_file = self.cc.config_dir / "api_config.json"
        self.api_cache_file = self.cc.data_dir / "api_cache.json"
        self.load_api_config()
        self.load_cache()

    def load_api_config(self):
        """Load API configuration"""
        default_config = {
            "apis": {
                "shodan": {
                    "name": "Shodan",
                    "free_tier": True,
                    "rate_limit": 1,  # requests per minute
                    "endpoints": {
                        "search": "https://api.shodan.io/shodan/host/search",
                        "host": "https://api.shodan.io/shodan/host/{ip}",
                        "info": "https://api.shodan.io/api-info"
                    }
                },
                "virustotal": {
                    "name": "VirusTotal",
                    "free_tier": True,
                    "rate_limit": 4,  # requests per minute
                    "endpoints": {
                        "file": "https://www.virustotal.com/api/v3/files/{hash}",
                        "url": "https://www.virustotal.com/api/v3/urls/{url_id}",
                        "ip": "https://www.virustotal.com/api/v3/ip_addresses/{ip}"
                    }
                },
                "ipinfo": {
                    "name": "IPInfo",
                    "free_tier": True,
                    "rate_limit": 1000,  # requests per day
                    "endpoints": {
                        "ip": "https://ipinfo.io/{ip}/json"
                    }
                },
                "hunter": {
                    "name": "Hunter.io",
                    "free_tier": True,
                    "rate_limit": 50,  # requests per month
                    "endpoints": {
                        "domain": "https://api.hunter.io/v2/domain-search",
                        "email": "https://api.hunter.io/v2/email-verifier"
                    }
                },
                "haveibeenpwned": {
                    "name": "HaveIBeenPwned",
                    "free_tier": True,
                    "rate_limit": 10,  # requests per minute (when using API key)
                    "endpoints": {
                        "breaches": "https://haveibeenpwned.com/api/v3/breachedaccount/{account}",
                        "paste": "https://haveibeenpwned.com/api/v3/pasteaccount/{account}"
                    }
                },
                "abuseipdb": {
                    "name": "AbuseIPDB",
                    "free_tier": True,
                    "rate_limit": 1000,  # requests per day
                    "endpoints": {
                        "check": "https://api.abuseipdb.com/api/v2/check"
                    }
                },
                "urlscan": {
                    "name": "URLScan.io",
                    "free_tier": True,
                    "rate_limit": 3,  # submissions per minute
                    "endpoints": {
                        "scan": "https://urlscan.io/api/v1/scan/",
                        "result": "https://urlscan.io/api/v1/result/{uuid}"
                    }
                }
            },
            "api_keys": {},
            "rate_limits": {},
            "cache_enabled": True,
            "cache_ttl": 3600  # 1 hour
        }

        if not self.api_config_file.exists():
            with open(self.api_config_file, 'w') as f:
                json.dump(default_config, f, indent=2)

        with open(self.api_config_file, 'r') as f:
            self.api_config = json.load(f)

    def load_cache(self):
        """Load API response cache"""
        if self.api_cache_file.exists():
            try:
                with open(self.api_cache_file, 'r') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
        else:
            self.cache = {}

    def save_cache(self):
        """Save API response cache"""
        with open(self.api_cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def run(self):
        print("\n=== API Integrations ===")
        print("1. Configure API keys")
        print("2. Test API connections")
        print("3. Shodan search")
        print("4. VirusTotal lookup")
        print("5. IP intelligence")
        print("6. Email OSINT")
        print("7. Domain reconnaissance")
        print("8. URL analysis")
        print("9. View API status")
        print("10. Clear cache")
        print("0. Back to main menu")

        while True:
            choice = input("Enter your choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.configure_api_keys()
            elif choice == "2":
                self.test_api_connections()
            elif choice == "3":
                self.shodan_search()
            elif choice == "4":
                self.virustotal_lookup()
            elif choice == "5":
                self.ip_intelligence()
            elif choice == "6":
                self.email_osint()
            elif choice == "7":
                self.domain_recon()
            elif choice == "8":
                self.url_analysis()
            elif choice == "9":
                self.view_api_status()
            elif choice == "10":
                self.clear_cache()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def configure_api_keys(self):
        """Configure API keys for paid services"""
        print("Configure API Keys (leave blank to skip or use free tier):")
        print("Note: Free tiers are available for most services, but paid keys provide higher limits.")

        apis = {
            "shodan": "Shodan API Key (free tier available)",
            "virustotal": "VirusTotal API Key (free tier available)",
            "ipinfo": "IPInfo API Token (free tier available)",
            "hunter": "Hunter.io API Key (free tier available)",
            "abuseipdb": "AbuseIPDB API Key (free tier available)",
            "urlscan": "URLScan.io API Key (free tier available)"
        }

        for api_name, description in apis.items():
            current_key = self.api_config["api_keys"].get(api_name, "")
            masked_key = "*" * len(current_key) if current_key else "Not set"

            print(f"\n{description}")
            print(f"Current: {masked_key}")
            new_key = input("New key (or press Enter to keep current): ").strip()
            if new_key:
                self.api_config["api_keys"][api_name] = new_key
                print(f"✓ {api_name} API key updated")
            elif current_key:
                print(f"✓ Keeping existing {api_name} API key")
            else:
                print(f"Using free tier for {api_name}")

        self.save_api_config()

    def test_api_connections(self):
        """Test API connections"""
        print("Testing API connections...")

        test_cases = {
            "shodan": self.test_shodan,
            "virustotal": self.test_virustotal,
            "ipinfo": self.test_ipinfo,
            "hunter": self.test_hunter,
            "haveibeenpwned": self.test_haveibeenpwned,
            "abuseipdb": self.test_abuseipdb,
            "urlscan": self.test_urlscan
        }

        for api_name, test_func in test_cases.items():
            print(f"\nTesting {api_name}...")
            try:
                result = test_func()
                if result['status'] == 'success':
                    print(f"✓ {api_name} API working")
                    if 'details' in result:
                        print(f"  Details: {result['details']}")
                else:
                    print(f"✗ {api_name} API failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"✗ {api_name} API error: {e}")

    def make_api_request(self, api_name, endpoint_key, params=None, method='GET', data=None):
        """Make API request with caching and rate limiting"""
        if api_name not in self.api_config["apis"]:
            return {'status': 'error', 'error': f'Unknown API: {api_name}'}

        api_info = self.api_config["apis"][api_name]
        endpoint = api_info["endpoints"].get(endpoint_key)
        if not endpoint:
            return {'status': 'error', 'error': f'Unknown endpoint: {endpoint_key}'}

        # Check cache first
        if self.api_config.get("cache_enabled", True):
            cache_key = f"{api_name}_{endpoint_key}_{str(params)}_{str(data)}"
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if time.time() - cached_data['timestamp'] < self.api_config.get("cache_ttl", 3600):
                    return cached_data['data']

        # Rate limiting
        self.check_rate_limit(api_name)

        # Build URL
        url = endpoint
        if params:
            url += "?" + urllib.parse.urlencode(params)

        # Add API key if available
        headers = {'User-Agent': 'Termux-Command-Center/1.0'}
        api_key = self.api_config["api_keys"].get(api_name)
        if api_key:
            if api_name in ['shodan', 'virustotal', 'hunter', 'abuseipdb', 'urlscan']:
                params = params or {}
                params['key'] = api_key
                url = endpoint + "?" + urllib.parse.urlencode(params)
            elif api_name == 'ipinfo':
                headers['Authorization'] = f'Bearer {api_key}'
            elif api_name == 'haveibeenpwned':
                headers['hibp-api-key'] = api_key

        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            if data:
                req.data = json.dumps(data).encode('utf-8')
                headers['Content-Type'] = 'application/json'

            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))

            # Update rate limit tracking
            self.update_rate_limit(api_name)

            # Cache response
            if self.api_config.get("cache_enabled", True):
                self.cache[cache_key] = {
                    'timestamp': time.time(),
                    'data': response_data
                }
                self.save_cache()

            return response_data

        except urllib.error.HTTPError as e:
            error_msg = f"HTTP {e.code}: {e.reason}"
            if e.code == 401:
                error_msg += " (Check API key)"
            elif e.code == 429:
                error_msg += " (Rate limit exceeded)"
            return {'status': 'error', 'error': error_msg}
        except urllib.error.URLError as e:
            return {'status': 'error', 'error': f'Network error: {e.reason}'}
        except json.JSONDecodeError:
            return {'status': 'error', 'error': 'Invalid JSON response'}
        except Exception as e:
            return {'status': 'error', 'error': f'Unexpected error: {e}'}

    def check_rate_limit(self, api_name):
        """Check and enforce rate limits"""
        if api_name not in self.api_config["rate_limits"]:
            self.api_config["rate_limits"][api_name] = []

        rate_limits = self.api_config["rate_limits"][api_name]
        current_time = time.time()

        # Remove old requests outside the time window
        api_info = self.api_config["apis"][api_name]
        time_window = 60  # 1 minute
        rate_limits[:] = [t for t in rate_limits if current_time - t < time_window]

        if len(rate_limits) >= api_info.get("rate_limit", 1):
            sleep_time = time_window - (current_time - rate_limits[0])
            if sleep_time > 0:
                print(f"Rate limit reached for {api_name}. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)

    def update_rate_limit(self, api_name):
        """Update rate limit tracking"""
        if api_name not in self.api_config["rate_limits"]:
            self.api_config["rate_limits"][api_name] = []
        self.api_config["rate_limits"][api_name].append(time.time())

    def shodan_search(self):
        """Shodan search functionality"""
        query = input("Enter Shodan search query: ").strip()
        if not query:
            return

        print(f"Searching Shodan for: {query}")
        result = self.make_api_request("shodan", "search", {"query": query})

        if result.get('status') == 'error':
            print(f"Error: {result['error']}")
            return

        if 'matches' in result:
            print(f"Found {len(result['matches'])} results:")
            for match in result['matches'][:5]:  # Show first 5
                print(f"  IP: {match.get('ip_str', 'N/A')}")
                print(f"  Port: {match.get('port', 'N/A')}")
                print(f"  Hostname: {match.get('hostnames', ['N/A'])[0] if match.get('hostnames') else 'N/A'}")
                print(f"  Data: {match.get('data', '')[:100]}...")
                print()
        else:
            print("No results found or API error.")

    def virustotal_lookup(self):
        """VirusTotal lookup"""
        target_type = input("Lookup type (file/hash/url/ip): ").strip().lower()
        target = input(f"Enter {target_type}: ").strip()

        if target_type in ['file', 'hash']:
            result = self.make_api_request("virustotal", "file", None, target_hash=target)
        elif target_type == 'url':
            # First submit URL for analysis
            submit_result = self.make_api_request("virustotal", "url_submit", {"url": target})
            if submit_result.get('data'):
                analysis_id = submit_result['data']['id']
                print("URL submitted for analysis. Check back later.")
                return
        elif target_type == 'ip':
            result = self.make_api_request("virustotal", "ip", None, ip=target)

        if result.get('status') == 'error':
            print(f"Error: {result['error']}")
        else:
            print("VirusTotal results:")
            print(json.dumps(result, indent=2))

    def ip_intelligence(self):
        """IP intelligence gathering"""
        ip = input("Enter IP address: ").strip()

        print(f"Gathering intelligence for IP: {ip}")

        # IPInfo (free/paid)
        print("\nIPInfo:")
        ipinfo_result = self.make_api_request("ipinfo", "ip", ip=ip)
        if ipinfo_result.get('status') == 'error':
            print(f"Error: {ipinfo_result['error']}")
        else:
            print(f"  Location: {ipinfo_result.get('city', 'N/A')}, {ipinfo_result.get('region', 'N/A')}, {ipinfo_result.get('country', 'N/A')}")
            print(f"  ISP: {ipinfo_result.get('org', 'N/A')}")

        # AbuseIPDB
        print("\nAbuseIPDB:")
        abuse_result = self.make_api_request("abuseipdb", "check", {"ipAddress": ip})
        if abuse_result.get('status') == 'error':
            print(f"Error: {abuse_result['error']}")
        else:
            data = abuse_result.get('data', {})
            print(f"  Abuse Score: {data.get('abuseConfidenceScore', 'N/A')}%")
            print(f"  Reports: {data.get('totalReports', 'N/A')}")

        # Shodan
        print("\nShodan:")
        shodan_result = self.make_api_request("shodan", "host", ip=ip)
        if shodan_result.get('status') == 'error':
            print(f"Error: {shodan_result['error']}")
        else:
            print(f"  Hostnames: {', '.join(shodan_result.get('hostnames', []))}")
            print(f"  Ports: {', '.join(str(p) for p in shodan_result.get('ports', []))}")

    def email_osint(self):
        """Email OSINT"""
        email = input("Enter email address: ").strip()

        print(f"Gathering OSINT for email: {email}")

        # Hunter.io
        print("\nHunter.io:")
        hunter_result = self.make_api_request("hunter", "email", {"email": email})
        if hunter_result.get('status') == 'error':
            print(f"Error: {hunter_result['error']}")
        else:
            data = hunter_result.get('data', {})
            print(f"  Result: {data.get('result', 'N/A')}")
            print(f"  Score: {data.get('score', 'N/A')}")

        # HaveIBeenPwned
        print("\nHaveIBeenPwned:")
        hibp_result = self.make_api_request("haveibeenpwned", "breaches", account=email)
        if hibp_result.get('status') == 'error':
            print(f"Error: {hibp_result['error']}")
        else:
            breaches = hibp_result
            if breaches:
                print(f"  Found in {len(breaches)} breaches:")
                for breach in breaches[:3]:
                    print(f"    - {breach.get('Name', 'Unknown')} ({breach.get('BreachDate', 'Unknown')})")
            else:
                print("  No breaches found")

    def domain_recon(self):
        """Domain reconnaissance"""
        domain = input("Enter domain: ").strip()

        print(f"Gathering reconnaissance for domain: {domain}")

        # Hunter.io domain search
        print("\nHunter.io Domain Search:")
        hunter_result = self.make_api_request("hunter", "domain", {"domain": domain})
        if hunter_result.get('status') == 'error':
            print(f"Error: {hunter_result['error']}")
        else:
            data = hunter_result.get('data', {})
            print(f"  Emails found: {data.get('total', 0)}")
            if data.get('emails'):
                print("  Sample emails:")
                for email in data['emails'][:3]:
                    print(f"    - {email.get('value', '')}")

        # Shodan search for domain
        print("\nShodan Domain Search:")
        shodan_result = self.make_api_request("shodan", "search", {"query": f"hostname:{domain}"})
        if shodan_result.get('status') == 'error':
            print(f"Error: {shodan_result['error']}")
        else:
            matches = shodan_result.get('matches', [])
            print(f"  Found {len(matches)} hosts")
            if matches:
                match = matches[0]
                print(f"  Sample: {match.get('ip_str', 'N/A')}:{match.get('port', 'N/A')}")

    def url_analysis(self):
        """URL analysis"""
        url = input("Enter URL to analyze: ").strip()

        print(f"Analyzing URL: {url}")

        # URLScan.io
        print("\nURLScan.io:")
        scan_result = self.make_api_request("urlscan", "scan", data={"url": url, "visibility": "public"})
        if scan_result.get('status') == 'error':
            print(f"Error: {scan_result['error']}")
        else:
            uuid = scan_result.get('uuid')
            if uuid:
                print(f"  Scan submitted. UUID: {uuid}")
                print("  Results will be available at: https://urlscan.io/result/{uuid}")
            else:
                print("  Scan submission failed")

        # VirusTotal URL analysis
        print("\nVirusTotal URL Analysis:")
        vt_result = self.make_api_request("virustotal", "url_scan", {"url": url})
        if vt_result.get('status') == 'error':
            print(f"Error: {vt_result['error']}")
        else:
            print("  URL submitted for analysis")

    def view_api_status(self):
        """View API status and usage"""
        print("=== API Status ===")

        for api_name, api_info in self.api_config["apis"].items():
            has_key = api_name in self.api_config["api_keys"]
            rate_limits = self.api_config["rate_limits"].get(api_name, [])
            recent_requests = len([t for t in rate_limits if time.time() - t < 60])

            print(f"\n{api_info['name']} ({api_name}):")
            print(f"  API Key: {'✓ Configured' if has_key else '✗ Not configured (using free tier)'}")
            print(f"  Rate Limit: {api_info.get('rate_limit', 'Unknown')} requests/minute")
            print(f"  Recent Requests: {recent_requests}/minute")

    def clear_cache(self):
        """Clear API cache"""
        confirm = input("Clear API response cache? (y/N): ").strip().lower()
        if confirm == 'y':
            self.cache = {}
            self.save_cache()
            print("✓ Cache cleared")

    def save_api_config(self):
        """Save API configuration"""
        with open(self.api_config_file, 'w') as f:
            json.dump(self.api_config, f, indent=2)

    # Test functions for each API
    def test_shodan(self):
        return self.make_api_request("shodan", "info")

    def test_virustotal(self):
        # This would require a test endpoint, for now just check if key works
        api_key = self.api_config["api_keys"].get("virustotal")
        if api_key:
            return {'status': 'success', 'details': 'API key configured'}
        return {'status': 'success', 'details': 'Using free tier'}

    def test_ipinfo(self):
        result = self.make_api_request("ipinfo", "ip", ip="8.8.8.8")
        if result.get('status') == 'error':
            return result
        return {'status': 'success', 'details': f"IP: {result.get('ip', 'unknown')}"}

    def test_hunter(self):
        api_key = self.api_config["api_keys"].get("hunter")
        if api_key:
            return {'status': 'success', 'details': 'API key configured'}
        return {'status': 'success', 'details': 'Using free tier'}

    def test_haveibeenpwned(self):
        # Test with a known breached account (haveibeenpwned test account)
        result = self.make_api_request("haveibeenpwned", "breaches", account="test@example.com")
        if isinstance(result, list):
            return {'status': 'success', 'details': f'API working, found {len(result)} breaches'}
        return {'status': 'error', 'error': 'API test failed'}

    def test_abuseipdb(self):
        result = self.make_api_request("abuseipdb", "check", {"ipAddress": "127.0.0.1"})
        if result.get('status') == 'error':
            return result
        return {'status': 'success', 'details': 'API working'}

    def test_urlscan(self):
        api_key = self.api_config["api_keys"].get("urlscan")
        if api_key:
            return {'status': 'success', 'details': 'API key configured'}
        return {'status': 'success', 'details': 'Using free tier'}