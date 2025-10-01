#!/usr/bin/env python3

"""
Simple test to run GNOME Wardrive directly from source
This bypasses the build system and runs the app directly for testing
"""

import sys
import os
import signal

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up signal handling for Ctrl+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Set up environment for GResource
os.environ['GSETTINGS_SCHEMA_DIR'] = os.path.join(os.path.dirname(__file__), 'data')

# Load GResource
resource_path = os.path.join(os.path.dirname(__file__), 'builddir', 'data', 'gnome-wardrive.gresource')
if os.path.exists(resource_path):
    import gi
    from gi.repository import Gio
    resource = Gio.Resource.load(resource_path)
    resource._register()
else:
    print(f"Warning: GResource file not found at {resource_path}")
    print("Make sure to build the project first with: meson setup builddir && ninja -C builddir")

if __name__ == '__main__':
    try:
        # Test imports first
        print("Testing imports...")
        import gi
        gi.require_version('Gtk', '4.0')
        gi.require_version('Adw', '1')
        gi.require_version('NM', '1.0')
        gi.require_version('Geoclue', '2.0')
        
        from gi.repository import Gtk, Adw, Gio, GLib, NM, Geoclue
        print("✓ All GTK/GNOME modules imported successfully")
        
        # Import our application
        import application
        print("✓ Application module imported successfully")
        
        # Run the application
        print("Starting GNOME Wardrive...")
        app = application.WardriveApplication()
        sys.exit(app.run(sys.argv))
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all required packages are installed:")
        print("  sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-nm-1.0 gir1.2-geoclue-2.0")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)