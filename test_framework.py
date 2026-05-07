"""
Basic test suite for Android Security Framework

This file contains basic tests to verify the framework functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from android_security.tools.adb_wrapper import ADBWrapper
from android_security.tools.apk_analyzer import APKAnalyzer
from android_security.exploits.intent_hijacking import IntentHijacker
from android_security.exploits.debug_exploit import DebugExploit
from android_security.utils.logger import setup_logger, log_success, log_info, log_error
from android_security.utils.device_info import DeviceInfo


def test_imports():
    """Test that all modules can be imported"""
    try:
        log_info("Testing module imports...")
        
        # Try importing all main classes
        from android_security.tools import ADBWrapper, APKAnalyzer
        from android_security.exploits import IntentHijacker, DebugExploit
        from android_security.utils import setup_logger, DeviceInfo
        
        log_success("All modules imported successfully")
        return True
    except Exception as e:
        log_error(f"Import test failed: {e}")
        return False


def test_adb_wrapper():
    """Test ADB Wrapper initialization"""
    try:
        log_info("Testing ADB Wrapper...")
        
        # Initialize without device ID
        adb = ADBWrapper()
        assert adb is not None
        assert adb.adb_command == "adb"
        
        # Initialize with device ID
        adb_with_device = ADBWrapper("emulator-5554")
        assert adb_with_device.adb_command == "adb -s emulator-5554"
        
        log_success("ADB Wrapper tests passed")
        return True
    except Exception as e:
        log_error(f"ADB Wrapper test failed: {e}")
        return False


def test_intent_hijacker():
    """Test Intent Hijacker initialization"""
    try:
        log_info("Testing Intent Hijacker...")
        
        adb = ADBWrapper()
        hijacker = IntentHijacker(adb)
        assert hijacker is not None
        assert hijacker.adb == adb
        
        # Test PoC generation
        poc = hijacker.generate_poc_intent("com.example/.MainActivity", "sql_injection")
        assert "am start" in poc
        assert "com.example/.MainActivity" in poc
        
        log_success("Intent Hijacker tests passed")
        return True
    except Exception as e:
        log_error(f"Intent Hijacker test failed: {e}")
        return False


def test_debug_exploit():
    """Test Debug Exploit initialization"""
    try:
        log_info("Testing Debug Exploit...")
        
        adb = ADBWrapper()
        debug = DebugExploit(adb)
        assert debug is not None
        assert debug.adb == adb
        
        log_success("Debug Exploit tests passed")
        return True
    except Exception as e:
        log_error(f"Debug Exploit test failed: {e}")
        return False


def test_device_info():
    """Test Device Info initialization"""
    try:
        log_info("Testing Device Info...")
        
        adb = ADBWrapper()
        device_info = DeviceInfo(adb)
        assert device_info is not None
        assert device_info.adb == adb
        
        log_success("Device Info tests passed")
        return True
    except Exception as e:
        log_error(f"Device Info test failed: {e}")
        return False


def test_logger():
    """Test logging utilities"""
    try:
        log_info("Testing Logger...")
        
        logger = setup_logger()
        assert logger is not None
        
        # Test colored logging functions
        log_success("This is a success message")
        log_info("This is an info message")
        log_error("This is an error message")
        
        log_success("Logger tests passed")
        return True
    except Exception as e:
        log_error(f"Logger test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Android Security Framework - Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("ADB Wrapper", test_adb_wrapper),
        ("Intent Hijacker", test_intent_hijacker),
        ("Debug Exploit", test_debug_exploit),
        ("Device Info", test_device_info),
        ("Logger", test_logger),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            log_error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
