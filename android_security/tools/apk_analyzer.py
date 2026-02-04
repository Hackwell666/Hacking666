"""
APK Analyzer

Tools for analyzing Android APK files for security vulnerabilities.
"""

import zipfile
import os
import re
from typing import List, Dict, Optional


class APKAnalyzer:
    """Analyze APK files for security issues"""
    
    def __init__(self, apk_path: str):
        """
        Initialize APK analyzer
        
        Args:
            apk_path: Path to APK file
        """
        self.apk_path = apk_path
        self.manifest = None
        self.permissions = []
        self.activities = []
        self.services = []
        self.receivers = []
        
        if not os.path.exists(apk_path):
            raise FileNotFoundError(f"APK file not found: {apk_path}")
    
    def extract_apk(self, output_dir: str) -> bool:
        """
        Extract APK contents
        
        Args:
            output_dir: Directory to extract to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            return True
        except Exception as e:
            print(f"Error extracting APK: {e}")
            return False
    
    def get_permissions(self) -> List[str]:
        """
        Extract permissions from APK
        
        Returns:
            List of permissions
        """
        # This is a simplified version - real implementation would need aapt or androguard
        permissions = []
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as apk:
                # In real implementation, we'd parse AndroidManifest.xml properly
                # This is a placeholder showing the concept
                if 'AndroidManifest.xml' in apk.namelist():
                    # Would need to decode binary XML format
                    pass
        except Exception as e:
            print(f"Error reading permissions: {e}")
        
        return permissions
    
    def check_dangerous_permissions(self) -> List[str]:
        """
        Check for dangerous permissions
        
        Returns:
            List of dangerous permissions found
        """
        dangerous_perms = [
            'READ_CONTACTS', 'WRITE_CONTACTS', 'READ_SMS', 'SEND_SMS',
            'RECEIVE_SMS', 'READ_CALL_LOG', 'WRITE_CALL_LOG',
            'CAMERA', 'RECORD_AUDIO', 'ACCESS_FINE_LOCATION',
            'ACCESS_COARSE_LOCATION', 'READ_EXTERNAL_STORAGE',
            'WRITE_EXTERNAL_STORAGE', 'CALL_PHONE'
        ]
        
        found_permissions = self.get_permissions()
        dangerous_found = []
        
        for perm in found_permissions:
            for dangerous in dangerous_perms:
                if dangerous in perm:
                    dangerous_found.append(perm)
        
        return dangerous_found
    
    def scan_for_hardcoded_secrets(self, extracted_dir: str) -> List[Dict[str, str]]:
        """
        Scan for hardcoded secrets in the APK
        
        Args:
            extracted_dir: Directory with extracted APK contents
            
        Returns:
            List of potential secrets found
        """
        secrets = []
        
        # Common patterns for secrets
        patterns = {
            'API_KEY': r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]+)["\']',
            'PASSWORD': r'password["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            'TOKEN': r'token["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]+)["\']',
            'SECRET': r'secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]+)["\']',
        }
        
        # Scan relevant files
        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                if file.endswith(('.xml', '.java', '.smali', '.js')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            for secret_type, pattern in patterns.items():
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    secrets.append({
                                        'type': secret_type,
                                        'value': match.group(1),
                                        'file': file_path,
                                        'line': content[:match.start()].count('\n') + 1
                                    })
                    except Exception:
                        pass
        
        return secrets
    
    def check_backup_allowed(self) -> bool:
        """
        Check if backup is allowed in manifest
        
        Returns:
            True if backup is allowed, False otherwise
        """
        # Placeholder - would need to parse manifest
        return True
    
    def check_debuggable(self) -> bool:
        """
        Check if app is debuggable
        
        Returns:
            True if debuggable, False otherwise
        """
        # Placeholder - would need to parse manifest
        return False
    
    def find_exported_components(self) -> Dict[str, List[str]]:
        """
        Find exported components (activities, services, receivers)
        
        Returns:
            Dictionary with lists of exported components
        """
        exported = {
            'activities': [],
            'services': [],
            'receivers': [],
            'providers': []
        }
        
        # Placeholder - would need to parse manifest
        return exported
    
    def security_report(self, extracted_dir: Optional[str] = None) -> Dict:
        """
        Generate a comprehensive security report
        
        Args:
            extracted_dir: Optional directory with extracted APK
            
        Returns:
            Security report dictionary
        """
        report = {
            'apk_path': self.apk_path,
            'dangerous_permissions': self.check_dangerous_permissions(),
            'backup_allowed': self.check_backup_allowed(),
            'debuggable': self.check_debuggable(),
            'exported_components': self.find_exported_components(),
            'secrets': []
        }
        
        if extracted_dir and os.path.exists(extracted_dir):
            report['secrets'] = self.scan_for_hardcoded_secrets(extracted_dir)
        
        return report
