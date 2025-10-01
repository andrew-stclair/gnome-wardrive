#!/bin/bash

# Setup script to enable WiFi scanning for GNOME Wardrive
# This creates a PolicyKit rule to allow users in netdev group to scan WiFi

set -e

echo "Setting up WiFi scanning permissions for GNOME Wardrive..."

# Check if user is in netdev group
if ! groups | grep -q netdev; then
    echo "Adding user to netdev group..."
    sudo usermod -a -G netdev $USER
    echo "⚠️  You need to logout and login again for group changes to take effect!"
fi

# Create PolicyKit rule for WiFi scanning
POLICY_FILE="/etc/polkit-1/rules.d/10-gnome-wardrive-wifi-scan.rules"

echo "Creating PolicyKit rule at $POLICY_FILE..."

sudo tee "$POLICY_FILE" > /dev/null << 'EOF'
/* Allow users in netdev group to scan WiFi networks without authentication */
polkit.addRule(function(action, subject) {
    if ((action.id == "org.freedesktop.NetworkManager.wifi.scan") &&
        subject.isInGroup("netdev")) {
        return polkit.Result.YES;
    }
});
EOF

echo "✅ PolicyKit rule created successfully!"
echo "✅ Restarting PolicyKit to apply changes..."

# Restart PolicyKit
sudo systemctl restart polkit

echo ""
echo "🎉 Setup complete! WiFi scanning should now work without authentication."
echo ""
echo "If you added the user to netdev group, please:"
echo "1. Logout and login again"
echo "2. Run the application again"
echo ""
echo "To test WiFi scanning manually:"
echo "  nmcli device wifi rescan"
echo ""