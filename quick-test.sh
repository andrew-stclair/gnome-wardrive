#!/bin/bash
# Quick test script for GNOME Wardrive

echo "🚀 Starting GNOME Wardrive..."

# Test WiFi scanning capability
echo "📡 Testing WiFi scanning..."
if python3 test-wifi-scanning.py > /dev/null 2>&1; then
    echo "✅ Portable WiFi scanning ready"
else
    echo "⚠️  WiFi scanning test failed - check NetworkManager status"
fi
echo ""

# Compile resources if needed
if [ ! -f "data/gnome-wardrive.gresource" ] || [ "data/gnome-wardrive.gresource.xml" -nt "data/gnome-wardrive.gresource" ]; then
    echo "📦 Compiling UI resources..."
    glib-compile-resources --target=data/gnome-wardrive.gresource --sourcedir=data data/gnome-wardrive.gresource.xml
fi

# Run the application
echo "🎯 Launching application..."
/usr/bin/python3 run-dev.py