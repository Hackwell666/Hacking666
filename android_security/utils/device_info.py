"""
Device Information Utilities

Utilities for gathering Android device information.
"""

from typing import Dict, List, Optional


class DeviceInfo:
    """Gather comprehensive device information"""
    
    def __init__(self, adb_wrapper):
        """
        Initialize DeviceInfo
        
        Args:
            adb_wrapper: Instance of ADBWrapper
        """
        self.adb = adb_wrapper
    
    def get_full_device_info(self) -> Dict[str, str]:
        """
        Get comprehensive device information
        
        Returns:
            Dictionary with device details
        """
        info = self.adb.get_device_info()
        
        # Add additional properties
        additional_props = [
            ('build_id', 'ro.build.id'),
            ('build_fingerprint', 'ro.build.fingerprint'),
            ('product_name', 'ro.product.name'),
            ('board', 'ro.product.board'),
            ('cpu_abi', 'ro.product.cpu.abi'),
            ('kernel_version', 'sys.kernel.version'),
        ]
        
        for key, prop in additional_props:
            stdout, _, _ = self.adb._execute_command(f"shell getprop {prop}")
            info[key] = stdout.strip()
        
        return info
    
    def get_security_info(self) -> Dict[str, str]:
        """
        Get security-related information
        
        Returns:
            Dictionary with security details
        """
        security_info = {}
        
        # Check SELinux status
        selinux = self.adb.shell("getenforce")
        security_info['selinux'] = selinux.strip()
        
        # Check for root
        su_check = self.adb.shell("which su")
        security_info['rooted'] = 'su' in su_check
        
        # Check screen lock
        screen_lock = self.adb.shell("dumpsys window | grep mDreamingLockscreen")
        security_info['screen_lock'] = 'true' in screen_lock.lower()
        
        # Get security patch level
        patch_level = self.adb.shell("getprop ro.build.version.security_patch")
        security_info['security_patch'] = patch_level.strip()
        
        return security_info
    
    def get_installed_apps_info(self) -> List[Dict[str, str]]:
        """
        Get information about installed applications
        
        Returns:
            List of dictionaries with app information
        """
        apps = []
        packages = self.adb.list_packages()
        
        for package in packages[:20]:  # Limit to first 20 for performance
            app_info = {
                'package': package,
                'debuggable': str(self.adb.check_debuggable(package))
            }
            apps.append(app_info)
        
        return apps
    
    def check_adb_over_network(self) -> bool:
        """
        Check if ADB over network is enabled
        
        Returns:
            True if enabled, False otherwise
        """
        tcpip_check = self.adb.shell("getprop service.adb.tcp.port")
        return tcpip_check.strip() != "" and tcpip_check.strip() != "-1"
    
    def get_storage_info(self) -> Dict[str, str]:
        """
        Get storage information
        
        Returns:
            Dictionary with storage details
        """
        storage = {}
        
        # Get disk usage
        df_output = self.adb.shell("df -h /sdcard")
        lines = df_output.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                storage['total'] = parts[1]
                storage['used'] = parts[2]
                storage['available'] = parts[3]
                storage['use_percent'] = parts[4]
        
        return storage
    
    def get_network_info(self) -> Dict[str, str]:
        """
        Get network information
        
        Returns:
            Dictionary with network details
        """
        network = {}
        
        # Get IP address
        ip_output = self.adb.shell("ip addr show wlan0")
        if 'inet ' in ip_output:
            for line in ip_output.split('\n'):
                if 'inet ' in line and '127.0.0.1' not in line:
                    parts = line.strip().split()
                    if len(parts) > 1:
                        network['ip_address'] = parts[1].split('/')[0]
        
        # Get WiFi status
        wifi = self.adb.shell("dumpsys wifi | grep 'Wi-Fi is'")
        network['wifi_enabled'] = 'enabled' in wifi.lower()
        
        return network
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive device information report
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("ANDROID DEVICE INFORMATION REPORT")
        report.append("=" * 60)
        
        # Basic info
        report.append("\n[DEVICE INFORMATION]")
        device_info = self.get_full_device_info()
        for key, value in device_info.items():
            report.append(f"  {key}: {value}")
        
        # Security info
        report.append("\n[SECURITY INFORMATION]")
        security_info = self.get_security_info()
        for key, value in security_info.items():
            report.append(f"  {key}: {value}")
        
        # Storage info
        report.append("\n[STORAGE INFORMATION]")
        storage_info = self.get_storage_info()
        for key, value in storage_info.items():
            report.append(f"  {key}: {value}")
        
        # Network info
        report.append("\n[NETWORK INFORMATION]")
        network_info = self.get_network_info()
        for key, value in network_info.items():
            report.append(f"  {key}: {value}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
