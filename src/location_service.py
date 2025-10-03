"""
Location Service
Handles GPS location tracking using GeoClue D-Bus interface
"""

import gi
gi.require_version('Geoclue', '2.0')

from gi.repository import GObject, Geoclue, Gio, GLib

class LocationService(GObject.GObject):
    """Location service using GeoClue"""
    
    __gsignals__ = {
        'location-updated': (GObject.SIGNAL_RUN_FIRST, None, (float, float, float)),
        'location-error': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }
    
    def __init__(self):
        super().__init__()
        
        # GeoClue objects
        self.manager = None
        self.client = None
        self.location = None
        
        # Location state
        self.is_active = False
        self.current_latitude = 0.0
        self.current_longitude = 0.0
        self.current_accuracy = 0.0
        
    def start(self):
        """Start location services"""
        if self.is_active:
            return
            
        try:
            print("🌍 Starting location services...")
            # Use the simpler direct D-Bus approach
            self.setup_dbus_connection()
        except Exception as e:
            print(f"❌ Failed to connect to GeoClue: {e}")
            self.emit('location-error', f'Failed to connect to GeoClue: {e}')
    
    def setup_dbus_connection(self):
        """Set up D-Bus connection to GeoClue"""
        try:
            # Connect to system bus
            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            
            # Create GeoClue Manager proxy
            self.manager_proxy = Gio.DBusProxy.new_sync(
                bus,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.GeoClue2',
                '/org/freedesktop/GeoClue2/Manager',
                'org.freedesktop.GeoClue2.Manager',
                None
            )
            
            print("✅ Connected to GeoClue Manager")
            
            # Get client
            result = self.manager_proxy.call_sync(
                'GetClient',
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            
            client_path = result.get_child_value(0).get_string()
            print(f"✅ Got client path: {client_path}")
            
            # Create client proxy
            self.client_proxy = Gio.DBusProxy.new_sync(
                bus,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.GeoClue2',
                client_path,
                'org.freedesktop.GeoClue2.Client',
                None
            )
            
            # Set properties using D-Bus property interface
            props_proxy = Gio.DBusProxy.new_sync(
                bus,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.GeoClue2',
                client_path,
                'org.freedesktop.DBus.Properties',
                None
            )
            
            # Set DesktopId
            props_proxy.call_sync(
                'Set',
                GLib.Variant('(ssv)', [
                    'org.freedesktop.GeoClue2.Client',
                    'DesktopId',
                    GLib.Variant('s', 'com.andrewstclair.Wardrive')
                ]),
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            
            # Set RequestedAccuracyLevel
            props_proxy.call_sync(
                'Set',
                GLib.Variant('(ssv)', [
                    'org.freedesktop.GeoClue2.Client',
                    'RequestedAccuracyLevel',
                    GLib.Variant('u', 8)  # EXACT
                ]),
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            
            print("✅ Set client properties via D-Bus")
            
            # Connect to LocationUpdated signal
            self.client_proxy.connect('g-signal', self.on_location_signal)
            
            # Start the client
            self.client_proxy.call_sync(
                'Start',
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            
            self.is_active = True
            print("✅ Location service started successfully")
            
        except Exception as e:
            print(f"❌ D-Bus setup failed: {e}")
            import traceback
            traceback.print_exc()
    
    def on_location_signal(self, proxy, sender_name, signal_name, parameters):
        """Handle location update signals"""
        if signal_name == 'LocationUpdated':
            old_path = parameters.get_child_value(0).get_string()
            new_path = parameters.get_child_value(1).get_string()
            print(f"📍 Location updated signal: {old_path} -> {new_path}")
            
            if new_path and new_path != '/':
                self.get_location_from_path(new_path)
    
    def get_location_from_path(self, location_path):
        """Get location data from D-Bus path"""
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            
            location_proxy = Gio.DBusProxy.new_sync(
                bus,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.GeoClue2',
                location_path,
                'org.freedesktop.GeoClue2.Location',
                None
            )
            
            # Get location properties
            latitude = location_proxy.get_cached_property('Latitude').get_double()
            longitude = location_proxy.get_cached_property('Longitude').get_double()
            accuracy = location_proxy.get_cached_property('Accuracy').get_double()
            
            # Update current location
            self.current_latitude = latitude
            self.current_longitude = longitude
            self.current_accuracy = accuracy
            
            # Emit location update (latitude, longitude, accuracy only)
            self.emit('location-updated', latitude, longitude, accuracy)
            
            print(f"✅ Location updated: coordinates available (±{accuracy:.1f}m accuracy)")
            
        except Exception as e:
            print(f"❌ Error getting location from path: {e}")
            
    def stop(self):
        """Stop location services"""
        if not self.is_active:
            return
            
        try:
            if self.client:
                self.client.call_stop(None, None, None)
                self.client = None
                
            self.is_active = False
            
        except Exception as e:
            print(f"Error stopping location service: {e}")
            

            
    def get_current_location(self):
        """Get current location data"""
        return {
            'latitude': self.current_latitude,
            'longitude': self.current_longitude,
            'accuracy': self.current_accuracy,
            'active': self.is_active
        }