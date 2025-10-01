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
    PACKAGES="python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-nm-1.0 gir1.2-geoclue-2.0 meson ninja-build appstream-util desktop-file-utils libglib2.0-bin flatpak flatpak-builder"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
    INSTALL_CMD="sudo dnf install -y"
    PACKAGES="python3-gobject gtk4-devel libadwaita-devel NetworkManager-glib-devel geoclue2-devel meson ninja-build appstream desktop-file-utils glib2-devel flatpak flatpak-builder"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S --needed"
    PACKAGES="python-gobject gtk4 libadwaita networkmanager geoclue meson ninja appstream-glib desktop-file-utils glib2 flatpak flatpak-builder"
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

# Set up Flatpak development environment
echo "Setting up Flatpak development environment..."
if ! flatpak remote-list | grep -q flathub; then
    echo "Adding Flathub repository..."
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
fi

echo "Installing GNOME Platform runtime..."
flatpak install -y flathub org.gnome.Platform//46 org.gnome.Sdk//46

# Test the setup
echo "Testing setup..."
python3 test_setup.py

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To build and run the application:"
echo "  meson setup builddir"
echo "  meson compile -C builddir"
echo "  ./builddir/src/gnome-wardrive"
echo ""
echo "To build Flatpak:"
echo "  flatpak-builder build-dir com.andrewstclair.Wardrive.yml --force-clean"
echo "  flatpak-builder --run build-dir com.andrewstclair.Wardrive.yml gnome-wardrive"
echo ""
echo "Happy hacking! 🚀"