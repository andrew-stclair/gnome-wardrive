"""
GNOME Wardrive Application Class
Main application controller handling initialization and lifecycle
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib
try:
    from .window import WardriveWindow
except ImportError:
    from window import WardriveWindow

class WardriveApplication(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        super().__init__(
            application_id='com.andrewstclair.Wardrive',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        
        # Connect application signals
        self.connect('activate', self.on_activate)
        self.connect('startup', self.on_startup)
        
        # Application state
        self.main_window = None
        
    def on_startup(self, app):
        """Initialize application on startup"""
        # Set up application-wide actions
        self.setup_actions()
        
        # Load CSS styling
        self.load_css()
        
    def on_activate(self, app):
        """Activate the application - create and present main window"""
        if not self.main_window:
            self.main_window = WardriveWindow(application=self)
        
        self.main_window.present()
        
    def setup_actions(self):
        """Set up application-wide actions"""
        # Quit action
        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action('app.quit', ['<Ctrl>q'])
        
        # About action
        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.on_about_action)
        self.add_action(about_action)
        
        # Preferences action
        preferences_action = Gio.SimpleAction.new('preferences', None)
        preferences_action.connect('activate', self.on_preferences_action)
        self.add_action(preferences_action)
        
    def on_quit_action(self, action, param):
        """Handle quit action"""
        self.quit()
        
    def on_about_action(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow(
            transient_for=self.main_window,
            application_name='GNOME Wardrive',
            application_icon='com.andrewstclair.Wardrive',
            version='1.0.0',
            developer_name='Your Name',
            license_type=Gtk.License.GPL_3_0,
            copyright='© 2025 Your Name',
            comments='WiFi wardriving application for GNOME',
            website='https://github.com/yourusername/gnome-wardrive',
            issue_url='https://github.com/yourusername/gnome-wardrive/issues',
        )
        about_dialog.present()
        
    def on_preferences_action(self, action, param):
        """Show preferences window"""
        # TODO: Implement preferences window
        pass
        
    def load_css(self):
        """Load custom CSS styling"""
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_resource('/com/andrewstclair/Wardrive/style.css')
            # Get the default display for CSS loading
            from gi.repository import Gdk
            display = Gdk.Display.get_default()
            
            if display:
                Gtk.StyleContext.add_provider_for_display(
                    display,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
        except Exception as e:
            print(f"Could not load CSS: {e}")