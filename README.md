# Termux Command Center

A comprehensive cybersecurity toolkit for Termux Android environment, designed for purple teaming, OSINT, reconnaissance, penetration testing, and automated monitoring operations.

## 🚀 Features

### Core Capabilities
- **Automated Setup**: One-command installation of 30+ security tools
- **Real-time Monitoring**: Live system monitoring with curses-based dashboard
- **Advanced Scanning**: Intelligent network scanning with API integrations
- **API Integrations**: Multi-API support with rate limiting and caching
- **AI/ML Analysis**: Machine learning-powered anomaly detection
- **Reporting & Visualization**: Advanced charts and analytics with matplotlib
- **Team Collaboration**: Multi-user collaboration with RBAC and shared knowledge base
- **Performance Monitoring**: System performance tracking with optimization recommendations
- **Mobile Features**: Android-specific capabilities leveraging Termux:API
- **Backup & Restore**: Comprehensive backup and restore functionality
- **Security Hardening**: Encryption, access control, and audit logging

### Security Tools Integration
- **Network Scanning**: Nmap, Masscan, ZMap
- **Web Application Testing**: SQLMap, Nikto, Dirbuster
- **Wireless Security**: Aircrack-ng, Reaver, Pixie Dust
- **Password Cracking**: John the Ripper, Hashcat
- **Forensic Tools**: Autopsy, Volatility, Binwalk
- **Social Engineering**: SET, King Phisher
- **Exploitation**: Metasploit Framework, BeEF
- **OSINT Tools**: Maltego, Recon-ng, theHarvester

## 📦 Installation

### Full User Guide
For complete Termux setup, usage examples, API configuration, and detailed module instructions, read the full user guide:

- `USER_GUIDE.md`

### Automated Setup
```bash
git clone https://github.com/cmd-kevill33/termux_cmd_center.git
cd termux_cmd_center
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
# Install Python dependencies
pip install --user -r requirements.txt

# Install required Termux packages
pkg install nmap sqlmap nikto aircrack-ng john hashcat metasploit termux-api

# Make executable
chmod +x main.py
```

## 🎯 Usage

### Starting the Command Center
```bash
python main.py
```

### Main Menu Options
1. **Dashboard** - Real-time monitoring and system overview
2. **Automated Monitoring** - Background data collection and alerting
3. **Advanced Scanner** - Intelligent network scanning
4. **API Integrations** - Multi-API management and querying
5. **AI/ML Analysis** - Anomaly detection and pattern analysis
6. **Reporting & Visualization** - Generate charts and reports
7. **Collaboration** - Team management and shared resources
8. **Performance Monitoring** - System performance analysis
9. **Mobile Features** - Android-specific capabilities
10. **Backup & Restore** - Data backup and recovery
11. **Security Hardening** - Security configuration and monitoring

## 📁 Project Structure

```
termux-cmd-center/
├── main.py                 # Main application entry point
├── setup.sh               # Automated installation script
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── modules/              # Feature modules
│   ├── dashboard.py              # Real-time monitoring dashboard
│   ├── automated_monitoring.py   # Background monitoring system
│   ├── advanced_scanner.py       # Intelligent network scanning
│   ├── api_integrations.py       # Multi-API support
│   ├── ai_ml.py                  # AI/ML anomaly detection
│   ├── reporting_viz.py          # Reporting and visualization
│   ├── collaboration.py          # Team collaboration tools
│   ├── performance_monitoring.py # System performance monitoring
│   ├── mobile_features.py        # Android-specific features
│   ├── backup_restore.py         # Backup and restore functionality
│   └── security_hardening.py     # Security hardening tools
├── data/                 # Application data directory
│   ├── configs/          # Configuration files
│   ├── logs/            # Application logs
│   ├── reports/         # Generated reports
│   ├── backups/         # Backup archives
│   └── security/        # Security-related data
└── configs/             # Default configurations
```

## 🔧 Modules Overview

