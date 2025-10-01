"""
WiFi Scanner Service
Handles WiFi network scanning using NetworkManager D-Bus interface
"""

import gi
gi.require_version('NM', '1.0')

from gi.repository import GObject, NM, GLib
import time

class WiFiScanner(GObject.GObject):
    """WiFi scanner using NetworkManager"""
    
    __gsignals__ = {
        'network-found': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'scan-completed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'scan-error': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }
    
    def __init__(self):
        super().__init__()
        
        # NetworkManager client
        self.nm_client = NM.Client.new(None)
        self.is_scanning = False
        self.scan_timeout_id = None
        self.scan_attempts = 0
        
        # Get WiFi devices
        self.wifi_devices = []
        self.refresh_wifi_devices()
        
    def refresh_wifi_devices(self):
        """Get all available WiFi devices"""
        self.wifi_devices = []
        for device in self.nm_client.get_devices():
            if device.get_device_type() == NM.DeviceType.WIFI:
                self.wifi_devices.append(device)
                
        print(f"Found {len(self.wifi_devices)} WiFi devices")
        
    def start_scan(self):
        """Start WiFi scanning"""
        if self.is_scanning:
            return
            
        if not self.wifi_devices:
            self.emit('scan-error', 'No WiFi devices found')
            return
            
        self.is_scanning = True
        self.scan_attempts = 0
        
        # Try to request active scan, but continue with passive scanning if denied
        self._attempt_active_scan()
                
        # Set up periodic scan updates (works with both active and passive scanning)
        self.scan_timeout_id = GLib.timeout_add_seconds(1, self.update_scan_results)
        
    def _attempt_active_scan(self):
        """Attempt active WiFi scanning, fall back to passive if not authorized"""
        active_scan_successful = False
        
        for device in self.wifi_devices:
            try:
                # Try to request an active scan
                wifi_device = device
                wifi_device.request_scan_async(None, self.on_scan_requested, device)
                active_scan_successful = True
            except Exception as e:
                # If scan request fails, we'll continue with passive scanning
                error_msg = str(e).lower()
                if "not authorized" in error_msg or "authentication" in error_msg:
                    print(f"ℹ️  Active scanning not available on {device.get_iface()}, using passive monitoring")
                else:
                    print(f"⚠️  Scan request failed on {device.get_iface()}: {e}")
        
        if not active_scan_successful:
            print("ℹ️  Running in passive WiFi monitoring mode")
            print("ℹ️  The app will detect networks as they beacon or when other devices scan")
        
    def stop_scan(self):
        """Stop WiFi scanning"""
        self.is_scanning = False
        
        if self.scan_timeout_id:
            GLib.source_remove(self.scan_timeout_id)
            self.scan_timeout_id = None
            
        self.emit('scan-completed')
        
    def on_scan_requested(self, device, result, user_data):
        """Handle scan request completion"""
        try:
            device.request_scan_finish(result)
            print(f"✅ Active scan initiated on {device.get_iface()}")
        except Exception as e:
            # This is expected in sandboxed environments - just continue with passive scanning
            pass
            
    def update_scan_results(self):
        """Update scan results from all devices"""
        if not self.is_scanning:
            return False
            
        current_time = time.time()
        networks_found_this_cycle = 0
        
        for device in self.wifi_devices:
            try:
                access_points = device.get_access_points()
                
                for ap in access_points:
                    network_data = self.extract_network_data(ap, device, current_time)
                    if network_data:
                        self.emit('network-found', network_data)
                        networks_found_this_cycle += 1
                        
            except Exception as e:
                print(f"Error getting access points from {device.get_iface()}: {e}")
        
        # Provide periodic feedback about scanning
        self.scan_attempts += 1
        if self.scan_attempts % 10 == 0:  # Every 10 seconds
            total_networks = sum(len(device.get_access_points()) for device in self.wifi_devices)
            print(f"📡 Monitoring: {total_networks} networks visible across {len(self.wifi_devices)} device(s)")
                
        return True  # Continue timeout
    
    def get_current_networks(self):
        """Get all currently visible networks from all devices"""
        networks = []
        current_time = time.time()
        
        for device in self.wifi_devices:
            try:
                access_points = device.get_access_points()
                for ap in access_points:
                    network_data = self.extract_network_data(ap, device, current_time)
                    if network_data:
                        networks.append(network_data)
            except Exception as e:
                print(f"Error getting networks from {device.get_iface()}: {e}")
                
        return networks
        
    def extract_network_data(self, access_point, device, timestamp):
        """Extract network data from access point"""
        try:
            ssid_bytes = access_point.get_ssid()
            ssid = ssid_bytes.get_data().decode('utf-8') if ssid_bytes else None
            
            # Skip if no SSID (hidden networks handled separately)
            if not ssid:
                ssid = f"Hidden_{access_point.get_bssid()}"
                
            network_data = {
                'ssid': ssid,
                'bssid': access_point.get_bssid(),
                'signal_strength': access_point.get_strength(),
                'frequency': access_point.get_frequency(),
                'channel': self.frequency_to_channel(access_point.get_frequency()),
                'security': self.get_security_type(access_point),
                'device_interface': device.get_iface(),
                'timestamp': timestamp,
                'last_seen': timestamp,
            }
            
            return network_data
            
        except Exception as e:
            print(f"Error extracting network data: {e}")
            return None
            
    def get_security_type(self, access_point):
        """Determine security type of access point"""
        try:
            flags = access_point.get_flags()
            wpa_flags = access_point.get_wpa_flags()
            rsn_flags = access_point.get_rsn_flags()
            
            # Use the correct NM flag names
            ApFlags = getattr(NM, '80211ApFlags')
            SecurityFlags = getattr(NM, '80211ApSecurityFlags')
            
            # Check for WPA3 (RSN with SAE)
            if hasattr(SecurityFlags, 'KEY_MGMT_SAE') and rsn_flags & SecurityFlags.KEY_MGMT_SAE:
                return 'WPA3'
            # Check for WPA2 (RSN with PSK or 802.1X)
            elif rsn_flags & (SecurityFlags.KEY_MGMT_PSK | SecurityFlags.KEY_MGMT_802_1X):
                return 'WPA2'
            # Check for WPA (WPA flags present)
            elif wpa_flags & (SecurityFlags.KEY_MGMT_PSK | SecurityFlags.KEY_MGMT_802_1X):
                return 'WPA'
            # Check for WEP (privacy flag without WPA/WPA2)
            elif flags & ApFlags.PRIVACY:
                return 'WEP'
            else:
                return 'Open'
        except Exception as e:
            print(f"Error determining security type: {e}")
            # Fallback: simple detection based on presence of security
            try:
                wpa_flags = access_point.get_wpa_flags()
                rsn_flags = access_point.get_rsn_flags()
                
                if rsn_flags or wpa_flags:
                    return 'WPA/WPA2'
                elif access_point.get_flags():
                    return 'WEP'  
                else:
                    return 'Open'
            except:
                return 'Unknown'
            
    def frequency_to_channel(self, frequency):
        """Convert frequency to WiFi channel number"""
        if frequency >= 2412 and frequency <= 2484:
            # 2.4 GHz band
            if frequency == 2484:
                return 14
            else:
                return int((frequency - 2412) / 5) + 1
        elif frequency >= 5170 and frequency <= 5825:
            # 5 GHz band
            return int((frequency - 5000) / 5)
        elif frequency >= 5925 and frequency <= 7125:
            # 6 GHz band (WiFi 6E)
            return int((frequency - 5950) / 5) + 1
        else:
            return 0  # Unknown
            
    def get_network_count(self):
        """Get total number of unique networks found"""
        # This would typically be managed by DataManager
        return 0