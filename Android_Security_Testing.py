# Android Security Testing and Exploitation Tool
# This script provides various Android security testing capabilities using ADB
# For educational and authorized security testing purposes only

import subprocess
import re
import time
import os
import sys
from typing import List, Dict, Optional

# Constants
DANGEROUS_PERMISSIONS = [
    'READ_CONTACTS', 'WRITE_CONTACTS', 'READ_SMS', 'SEND_SMS',
    'READ_CALL_LOG', 'CAMERA', 'RECORD_AUDIO', 'ACCESS_FINE_LOCATION',
    'ACCESS_COARSE_LOCATION', 'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE'
]

MAX_PACKAGES_TO_CHECK = 20
MAX_PACKAGES_TO_REPORT = 50

class AndroidSecurityTester:
    """
    Android Security Testing Tool for penetration testing and vulnerability assessment
    """
    
    def __init__(self):
        self.device_id = None
        self.connected_devices = []
        
    def check_adb_installed(self) -> bool:
        """Check if ADB is installed on the system"""
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected Android devices"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            self.connected_devices = devices
            return devices
        except Exception as e:
            print(f"Error getting devices: {e}")
            return []
    
    def connect_to_device(self, device_id: Optional[str] = None) -> bool:
        """Connect to specific device or first available device"""
        if not device_id:
            devices = self.get_connected_devices()
            if not devices:
                print("No devices connected!")
                return False
            device_id = devices[0]
        
        self.device_id = device_id
        print(f"Connected to device: {device_id}")
        return True
    
    def extract_installed_packages(self) -> List[str]:
        """Extract all installed packages from device"""
        if not self.device_id:
            print("No device connected!")
            return []
        
        try:
            cmd = ['adb', '-s', self.device_id, 'shell', 'pm', 'list', 'packages']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            packages = []
            for line in result.stdout.strip().split('\n'):
                if line.startswith('package:'):
                    packages.append(line.replace('package:', '').strip())
            print(f"Found {len(packages)} installed packages")
            return packages
        except Exception as e:
            print(f"Error extracting packages: {e}")
            return []
    
    def analyze_app_permissions(self, package_name: str) -> Dict[str, List[str]]:
        """Analyze permissions for a specific app"""
        if not self.device_id:
            print("No device connected!")
            return {}
        
        try:
            cmd = ['adb', '-s', self.device_id, 'shell', 'dumpsys', 'package', package_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            permissions = {
                'requested': [],
                'granted': [],
                'dangerous': []
            }
            
            lines = result.stdout.split('\n')
            in_permissions_section = False
            
            for line in lines:
                if 'requested permissions:' in line.lower():
                    in_permissions_section = True
                    continue
                
                if in_permissions_section:
                    if line.strip().startswith('android.permission.'):
                        perm = line.strip()
                        permissions['requested'].append(perm)
                        
                        # Check if granted
                        if 'granted=true' in line:
                            permissions['granted'].append(perm)
                        
                        # Check if dangerous
                        for dangerous_perm in DANGEROUS_PERMISSIONS:
                            if dangerous_perm in perm:
                                permissions['dangerous'].append(perm)
                                break
                    elif line.strip() and not line.strip().startswith('android.'):
                        in_permissions_section = False
            
            return permissions
        except Exception as e:
            print(f"Error analyzing permissions: {e}")
            return {}
    
    def check_debuggable_apps(self) -> List[str]:
        """Find debuggable applications on the device"""
        if not self.device_id:
            print("No device connected!")
            return []
        
        try:
            packages = self.extract_installed_packages()
            debuggable = []
            
            print("Checking for debuggable apps...")
            for package in packages:
                cmd = ['adb', '-s', self.device_id, 'shell', 'dumpsys', 'package', package]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if 'debuggable=true' in result.stdout.lower():
                    debuggable.append(package)
                    print(f"  [!] Debuggable: {package}")
            
            return debuggable
        except Exception as e:
            print(f"Error checking debuggable apps: {e}")
            return []
    
    def extract_device_info(self) -> Dict[str, str]:
        """Extract device information"""
        if not self.device_id:
            print("No device connected!")
            return {}
        
        info = {}
        
        try:
            # Get Android version
            cmd = ['adb', '-s', self.device_id, 'shell', 'getprop', 'ro.build.version.release']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            info['android_version'] = result.stdout.strip()
            
            # Get device model
            cmd = ['adb', '-s', self.device_id, 'shell', 'getprop', 'ro.product.model']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            info['model'] = result.stdout.strip()
            
            # Get device manufacturer
            cmd = ['adb', '-s', self.device_id, 'shell', 'getprop', 'ro.product.manufacturer']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            info['manufacturer'] = result.stdout.strip()
            
            # Get SDK version
            cmd = ['adb', '-s', self.device_id, 'shell', 'getprop', 'ro.build.version.sdk']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            info['sdk_version'] = result.stdout.strip()
            
            # Check if rooted
            cmd = ['adb', '-s', self.device_id, 'shell', 'su', '-c', 'id']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            info['rooted'] = 'uid=0' in result.stdout
            
            return info
        except Exception as e:
            print(f"Error extracting device info: {e}")
            return info
    
    def pull_app_data(self, package_name: str, output_dir: str) -> bool:
        """Attempt to pull application data (requires root or backup permissions)"""
        if not self.device_id:
            print("No device connected!")
            return False
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Try to backup app data
            backup_file = os.path.join(output_dir, f"{package_name}.ab")
            cmd = ['adb', '-s', self.device_id, 'backup', '-f', backup_file, package_name]
            
            print(f"Attempting to backup {package_name}...")
            print("Please confirm backup on device if prompted...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                print(f"Successfully backed up {package_name} to {backup_file}")
                return True
            else:
                print(f"Failed to backup {package_name}")
                return False
        except Exception as e:
            print(f"Error pulling app data: {e}")
            return False
    
    def check_screen_lock(self) -> bool:
        """Check if device has screen lock enabled"""
        if not self.device_id:
            print("No device connected!")
            return False
        
        try:
            cmd = ['adb', '-s', self.device_id, 'shell', 'dumpsys', 'window']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Check for lock screen indicators
            is_locked = 'mShowingLockscreen=true' in result.stdout or 'isScreenLocked=true' in result.stdout
            return is_locked
        except Exception as e:
            print(f"Error checking screen lock: {e}")
            return False
    
    def scan_for_vulnerabilities(self) -> Dict[str, List[str]]:
        """Scan device for common security vulnerabilities"""
        if not self.device_id:
            print("No device connected!")
            return {}
        
        vulnerabilities = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        print("\n[*] Starting vulnerability scan...")
        
        # Check for debuggable apps
        debuggable = self.check_debuggable_apps()
        if debuggable:
            vulnerabilities['high'].append(f"Found {len(debuggable)} debuggable apps")
        
        # Check device info
        info = self.extract_device_info()
        
        # Check for old Android version
        if info.get('sdk_version'):
            sdk = int(info['sdk_version'])
            if sdk < 23:  # Android 6.0
                vulnerabilities['critical'].append(f"Outdated Android version (SDK {sdk})")
            elif sdk < 28:  # Android 9.0
                vulnerabilities['high'].append(f"Old Android version (SDK {sdk})")
        
        # Check if rooted
        if info.get('rooted'):
            vulnerabilities['medium'].append("Device is rooted")
        
        # Check screen lock
        if not self.check_screen_lock():
            vulnerabilities['high'].append("No screen lock enabled")
        
        # Check for apps with dangerous permissions
        packages = self.extract_installed_packages()
        dangerous_apps = 0
        for package in packages[:MAX_PACKAGES_TO_CHECK]:
            perms = self.analyze_app_permissions(package)
            if len(perms.get('dangerous', [])) > 5:
                dangerous_apps += 1
        
        if dangerous_apps > 0:
            vulnerabilities['medium'].append(f"{dangerous_apps} apps with excessive dangerous permissions")
        
        return vulnerabilities
    
    def generate_report(self, output_file: str = "android_security_report.txt"):
        """Generate comprehensive security report"""
        if not self.device_id:
            print("No device connected!")
            return
        
        print("\n[*] Generating security report...")
        
        with open(output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("ANDROID SECURITY ASSESSMENT REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            # Device Info
            f.write("DEVICE INFORMATION\n")
            f.write("-" * 70 + "\n")
            info = self.extract_device_info()
            for key, value in info.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            # Installed Packages
            f.write("INSTALLED PACKAGES\n")
            f.write("-" * 70 + "\n")
            packages = self.extract_installed_packages()
            f.write(f"Total packages: {len(packages)}\n")
            for package in packages[:MAX_PACKAGES_TO_REPORT]:
                f.write(f"  - {package}\n")
            f.write("\n")
            
            # Vulnerabilities
            f.write("VULNERABILITY SCAN RESULTS\n")
            f.write("-" * 70 + "\n")
            vulns = self.scan_for_vulnerabilities()
            
            for severity in ['critical', 'high', 'medium', 'low']:
                if vulns.get(severity):
                    f.write(f"\n{severity.upper()} SEVERITY:\n")
                    for vuln in vulns[severity]:
                        f.write(f"  [!] {vuln}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("Report generated at: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("=" * 70 + "\n")
        
        print(f"\n[+] Report saved to: {output_file}")


def main():
    """Main function to run Android security testing"""
    print("=" * 70)
    print("ANDROID SECURITY TESTING TOOL")
    print("For educational and authorized testing purposes only")
    print("=" * 70)
    print()
    
    tester = AndroidSecurityTester()
    
    # Check if ADB is installed
    if not tester.check_adb_installed():
        print("[!] ERROR: ADB is not installed or not in PATH")
        print("    Please install Android Debug Bridge (ADB) to use this tool")
        sys.exit(1)
    
    # Get connected devices
    devices = tester.get_connected_devices()
    if not devices:
        print("[!] No Android devices connected via ADB")
        print("    Please connect a device and enable USB debugging")
        sys.exit(1)
    
    print(f"[+] Found {len(devices)} device(s)")
    for i, device in enumerate(devices):
        print(f"    [{i}] {device}")
    
    # Connect to first device
    tester.connect_to_device(devices[0])
    
    # Main menu
    while True:
        print("\n" + "=" * 70)
        print("SELECT OPERATION:")
        print("=" * 70)
        print("1. Extract device information")
        print("2. List installed packages")
        print("3. Analyze app permissions")
        print("4. Check for debuggable apps")
        print("5. Scan for vulnerabilities")
        print("6. Generate security report")
        print("7. Pull app data (requires permissions)")
        print("8. Exit")
        print()
        
        try:
            choice = input("Enter choice (1-8): ").strip()
            
            if choice == '1':
                print("\n[*] Extracting device information...")
                info = tester.extract_device_info()
                for key, value in info.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            elif choice == '2':
                print("\n[*] Extracting installed packages...")
                packages = tester.extract_installed_packages()
                for package in packages:
                    print(f"  - {package}")
            
            elif choice == '3':
                package = input("Enter package name: ").strip()
                print(f"\n[*] Analyzing permissions for {package}...")
                perms = tester.analyze_app_permissions(package)
                print(f"\n  Requested: {len(perms.get('requested', []))}")
                print(f"  Granted: {len(perms.get('granted', []))}")
                print(f"  Dangerous: {len(perms.get('dangerous', []))}")
                if perms.get('dangerous'):
                    print("\n  Dangerous permissions:")
                    for perm in perms['dangerous']:
                        print(f"    - {perm}")
            
            elif choice == '4':
                debuggable = tester.check_debuggable_apps()
                print(f"\n[+] Found {len(debuggable)} debuggable apps")
            
            elif choice == '5':
                vulns = tester.scan_for_vulnerabilities()
                print("\n[*] Vulnerability scan complete!")
                for severity in ['critical', 'high', 'medium', 'low']:
                    if vulns.get(severity):
                        print(f"\n  {severity.upper()}:")
                        for vuln in vulns[severity]:
                            print(f"    [!] {vuln}")
            
            elif choice == '6':
                output = input("Enter output filename (default: android_security_report.txt): ").strip()
                if not output:
                    output = "android_security_report.txt"
                tester.generate_report(output)
            
            elif choice == '7':
                package = input("Enter package name: ").strip()
                output_dir = input("Enter output directory (default: ./backup): ").strip()
                if not output_dir:
                    output_dir = "./backup"
                tester.pull_app_data(package, output_dir)
            
            elif choice == '8':
                print("\n[*] Exiting...")
                break
            
            else:
                print("\n[!] Invalid choice!")
        
        except KeyboardInterrupt:
            print("\n\n[*] Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n[!] Error: {e}")
    
    print("\n" + "=" * 70)
    print("DISCLAIMER: This tool is for educational and authorized testing only.")
    print("Unauthorized access to devices is illegal and unethical.")
    print("Written for security research and penetration testing purposes.")
    print("=" * 70)


if __name__ == "__main__":
    main()
