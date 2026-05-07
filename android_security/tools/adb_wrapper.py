"""
ADB (Android Debug Bridge) Wrapper

A Python wrapper for Android Debug Bridge commands to interact with Android devices.
"""

import subprocess
from typing import List, Optional, Dict


class ADBWrapper:
    """Wrapper class for ADB commands"""
    
    def __init__(self, device_id: Optional[str] = None):
        """
        Initialize ADB wrapper
        
        Args:
            device_id: Specific device ID to target (optional)
        """
        self.device_id = device_id
        self.adb_command = "adb"
        if device_id:
            self.adb_command = f"adb -s {device_id}"
    
    def _execute_command(self, command: str) -> tuple:
        """
        Execute an ADB command
        
        Args:
            command: ADB command to execute
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        full_command = f"{self.adb_command} {command}"
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1
    
    def list_devices(self) -> List[str]:
        """
        List all connected Android devices
        
        Returns:
            List of device IDs
        """
        stdout, _, _ = self._execute_command("devices")
        devices = []
        for line in stdout.split('\n')[1:]:  # Skip header
            if line.strip() and '\tdevice' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        return devices
    
    def install_apk(self, apk_path: str) -> bool:
        """
        Install an APK on the device
        
        Args:
            apk_path: Path to APK file
            
        Returns:
            True if successful, False otherwise
        """
        _, stderr, returncode = self._execute_command(f"install {apk_path}")
        return returncode == 0
    
    def uninstall_package(self, package_name: str) -> bool:
        """
        Uninstall a package from the device
        
        Args:
            package_name: Package name to uninstall
            
        Returns:
            True if successful, False otherwise
        """
        _, _, returncode = self._execute_command(f"uninstall {package_name}")
        return returncode == 0
    
    def list_packages(self) -> List[str]:
        """
        List all installed packages
        
        Returns:
            List of package names
        """
        stdout, _, _ = self._execute_command("shell pm list packages")
        packages = []
        for line in stdout.split('\n'):
            if line.startswith('package:'):
                packages.append(line.replace('package:', '').strip())
        return packages
    
    def get_device_info(self) -> Dict[str, str]:
        """
        Get device information
        
        Returns:
            Dictionary with device information
        """
        info = {}
        
        # Get Android version
        stdout, _, _ = self._execute_command("shell getprop ro.build.version.release")
        info['android_version'] = stdout.strip()
        
        # Get device model
        stdout, _, _ = self._execute_command("shell getprop ro.product.model")
        info['model'] = stdout.strip()
        
        # Get manufacturer
        stdout, _, _ = self._execute_command("shell getprop ro.product.manufacturer")
        info['manufacturer'] = stdout.strip()
        
        # Get SDK version
        stdout, _, _ = self._execute_command("shell getprop ro.build.version.sdk")
        info['sdk_version'] = stdout.strip()
        
        return info
    
    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """
        Pull a file from device to local machine
        
        Args:
            remote_path: Path on device
            local_path: Local destination path
            
        Returns:
            True if successful, False otherwise
        """
        _, _, returncode = self._execute_command(f"pull {remote_path} {local_path}")
        return returncode == 0
    
    def push_file(self, local_path: str, remote_path: str) -> bool:
        """
        Push a file from local machine to device
        
        Args:
            local_path: Local file path
            remote_path: Destination path on device
            
        Returns:
            True if successful, False otherwise
        """
        _, _, returncode = self._execute_command(f"push {local_path} {remote_path}")
        return returncode == 0
    
    def shell(self, command: str) -> str:
        """
        Execute a shell command on the device
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output
        """
        stdout, _, _ = self._execute_command(f"shell {command}")
        return stdout
    
    def logcat(self, filter_string: Optional[str] = None, lines: int = 100) -> str:
        """
        Get device logcat
        
        Args:
            filter_string: Optional filter for logcat
            lines: Number of lines to retrieve
            
        Returns:
            Logcat output
        """
        command = f"logcat -d -t {lines}"
        if filter_string:
            command += f" | grep {filter_string}"
        stdout, _, _ = self._execute_command(command)
        return stdout
    
    def check_debuggable(self, package_name: str) -> bool:
        """
        Check if an app is debuggable
        
        Args:
            package_name: Package name to check
            
        Returns:
            True if debuggable, False otherwise
        """
        stdout = self.shell(f"dumpsys package {package_name}")
        return "android:debuggable" in stdout and "true" in stdout
