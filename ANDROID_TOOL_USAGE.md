# Android Security Testing Tool - Usage Guide

## Overview
The Android Security Testing Tool is a comprehensive Python-based security assessment utility designed for penetration testing and vulnerability assessment of Android devices via ADB (Android Debug Bridge).

## Prerequisites

### Required Software
1. **Python 3.x** - Must be installed on your system
2. **Android Debug Bridge (ADB)** - Required for device communication

### Installing ADB

#### Windows
```bash
# Download Android Platform Tools from:
# https://developer.android.com/studio/releases/platform-tools

# Extract and add to PATH
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install adb
```

#### macOS
```bash
brew install android-platform-tools
```

### Verify ADB Installation
```bash
adb version
```

## Device Setup

### 1. Enable Developer Options on Android Device
1. Go to Settings → About Phone
2. Tap "Build Number" 7 times
3. Developer Options will be enabled

### 2. Enable USB Debugging
1. Go to Settings → Developer Options
2. Enable "USB Debugging"
3. Connect device via USB cable

### 3. Authorize Computer
When you connect your device, you'll see a prompt on the device asking to authorize the computer. Tap "Allow" or "OK".

### 4. Verify Connection
```bash
adb devices
```
You should see your device listed.

## Running the Tool

### Basic Usage
```bash
python Android_Security_Testing.py
```

### Features and Operations

#### 1. Extract Device Information
- Retrieves Android version, SDK level, manufacturer, model
- Checks if device is rooted
- Displays comprehensive device fingerprint

#### 2. List Installed Packages
- Enumerates all installed applications
- Shows system and user apps
- Useful for identifying attack surface

#### 3. Analyze App Permissions
- Examines requested permissions for any app
- Identifies granted permissions
- Highlights dangerous permissions (location, camera, SMS, contacts, etc.)

Example:
```
Enter package name: com.example.app
```

#### 4. Check for Debuggable Apps
- Scans all installed apps for debuggable flag
- Debuggable apps can be exploited for code injection
- Critical security vulnerability indicator

#### 5. Scan for Vulnerabilities
Automated scan that checks for:
- **Critical**: Outdated Android versions (SDK < 23)
- **High**: Old Android versions, no screen lock, debuggable apps
- **Medium**: Rooted devices, excessive permissions
- **Low**: Other security concerns

#### 6. Generate Security Report
Creates a comprehensive text report including:
- Complete device information
- Installed packages (up to 50)
- Vulnerability assessment with severity ratings
- Timestamped for audit trail

Output: `android_security_report.txt`

#### 7. Pull App Data
Attempts to backup and extract application data:
```
Enter package name: com.example.app
Enter output directory: ./backups
```

**Note**: Requires user confirmation on device and proper permissions.

## Security Testing Scenarios

### Scenario 1: Initial Device Assessment
1. Extract device information (option 1)
2. Scan for vulnerabilities (option 5)
3. Generate security report (option 6)

### Scenario 2: Application Analysis
1. List installed packages (option 2)
2. Analyze permissions for suspicious apps (option 3)
3. Check if apps are debuggable (option 4)

### Scenario 3: Data Extraction
1. Identify target application
2. Analyze its permissions
3. Attempt to pull app data (option 7)

### Scenario 4: Comprehensive Audit
Run all options in sequence for complete security assessment.

## Example Output

### Device Information
```
Android Version: 11
Model: Pixel 4
Manufacturer: Google
SDK Version: 30
Rooted: False
```

### Vulnerability Scan
```
CRITICAL:
  [!] None found

HIGH:
  [!] Found 3 debuggable apps
  [!] No screen lock enabled

MEDIUM:
  [!] 5 apps with excessive dangerous permissions

LOW:
  [!] None found
```

## Security Considerations

### Legal and Ethical Use
⚠️ **WARNING**: This tool must only be used for:
- Authorized security testing
- Your own devices
- Educational purposes with proper permission
- Professional penetration testing with written authorization

### Unauthorized Use is Illegal
Using this tool without proper authorization is:
- Illegal in most jurisdictions
- Violation of computer fraud laws
- Potential criminal offense
- Unethical and harmful

### Best Practices
1. **Always obtain written permission** before testing any device
2. **Use in isolated test environments** when possible
3. **Document all testing activities** for audit trail
4. **Report vulnerabilities responsibly** to device/app owners
5. **Do not retain sensitive data** extracted during testing

## Troubleshooting

### ADB Not Found
```
[!] ERROR: ADB is not installed or not in PATH
```
**Solution**: Install ADB and ensure it's in your system PATH

### No Devices Connected
```
[!] No Android devices connected via ADB
```
**Solution**: 
- Check USB cable connection
- Enable USB debugging on device
- Authorize computer on device
- Try different USB port
- Run `adb devices` to verify

### Device Unauthorized
```
List of devices attached
ABC123    unauthorized
```
**Solution**: Check device screen for authorization prompt and tap "Allow"

### Permission Denied
Some operations may fail without root access or proper permissions. This is expected behavior for security-protected data.

## Advanced Usage

### Testing Multiple Devices
The tool can work with multiple connected devices. It will list all connected devices and default to the first one. You can modify the code to select specific devices.

### Automated Scanning
For batch scanning, you can modify the script to run specific checks non-interactively:

```python
from Android_Security_Testing import AndroidSecurityTester

tester = AndroidSecurityTester()
if tester.connect_to_device():
    tester.generate_report("device_report.txt")
```

### Integration with Other Tools
The output can be integrated with:
- Security information and event management (SIEM) systems
- Automated testing pipelines
- Compliance reporting tools

## Support and Resources

### Official Android Security Resources
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [Android Permissions Overview](https://developer.android.com/guide/topics/permissions/overview)

### ADB Documentation
- [Android Debug Bridge Documentation](https://developer.android.com/studio/command-line/adb)

### Security Testing Resources
- OWASP Mobile Security Testing Guide
- Android Application Security Testing Framework

## Disclaimer
This tool is provided for educational and authorized security testing purposes only. The authors and contributors are not responsible for any misuse or damage caused by this tool. Users must comply with all applicable laws and regulations regarding computer security and privacy. Always obtain proper authorization before conducting any security testing.

---

**Written for security research and penetration testing purposes**
**Use responsibly and ethically**
