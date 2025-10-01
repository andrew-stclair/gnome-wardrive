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
    from wifi_scanner import WiFiScanner
    from location_service import LocationService
    from data_manager import DataManager

@Gtk.Template(resource_path='/com/andrewstclair/Wardrive/ui/window_simple.ui')
class WardriveWindow(Adw.ApplicationWindow):
    """Main application window"""
    
    __gtype_name__ = 'WardriveWindow'
    
    # Template children - these will be populated from the UI file
    header_bar = Gtk.Template.Child()
    networks_listbox = Gtk.Template.Child()
    status_label = Gtk.Template.Child()
    location_label = Gtk.Template.Child()
    scan_button = Gtk.Template.Child()
    export_button = Gtk.Template.Child()
    
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
        
        # Show scanning mode info
        self.show_scanning_info()
        
    def show_scanning_info(self):
        """Display information about WiFi scanning capabilities"""
        # This will be called after WiFi scanner initialization
        GLib.timeout_add_seconds(1, self._check_scanning_mode)
        
    def _check_scanning_mode(self):
        """Check and display the current WiFi scanning mode"""
        if hasattr(self, 'wifi_scanner') and self.wifi_scanner.wifi_devices:
            device_count = len(self.wifi_scanner.wifi_devices)
            self.status_label.set_text(
                f"📡 WiFi Monitor Ready • {device_count} device(s) • "
                f"Passive scanning mode (Flatpak compatible)"
            )
        return False  # Don't repeat
        
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
        self.status_label.set_text('Ready to scan')
        self.location_label.set_text('Location: Unknown')
        
        # Start location service
        self.location_service.start()
        
    def on_scan_clicked(self, button):
        """Handle scan button click"""
        if self.wifi_scanner.is_scanning:
            self.wifi_scanner.stop_scan()
            button.set_label('Start Scanning')
            self.status_label.set_text('Scan stopped')
        else:
            self.wifi_scanner.start_scan()
            button.set_label('Stop Scanning')
            self.status_label.set_text('Scanning...')
            
    def on_export_clicked(self, button):
        """Handle export button click"""
        self.show_export_dialog()
        
    def on_network_found(self, scanner, network_data):
        """Handle new network found"""
        # Add network to the list
        self.add_network_to_list(network_data)
        
        # Save to data manager
        self.data_manager.add_network(network_data)
        
        # Update UI
        network_count = self.data_manager.get_network_count()
        self.status_label.set_text(f'Found {network_count} networks')
        
        if network_count > 0:
            self.export_button.set_sensitive(True)
            
    def on_scan_completed(self, scanner):
        """Handle scan completion"""
        self.scan_button.set_label('Start Scanning')
        network_count = self.data_manager.get_network_count()
        self.status_label.set_text(f'Scan complete - {network_count} networks found')
        
    def on_location_updated(self, service, latitude, longitude, accuracy):
        """Handle location update"""
        self.location_label.set_text(f'Location: {latitude:.6f}, {longitude:.6f} (±{accuracy}m)')
        self.data_manager.update_location(latitude, longitude, accuracy)
        
    def add_network_to_list(self, network_data):
        """Add a network to the networks list"""
        row = Adw.ActionRow()
        row.set_title(network_data.get('ssid', 'Hidden Network'))
        
        subtitle = f"BSSID: {network_data.get('bssid', 'Unknown')}"
        if 'signal_strength' in network_data:
            subtitle += f" | Signal: {network_data['signal_strength']} dBm"
        if 'security' in network_data:
            subtitle += f" | Security: {network_data['security']}"
            
        row.set_subtitle(subtitle)
        
        # Add security icon
        if network_data.get('security') != 'Open':
            icon = Gtk.Image.new_from_icon_name('security-high-symbolic')
            row.add_suffix(icon)
            
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