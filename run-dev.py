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

# Load GResource from multiple possible locations
import gi
from gi.repository import Gio

possible_resource_paths = [
    os.path.join(os.path.dirname(__file__), 'builddir', 'data', 'gnome-wardrive.gresource'),
    os.path.join(os.path.dirname(__file__), 'data', 'gnome-wardrive.gresource'),
]

resource_loaded = False
for resource_path in possible_resource_paths:
    if os.path.exists(resource_path):
        try:
            resource = Gio.Resource.load(resource_path)
            resource._register()
            print(f"✓ GResource loaded from {resource_path}")
            resource_loaded = True
            break
        except Exception as e:
            print(f"✗ Failed to load resource from {resource_path}: {e}")

if not resource_loaded:
    print(f"Warning: GResource file not found. Tried:")
    for path in possible_resource_paths:
        print(f"  - {path}")
    print("Make sure to build the project first with: meson setup builddir && meson compile -C builddir")

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