### 1. Dashboard (`dashboard.py`)
- Real-time system monitoring
- Interactive curses-based interface
- Live network statistics
- Process monitoring
- Alert management

### 2. Automated Monitoring (`automated_monitoring.py`)
- Background data collection
- Configurable monitoring intervals
- Alert system with notifications
- Historical data storage
- Automated reporting

### 3. Advanced Scanner (`advanced_scanner.py`)
- Intelligent network scanning
- Multi-phase scanning strategies
- Vulnerability detection
- Service enumeration
- Custom scan profiles

### 4. API Integrations (`api_integrations.py`)
- Multi-API support (VirusTotal, Shodan, etc.)
- Rate limiting and caching
- API key management
- Error handling and retries
- Data aggregation

### 5. AI/ML Analysis (`ai_ml.py`)
- Statistical anomaly detection
- Machine learning models
- Pattern recognition
- Predictive analysis
- Automated alerting

### 6. Reporting & Visualization (`reporting_viz.py`)
- Data visualization with matplotlib
- Interactive charts and graphs
- PDF report generation
- Export capabilities
- Custom report templates

### 7. Collaboration (`collaboration.py`)
- Multi-user support
- Role-based access control (RBAC)
- Shared knowledge base
- Team communication
- Project management

### 8. Performance Monitoring (`performance_monitoring.py`)
- System resource monitoring
- Performance metrics collection
- Optimization recommendations
- Historical performance data
- Alert thresholds

### 9. Mobile Features (`mobile_features.py`)
- Camera access and control
- GPS location services
- Sensor data collection
- Android notifications
- Device information gathering

### 10. Backup & Restore (`backup_restore.py`)
- Comprehensive backup creation
- Selective restore options
- Archive management
- Data export/import
- Emergency recovery

### 11. Security Hardening (`security_hardening.py`)
- Encryption management
- Access control
- Audit logging
- Threat detection
- Security compliance checking

## 🔐 Security Features

### Encryption
- AES-256 encryption for sensitive data
- Secure key management
- Encrypted backups
- Key rotation capabilities

### Access Control
- Session management
- Rate limiting
- Account lockouts
- Input validation

### Audit Logging
- Comprehensive security event logging
- Log analysis and reporting
- Compliance reporting
- Threat detection

## 📊 API Integrations

### Supported APIs
- **VirusTotal**: File and URL scanning
- **Shodan**: Internet-connected device search
- **Censys**: Certificate and host data
- **HaveIBeenPwned**: Breach data checking
- **IPInfo**: IP geolocation and details
- **AbuseIPDB**: IP abuse reporting

### API Configuration
```json
{
  "virustotal": {
    "api_key": "your_api_key_here",
    "rate_limit": 4,
    "timeout": 30
  },
  "shodan": {
    "api_key": "your_api_key_here",
    "rate_limit": 1,
    "timeout": 10
  }
}
```

## 📱 Mobile Features

### Termux:API Integration
- **Camera**: Photo capture and video recording
- **Location**: GPS coordinates and location services
- **Sensors**: Accelerometer, gyroscope, magnetometer
- **Notifications**: Android notification management
- **Contacts**: Contact database access
- **SMS**: SMS sending and receiving
- **Calls**: Call log access
- **Battery**: Battery status monitoring

### Mobile-Specific Capabilities
- On-device scanning and analysis
- Location-based intelligence gathering
- Mobile network monitoring
- Android application analysis
- Device security assessment

## 🤖 AI/ML Features

### Anomaly Detection
- Statistical analysis of network traffic
- Machine learning-based pattern recognition
- Automated threat detection
- Predictive security analysis

### Data Analysis
- Log analysis and correlation
- Behavioral pattern detection
- Risk assessment scoring
- Automated report generation

## 👥 Collaboration Features

### Team Management
- User account management
- Role-based permissions
- Team project organization
- Shared resource management

### Communication
- In-app messaging
- Alert broadcasting
- Report sharing
- Knowledge base management

## 📈 Performance Monitoring

