"""
Main Window for GNOME Wardrive Application
Handles the primary user interface and coordinates between services
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib
try:
    from .wifi_scanner import WiFiScanner
    from .location_service import LocationService
    from .data_manager import DataManager
except ImportError:
    try:
        from gnome_wardrive.wifi_scanner import WiFiScanner
        from gnome_wardrive.location_service import LocationService
        from gnome_wardrive.data_manager import DataManager
    except ImportError:
        from wifi_scanner import WiFiScanner
        from location_service import LocationService
        from data_manager import DataManager

@Gtk.Template(resource_path='/com/andrewstclair/Wardrive/ui/window_mobile.ui')
class WardriveWindow(Adw.ApplicationWindow):
    """Main application window"""
    
    __gtype_name__ = 'WardriveWindow'
    
    # Template children - these will be populated from the UI file
    header_bar = Gtk.Template.Child()
    networks_listbox = Gtk.Template.Child()
    scan_button = Gtk.Template.Child()
    export_button = Gtk.Template.Child()
    networks_count_label = Gtk.Template.Child()
    empty_networks_row = Gtk.Template.Child()
    devices_count_label = Gtk.Template.Child()
    location_label = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize services
        self.wifi_scanner = WiFiScanner()
        self.location_service = LocationService()
        self.data_manager = DataManager()
        
        # Connect signals
        self.setup_signals()
        
        # Initialize UI state
        self.setup_ui()
        
        # Mobile-specific initialization
        self.setup_mobile_ui()
        
        # Show scanning mode info
        self.show_scanning_info()
        
    def setup_mobile_ui(self):
        """Configure mobile-specific UI elements"""
        # Track network count
        self.network_count = 0
        
        # Initialize mobile status indicators
        self.update_networks_count(0)
        self.update_location_accuracy("No GPS")
        self.update_devices_count()
        
        # Set up responsive behavior
        self.setup_adaptive_behavior()
        
    def setup_adaptive_behavior(self):
        """Set up adaptive UI behavior for different screen sizes"""
        # Connect to size changes for responsive design
        self.connect('notify::default-width', self._on_size_changed)
        self.connect('notify::default-height', self._on_size_changed)
        
    def _on_size_changed(self, *args):
        """Handle window size changes for responsive design"""
        # Get current size
        width = self.get_default_width()
        
        # Adjust UI for very narrow screens (< 400px)
        if width < 400:
            self.scan_button.set_label("Scan")
        else:
            self.scan_button.set_label("Start Scan")
        
    def show_scanning_info(self):
        """Display information about WiFi scanning capabilities"""
        # This will be called after WiFi scanner initialization
        GLib.timeout_add_seconds(1, self._check_scanning_mode)
        
    def _check_scanning_mode(self):
        """Check and display the current WiFi scanning mode"""
        # Refresh WiFi devices and update display
        if hasattr(self, 'wifi_scanner'):
            self.wifi_scanner.refresh_wifi_devices()
            self.update_devices_count()
        return False  # Don't repeat
        
    def update_networks_count(self, count):
        """Update the networks count display"""
        self.network_count = count
        if count == 0:
            self.networks_count_label.set_text("No networks")
            self.empty_networks_row.set_visible(True)
        elif count == 1:
            self.networks_count_label.set_text("1 network")
            self.empty_networks_row.set_visible(False)
        else:
            self.networks_count_label.set_text(f"{count} networks")
            self.empty_networks_row.set_visible(False)
            
    def update_location_accuracy(self, status):
        """Update location accuracy display - now just logs the status"""
        # Location accuracy information no longer displayed in UI
        # This method is kept for compatibility but doesn't update UI elements
        print(f"Location accuracy: {status}")
            
    def update_devices_count(self):
        """Update WiFi devices count display"""
        if hasattr(self, 'wifi_scanner') and self.wifi_scanner.wifi_devices:
            device_count = len(self.wifi_scanner.wifi_devices)
            if device_count == 1:
                self.devices_count_label.set_text("1 device")
            else:
                self.devices_count_label.set_text(f"{device_count} devices")
        else:
            self.devices_count_label.set_text("0 devices")
            
    def set_scanning_active(self, active):
        """Update UI to show scanning state"""
        if active:
            self.scan_button.set_label("Stop Scan")
            self.scan_button.remove_css_class("suggested-action")
            self.scan_button.add_css_class("destructive-action")
        else:
            self.scan_button.set_label("Start Scan")
            self.scan_button.remove_css_class("destructive-action") 
            self.scan_button.add_css_class("suggested-action")
            self.update_devices_count()
        
    def setup_signals(self):
        """Connect widget signals"""
        self.scan_button.connect('clicked', self.on_scan_clicked)
        self.export_button.connect('clicked', self.on_export_clicked)
        
        # Connect service signals
        self.wifi_scanner.connect('network-found', self.on_network_found)
        self.wifi_scanner.connect('scan-completed', self.on_scan_completed)
        self.location_service.connect('location-updated', self.on_location_updated)
        
    def setup_ui(self):
        """Initialize UI state"""
        self.scan_button.set_label('Start Scanning')
        self.export_button.set_sensitive(False)
        self.location_label.set_text('Unknown')
        
        # Start location service
        self.location_service.start()
        
    def on_scan_clicked(self, button):
        """Handle scan button click"""
        if self.wifi_scanner.is_scanning:
            self.wifi_scanner.stop_scan()
            self.set_scanning_active(False)
        else:
            self.wifi_scanner.start_scan()
            self.set_scanning_active(True)
            
    def on_export_clicked(self, button):
        """Handle export button click"""
        self.show_export_dialog()
        
    def on_network_found(self, scanner, network_data):
        """Handle new network found"""
        # Add network to the list
        self.add_network_to_list(network_data)
        
        # Save to data manager
        self.data_manager.add_network(network_data)
        
        # Update mobile UI
        network_count = self.data_manager.get_network_count()
        self.update_networks_count(network_count)
        
        if network_count > 0:
            self.export_button.set_sensitive(True)
            
    def on_scan_completed(self, scanner):
        """Handle scan completion"""
        self.set_scanning_active(False)
        network_count = self.data_manager.get_network_count()
        self.update_networks_count(network_count)
        
    def on_location_updated(self, service, latitude, longitude, accuracy):
        """Handle location update"""
        # Update location display with lat, long, and accuracy
        if accuracy > 0:
            location_text = f"{latitude:.4f}, {longitude:.4f} (±{accuracy:.0f}m)"
        else:
            location_text = f"{latitude:.4f}, {longitude:.4f}"
        
        self.location_label.set_text(location_text)
        
        # Update mobile accuracy display
        if accuracy == 0:
            accuracy_text = "High accuracy"
        elif accuracy <= 10:
            accuracy_text = f"±{accuracy}m"
        else:
            accuracy_text = f"±{accuracy}m (low)"
        self.update_location_accuracy(accuracy_text)
        
        self.data_manager.update_location(latitude, longitude, accuracy)
        
    def add_network_to_list(self, network_data):
        """Add a network to the networks list"""
        row = Adw.ActionRow()
        
        # Set network name
        ssid = network_data.get('ssid', 'Hidden Network')
        row.set_title(ssid)
        
        # Create mobile-friendly subtitle
        bssid = network_data.get('bssid', 'Unknown')
        signal = network_data.get('signal_strength', 0)
        security = network_data.get('security', 'Unknown')
        
        subtitle = f"{bssid[-8:]} • {signal}% • {security}"
        row.set_subtitle(subtitle)
        
        # Set network type icon
        if security == 'Open':
            row.set_icon_name('network-wireless-symbolic')
        else:
            row.set_icon_name('network-wireless-encrypted-symbolic')
            
        # Add signal strength indicator
        signal_icon = Gtk.Image()
        if signal >= 70:
            signal_icon.set_from_icon_name('network-wireless-signal-excellent-symbolic')
        elif signal >= 50:
            signal_icon.set_from_icon_name('network-wireless-signal-good-symbolic')
        elif signal >= 30:
            signal_icon.set_from_icon_name('network-wireless-signal-ok-symbolic')
        else:
            signal_icon.set_from_icon_name('network-wireless-signal-weak-symbolic')
            
        signal_icon.add_css_class('dim-label')
        row.add_suffix(signal_icon)
            
        self.networks_listbox.append(row)
        
    def show_export_dialog(self):
        """Show export format selection dialog"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading='Export Data',
            body='Choose export format:'
        )
        
        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('csv', 'CSV')
        dialog.add_response('kml', 'KML')
        dialog.add_response('gpx', 'GPX')
        
        dialog.set_response_appearance('csv', Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect('response', self.on_export_dialog_response)
        dialog.present()
        
    def on_export_dialog_response(self, dialog, response):
        """Handle export dialog response"""
        if response in ['csv', 'kml', 'gpx']:
            self.export_data(response)
            
    def export_data(self, format_type):
        """Export data in specified format"""
        # Create file chooser dialog
        file_dialog = Gtk.FileDialog()
        file_dialog.set_title('Save Export File')
        
        # Set default filename based on format
        if format_type == 'csv':
            file_dialog.set_initial_name('wardrive_data.csv')
        elif format_type == 'kml':
            file_dialog.set_initial_name('wardrive_data.kml')
        elif format_type == 'gpx':
            file_dialog.set_initial_name('wardrive_data.gpx')
            
        file_dialog.save(self, None, self.on_export_file_selected, format_type)
        
    def on_export_file_selected(self, dialog, result, format_type):
        """Handle export file selection"""
        try:
            file = dialog.save_finish(result)
            if file:
                file_path = file.get_path()
                success = self.data_manager.export_data(file_path, format_type)
                
                if success:
                    toast = Adw.Toast(title=f'Data exported to {file_path}')
                else:
                    toast = Adw.Toast(title='Export failed')
                    
                # Add toast to window (requires a ToastOverlay in the UI)
                # self.toast_overlay.add_toast(toast)
        except Exception as e:
            print(f"Export error: {e}")
            toast = Adw.Toast(title='Export failed')
            # self.toast_overlay.add_toast(toast)