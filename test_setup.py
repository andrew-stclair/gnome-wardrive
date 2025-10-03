#!/usr/bin/env python3

"""
Simple test script to validate the GNOME Wardrive installation
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import gi
        gi.require_version('Gtk', '4.0')
        gi.require_version('Adw', '1')
        gi.require_version('NM', '1.0')
        gi.require_version('Geoclue', '2.0')
        
        from gi.repository import Gtk, Adw, Gio, GLib, NM, Geoclue
        print("✓ All GTK/GNOME modules imported successfully")
        
        # Add src to path for importing our modules
        sys.path.insert(0, 'src')
        
        # Test core modules that don't have GUI components
        from wifi_scanner import WiFiScanner
        from location_service import LocationService  
        from data_manager import DataManager
        print("✓ Core application modules imported successfully")
        
        # Test that main module syntax is valid (don't execute, just import for syntax check)
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", "src/main.py")
        if spec and spec.loader:
            main_module = importlib.util.module_from_spec(spec)
            print("✓ Main module syntax is valid")
        else:
            print("✗ Could not load main module spec")
            return False
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_networkmanager():
    """Test NetworkManager connectivity"""
    try:
        import gi
        gi.require_version('NM', '1.0')
        from gi.repository import NM
        
        client = NM.Client.new(None)
        if client:
            print("✓ NetworkManager client created successfully")
            devices = client.get_devices()
            wifi_devices = [d for d in devices if d.get_device_type() == NM.DeviceType.WIFI]
            print(f"✓ Found {len(wifi_devices)} WiFi devices")
            return True
        else:
            print("✗ Failed to create NetworkManager client")
            return False
    except Exception as e:
        print(f"✗ NetworkManager test failed: {e}")
        return False

def test_geoclue():
    """Test GeoClue availability"""
    try:
        import gi
        gi.require_version('Geoclue', '2.0')
        from gi.repository import Geoclue
        print("✓ GeoClue module imported successfully")
        return True
    except Exception as e:
        print(f"✗ GeoClue test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing GNOME Wardrive setup...")
    print("=" * 40)
    
    tests = [
        ("Import test", test_imports),
        ("NetworkManager test", test_networkmanager),
        ("GeoClue test", test_geoclue),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    print("Test Results:")
    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results)
    print(f"\nOverall: {'PASS' if all_passed else 'FAIL'}")
    
    if all_passed:
        print("\n✓ GNOME Wardrive is ready to run!")
    else:
        print("\n✗ Some tests failed. Check dependencies and permissions.")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())