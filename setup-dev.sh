#!/bin/bash

# Development setup script for GNOME Wardrive
# This script sets up the development environment

set -e

echo "Setting up GNOME Wardrive development environment..."
echo "=================================================="

# Check if we're running on a supported system
if command -v apt >/dev/null 2>&1; then
    PKG_MANAGER="apt"
    INSTALL_CMD="sudo apt install -y"
    PACKAGES="python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-nm-1.0 gir1.2-geoclue-2.0 meson ninja-build appstream-util desktop-file-utils libglib2.0-bin build-essential debhelper dh-python"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
    PACKAGES="python3-gobject gtk4-devel libadwaita-devel NetworkManager-glib-devel geoclue2-devel meson ninja-build appstream desktop-file-utils glib2-devel rpm-build"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S --needed"
    PACKAGES="python-gobject gtk4 libadwaita networkmanager geoclue meson ninja appstream-glib desktop-file-utils glib2 base-devel"
else
    echo "Unsupported package manager. Please install dependencies manually."
    echo "Required packages: GTK4, Libadwaita, NetworkManager, GeoClue, Meson, Python GObject"
    exit 1
fi

echo "Detected package manager: $PKG_MANAGER"
echo "Installing system dependencies..."
$INSTALL_CMD $PACKAGES

echo "Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

# Set up build environment
echo "Setting up build environment..."
meson setup builddir --buildtype=debug
echo "Build environment configured."

# Test the setup
echo "Testing setup..."
python3 test_setup.py

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To build and run the application:"
echo "  meson compile -C builddir"
echo "  ./builddir/src/gnome-wardrive"
echo ""
echo "To build Debian package:"
echo "  ./build-deb.sh"
echo ""
echo "Happy hacking! 🚀"