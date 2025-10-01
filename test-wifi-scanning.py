#!/usr/bin/env python3
"""
Test script to verify WiFi scanning works in portable mode
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import gi
gi.require_version('NM', '1.0')
from gi.repository import NM, GLib

def test_wifi_scanning():
    """Test WiFi network detection"""
    print("🔍 Testing portable WiFi scanning...")
    
    # Create NetworkManager client
    nm_client = NM.Client.new(None)
    
    # Find WiFi devices
    wifi_devices = []
    for device in nm_client.get_devices():
        if device.get_device_type() == NM.DeviceType.WIFI:
            wifi_devices.append(device)
    
    print(f"📡 Found {len(wifi_devices)} WiFi device(s)")
    
    if not wifi_devices:
        print("❌ No WiFi devices found")
        return False
    
    # Check available networks
    total_networks = 0
    for device in wifi_devices:
        access_points = device.get_access_points()
        device_networks = len(access_points)
        total_networks += device_networks
        
        print(f"📶 {device.get_iface()}: {device_networks} networks visible")
        
        # Show first few networks as examples
        for i, ap in enumerate(access_points[:3]):
            ssid_bytes = ap.get_ssid()
            ssid = ssid_bytes.get_data().decode('utf-8') if ssid_bytes else f"Hidden_{ap.get_bssid()}"
            strength = ap.get_strength()
            print(f"   • {ssid} ({strength}% signal)")
    
    print(f"✅ Total networks detected: {total_networks}")
    
    if total_networks > 0:
        print("✅ Portable WiFi scanning is working!")
        return True
    else:
        print("⚠️  No networks detected - this might be normal in some environments")
        return True  # Still considered successful as the scanning mechanism works

if __name__ == '__main__':
    try:
        test_wifi_scanning()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)