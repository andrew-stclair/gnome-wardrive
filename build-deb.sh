#!/bin/bash

# Build script for GNOME Wardrive Debian package

set -e

echo "🔨 Building GNOME Wardrive Debian package..."

# Check if we're in the right directory
if [ ! -f "meson.build" ] || [ ! -d "debian" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Install build dependencies if needed
echo "📦 Checking build dependencies..."
sudo apt-get update
sudo apt-get install -y \
    debhelper \
    dh-python \
    python3-all \
    meson \
    ninja-build \
    pkg-config \
    libgtk-4-dev \
    libadwaita-1-dev \
    python-gi-dev \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    gir1.2-nm-1.0 \
    gir1.2-geoclue-2.0 \
    libnm-dev \
    libgio-2.0-dev-bin \
    desktop-file-utils \
    appstream-util \
    build-essential \
    devscripts \
    lintian

# Clean previous builds
echo "🧹 Cleaning previous builds..."
if [ -d "debian/gnome-wardrive" ]; then
    rm -rf debian/gnome-wardrive
fi
if [ -d "builddir" ]; then
    rm -rf builddir
fi

# Build the package
echo "🚀 Building package..."
debuild -us -uc -b

echo ""
echo "✅ Package build completed!"
echo "📦 Package files should be in the parent directory:"
ls -la ../gnome-wardrive*.deb || echo "No .deb files found"

echo ""
echo "🔍 To install the package, run:"
echo "   sudo dpkg -i ../gnome-wardrive_*.deb"
echo "   sudo apt-get install -f  # to fix any dependency issues"