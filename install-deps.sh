#!/bin/bash

# Install runtime dependencies for GNOME Wardrive

set -e

echo "📦 Installing GNOME Wardrive runtime dependencies..."

# Update package list
sudo apt-get update

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
sudo apt-get install -y \
    python3 \
    python3-gi \
    python3-requests \
    python3-gpxpy \
    python3-cairo \
    python3-pkg-resources

# Install GTK/GNOME dependencies
echo "🎨 Installing GTK/GNOME dependencies..."
sudo apt-get install -y \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    gir1.2-nm-1.0 \
    gir1.2-geoclue-2.0 \
    libgtk-4-1 \
    libadwaita-1-0

# Install NetworkManager and GPS
echo "📡 Installing NetworkManager and GPS dependencies..."
sudo apt-get install -y \
    network-manager \
    gpsd \
    gpsd-clients

echo ""
echo "✅ All runtime dependencies installed!"
echo ""
echo "📝 Note: You may need to ensure NetworkManager is running:"
echo "   sudo systemctl enable --now NetworkManager"
echo ""
echo "🌐 For GPS functionality, you may need to configure gpsd:"
echo "   sudo systemctl enable --now gpsd"