### System Metrics
- CPU usage and load
- Memory utilization
- Network I/O statistics
- Disk usage and I/O
- Process monitoring

### Optimization
- Performance bottleneck identification
- Resource usage optimization
- Automated recommendations
- Historical trend analysis

## 💾 Backup & Recovery

### Backup Types
- **Full Backup**: Complete system backup
- **Configuration Backup**: Settings and configurations only
- **Data Backup**: Application data and logs

### Restore Options
- **Full Restore**: Complete system recovery
- **Selective Restore**: Individual file/directory recovery
- **Emergency Restore**: Critical system recovery

## 🔒 Security Hardening

### Security Controls
- Input sanitization and validation
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure session management

### Compliance
- Security audit trails
- Compliance reporting
- Vulnerability assessments
- Security policy enforcement

## 📋 Requirements

### System Requirements
- **Android Device**: API level 21+ (Android 5.0+)
- **Termux**: Latest version recommended
- **Storage**: Minimum 2GB free space
- **RAM**: 1GB minimum, 2GB recommended

### Python Dependencies
```
curses
json
time
pathlib
threading
urllib
matplotlib
seaborn
pandas
scikit-learn
cryptography
psutil
requests
```

### Termux Packages
```
python
curl
wget
git
openssl
libffi
libxml2
libxslt
```

## 🚨 Important Notes

### Security Warning
This toolkit contains powerful security tools that can be used for both defensive and offensive purposes. Use responsibly and only on systems you own or have explicit permission to test.

### Legal Compliance
Ensure compliance with local laws and regulations regarding cybersecurity testing and information gathering activities.

### Android Permissions
Some mobile features require specific Android permissions. Grant the following when prompted:
- Camera access
- Location access
- Storage access
- Contacts access
- SMS access

## 🐛 Troubleshooting

### Common Issues
1. **Module Import Errors**: Run `pip install -r requirements.txt`
2. **Permission Denied**: Use `termux-setup-storage` for storage access
3. **API Rate Limits**: Configure API keys and respect rate limits
4. **Memory Issues**: Close other applications and restart Termux

### Debug Mode
Enable debug logging by setting the environment variable:
```bash
export TERMUX_CMD_DEBUG=1
python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling
- Test on multiple Android devices
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Termux project for the Android Linux environment
- Security tool developers and maintainers
- Open source security community
- Android security researchers

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation
- Join the community discussions

---

**Disclaimer**: This tool is for educational and authorized security testing purposes only. Users are responsible for complying with applicable laws and regulations.

## Red Teaming Tools

- Metasploit Framework
- SQLMap for SQL injection
- Hydra for brute forcing
- John the Ripper & Hashcat for password cracking
- Aircrack-ng for wireless security
- Wireshark/Tshark for packet analysis
- Social-Engineer Toolkit

## OSINT Features

- Domain and IP intelligence
- Username enumeration across platforms
- Social media reconnaissance
- Google dorks
- Shodan integration
- Email OSINT

## Adding Custom Modules

Create Python files in `modules/` with a `Module` class:

```python
class Module:
    def __init__(self, command_center):
        self.cc = command_center
        self.description = "My Custom Tool"

    def run(self):
        # Your functionality here
        pass
```

## Directory Structure

```
~/termux_cmd_center/
├── main.py                 # Main application
├── setup.sh               # Automated setup
├── modules/               # Feature modules
│   ├── osint.py
│   ├── recon.py
│   ├── web_servers.py
│   ├── red_teaming.py
│   ├── purple_teaming.py
│   ├── tutorials.py
│   └── file_manager.py
├── config/                # Configuration files
├── tools/                 # Additional tools/scripts
├── data/                  # Data storage & tutorials
├── logs/                  # Log files
└── requirements.txt       # Python dependencies
```

## Security Notice

This tool is designed for authorized security testing and research only. Always obtain proper permission before performing security assessments. Use responsibly and in compliance with applicable laws and regulations.

## Requirements

- Termux on Android
- Internet connection for package installation
- Storage permissions for full functionality
