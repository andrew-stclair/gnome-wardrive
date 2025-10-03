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

# Build the project if needed
if [ ! -d "builddir" ]; then
    echo "📦 Setting up build directory..."
    meson setup builddir
fi

echo "🔨 Building project..."
meson compile -C builddir

# Run the application
echo "🎯 Launching application..."
/usr/bin/python3 run-dev.py