"""
Example usage of Android Security Testing Framework

This script demonstrates how to use the various tools and exploits
in the android_security package.
"""

from android_security.tools.adb_wrapper import ADBWrapper
from android_security.tools.apk_analyzer import APKAnalyzer
from android_security.exploits.intent_hijacking import IntentHijacker
from android_security.exploits.debug_exploit import DebugExploit
from android_security.utils.logger import setup_logger, log_info, log_success, log_error
from android_security.utils.device_info import DeviceInfo


def example_adb_usage():
    """Example: Using ADB Wrapper"""
    log_info("Example 1: ADB Wrapper Usage")
    
    # Initialize ADB wrapper
    adb = ADBWrapper()
    
    # List connected devices
    devices = adb.list_devices()
    log_success(f"Connected devices: {devices}")
    
    # Get device information
    if devices:
        info = adb.get_device_info()
        log_success(f"Device info: {info}")
        
        # List installed packages
        packages = adb.list_packages()
        log_success(f"Found {len(packages)} installed packages")
        
        # Check if a specific app is debuggable
        if packages:
            is_debuggable = adb.check_debuggable(packages[0])
            log_info(f"{packages[0]} debuggable: {is_debuggable}")


def example_apk_analysis():
    """Example: APK Analysis"""
    log_info("Example 2: APK Analysis")
    
    # Note: Replace with actual APK path
    apk_path = "/path/to/app.apk"
    
    try:
        analyzer = APKAnalyzer(apk_path)
        
        # Extract APK
        analyzer.extract_apk("/tmp/apk_extracted")
        
        # Check for dangerous permissions
        dangerous_perms = analyzer.check_dangerous_permissions()
        log_info(f"Dangerous permissions: {dangerous_perms}")
        
        # Generate security report
        report = analyzer.security_report("/tmp/apk_extracted")
        log_success("Security report generated")
        print(report)
        
    except FileNotFoundError:
        log_error(f"APK file not found: {apk_path}")


def example_intent_hijacking():
    """Example: Intent Hijacking"""
    log_info("Example 3: Intent Hijacking")
    
    adb = ADBWrapper()
    devices = adb.list_devices()
    
    if not devices:
        log_error("No devices connected")
        return
    
    hijacker = IntentHijacker(adb)
    
    # Find exported activities for a package
    package_name = "com.example.app"  # Replace with actual package
    activities = hijacker.find_exported_activities(package_name)
    log_info(f"Exported activities: {activities}")
    
    # Test deeplink vulnerability
    deeplink = "myapp://open?url=https://evil.com"
    result = hijacker.test_deeplink_vulnerability(package_name, deeplink)
    log_info(f"Deeplink test result: {result}")


def example_debug_exploit():
    """Example: Debug Exploitation"""
    log_info("Example 4: Debug Exploitation")
    
    adb = ADBWrapper()
    devices = adb.list_devices()
    
    if not devices:
        log_error("No devices connected")
        return
    
    debug_exploit = DebugExploit(adb)
    
    # Check if app is debuggable
    package_name = "com.example.app"  # Replace with actual package
    is_debuggable = debug_exploit.check_if_debuggable(package_name)
    log_info(f"{package_name} is debuggable: {is_debuggable}")
    
    if is_debuggable:
        # Get JDWP monitoring info
        jdwp_info = debug_exploit.monitor_jdwp(package_name)
        log_success(f"JDWP info: {jdwp_info}")
        
        # Get shared libraries
        libraries = debug_exploit.get_shared_libraries(package_name)
        log_info(f"Loaded libraries: {libraries}")


def example_device_info():
    """Example: Device Information Gathering"""
    log_info("Example 5: Device Information Gathering")
    
    adb = ADBWrapper()
    devices = adb.list_devices()
    
    if not devices:
        log_error("No devices connected")
        return
    
    device_info = DeviceInfo(adb)
    
    # Generate comprehensive report
    report = device_info.generate_report()
    print(report)
    
    # Get security-specific information
    security_info = device_info.get_security_info()
    log_success(f"Security info: {security_info}")


def main():
    """Main function to run all examples"""
    # Setup logger
    logger = setup_logger()
    
    print("\n" + "="*60)
    print("Android Security Testing Framework - Examples")
    print("="*60 + "\n")
    
    # Run examples (comment out as needed)
    try:
        example_adb_usage()
    except Exception as e:
        log_error(f"ADB example failed: {e}")
    
    print("\n" + "-"*60 + "\n")
    
    try:
        example_device_info()
    except Exception as e:
        log_error(f"Device info example failed: {e}")
    
    # Uncomment to run other examples:
    # example_apk_analysis()
    # example_intent_hijacking()
    # example_debug_exploit()


if __name__ == "__main__":
    main()
