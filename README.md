# Hacking666

A comprehensive security testing framework for various attack vectors and penetration testing techniques.

## Overview

This repository contains tools and utilities for security testing, including:
- Python-based attack demonstrations
- **Android Security Testing Framework** - Tools for Android application security analysis and penetration testing

## Android Development - Security Testing

The Android Security Testing Framework provides a comprehensive suite of tools for testing Android application security, discovering vulnerabilities, and demonstrating attack vectors.

### Features

#### 🔧 Tools
- **ADB Wrapper** - Python wrapper for Android Debug Bridge (ADB) commands
  - Device management and interaction
  - Package installation/removal
  - File push/pull operations
  - Logcat monitoring
  - Shell command execution

- **APK Analyzer** - Security analysis for Android APK files
  - Permission analysis
  - Dangerous permission detection
  - Hardcoded secrets scanning
  - Backup and debugging configuration checks
  - Exported component detection

#### 🎯 Exploits
- **Intent Hijacking** - Demonstrate Intent-based vulnerabilities
  - Find exported activities
  - Send malicious intents
  - Test deeplink vulnerabilities
  - Intent injection testing
  - PoC generation

- **Debug Exploitation** - Exploit debuggable applications
  - Debuggable app detection
  - Debugger attachment
  - Memory dumping
  - Runtime string extraction
  - SSL pinning bypass guidance
  - Shared library enumeration

#### 🛠️ Utilities
- **Logger** - Colored logging for security testing
- **Device Info** - Comprehensive device information gathering
  - System information
  - Security configuration
  - Storage and network details
  - Installed app enumeration

### Installation

```bash
# Clone the repository
git clone https://github.com/Hackwell666/Hacking666.git
cd Hacking666

# No additional dependencies required for basic usage
# Optional: Install enhanced features
pip install -r requirements.txt
```

### Prerequisites

- Python 3.6+
- Android Debug Bridge (ADB) installed and in PATH
- Android device with USB debugging enabled (for testing)

### Quick Start

```python
from android_security.tools.adb_wrapper import ADBWrapper
from android_security.utils.device_info import DeviceInfo

# Initialize ADB
adb = ADBWrapper()

# List connected devices
devices = adb.list_devices()
print(f"Connected devices: {devices}")

# Get device information
device_info = DeviceInfo(adb)
report = device_info.generate_report()
print(report)
```

### Usage Examples

#### 1. Device Management

```python
from android_security.tools.adb_wrapper import ADBWrapper

adb = ADBWrapper()

# List all connected devices
devices = adb.list_devices()

# Get device information
info = adb.get_device_info()
print(f"Model: {info['model']}")
print(f"Android Version: {info['android_version']}")

# List installed packages
packages = adb.list_packages()
print(f"Total packages: {len(packages)}")
```

#### 2. APK Security Analysis

```python
from android_security.tools.apk_analyzer import APKAnalyzer

# Analyze an APK file
analyzer = APKAnalyzer("/path/to/app.apk")

# Extract APK contents
analyzer.extract_apk("/tmp/extracted")

# Check for dangerous permissions
dangerous = analyzer.check_dangerous_permissions()
print(f"Dangerous permissions: {dangerous}")

# Scan for hardcoded secrets
secrets = analyzer.scan_for_hardcoded_secrets("/tmp/extracted")
for secret in secrets:
    print(f"Found {secret['type']}: {secret['value']} in {secret['file']}")

# Generate security report
report = analyzer.security_report("/tmp/extracted")
print(report)
```

#### 3. Intent Hijacking

```python
from android_security.tools.adb_wrapper import ADBWrapper
from android_security.exploits.intent_hijacking import IntentHijacker

adb = ADBWrapper()
hijacker = IntentHijacker(adb)

# Find exported activities
package = "com.example.vulnerableapp"
activities = hijacker.find_exported_activities(package)
print(f"Exported activities: {activities}")

# Test deeplink vulnerability
deeplink = "myapp://open?url=https://attacker.com"
result = hijacker.test_deeplink_vulnerability(package, deeplink)
print(result)

# Send malicious intent
success = hijacker.send_malicious_intent(
    component=f"{package}/.MainActivity",
    action="android.intent.action.VIEW",
    extras={"test": "malicious_payload"}
)
```

#### 4. Debug Exploitation

```python
from android_security.tools.adb_wrapper import ADBWrapper
from android_security.exploits.debug_exploit import DebugExploit

adb = ADBWrapper()
debug = DebugExploit(adb)

# Check if app is debuggable
package = "com.example.debuggableapp"
is_debuggable = debug.check_if_debuggable(package)
print(f"Debuggable: {is_debuggable}")

if is_debuggable:
    # Get process information
    pid = debug.get_app_pid(package)
    print(f"PID: {pid}")
    
    # Get loaded libraries
    libraries = debug.get_shared_libraries(package)
    print(f"Loaded libraries: {libraries}")
    
    # Extract runtime strings
    strings = debug.extract_runtime_strings(package)
    print(strings)
```

#### 5. Comprehensive Device Analysis

```python
from android_security.tools.adb_wrapper import ADBWrapper
from android_security.utils.device_info import DeviceInfo

adb = ADBWrapper()
device_info = DeviceInfo(adb)

# Generate full device report
report = device_info.generate_report()
print(report)

# Get security-specific information
security = device_info.get_security_info()
print(f"SELinux: {security['selinux']}")
print(f"Rooted: {security['rooted']}")
print(f"Security Patch: {security['security_patch']}")
```

### Running Examples

```bash
# Run the example script
python examples.py
```

### Project Structure

```
android_security/
├── __init__.py
├── tools/
│   ├── __init__.py
│   ├── adb_wrapper.py      # ADB command wrapper
│   └── apk_analyzer.py     # APK security analysis
├── exploits/
│   ├── __init__.py
│   ├── intent_hijacking.py # Intent-based attacks
│   └── debug_exploit.py    # Debug exploitation
└── utils/
    ├── __init__.py
    ├── logger.py           # Logging utilities
    └── device_info.py      # Device information gathering
```

### Security Features

- 🔍 **Permission Analysis** - Detect dangerous permissions in Android apps
- 🔐 **Secret Detection** - Scan for hardcoded API keys, tokens, and passwords
- 🎯 **Attack Surface** - Identify exported components and entry points
- 🐛 **Debug Detection** - Find debuggable applications
- 📱 **Device Profiling** - Comprehensive device security assessment
- ⚡ **Intent Testing** - Test for Intent-based vulnerabilities
- 🔓 **SSL Pinning** - SSL pinning bypass guidance

### Warning

⚠️ **Educational Purpose Only**: This framework is intended for educational purposes and authorized security testing only. Always obtain proper authorization before testing any applications or devices you do not own.

### Disclaimer

The tools in this repository are provided for educational and authorized security testing purposes only. Users are responsible for complying with applicable laws and regulations. Unauthorized access to computer systems is illegal.

### Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### License

This project is open source and available for educational purposes. 
