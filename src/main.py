#!/usr/bin/env python3

"""
GNOME Wardrive - WiFi Wardriving Application
Main entry point for the application
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('NM', '1.0')
gi.require_version('Geoclue', '2.0')

from gi.repository import Gtk, Adw, Gio, GLib
from .application import WardriveApplication

def main():
    """Main function to run the application"""
    app = WardriveApplication()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main())