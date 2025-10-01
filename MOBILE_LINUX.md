# Mobile Linux Installation Guide

## 🏗️ Native Multi-Architecture Builds

GNOME Wardrive uses **native runners** for all architectures to ensure optimal performance and consistency:

### Build Infrastructure
- **x86_64 (Desktop)**: Native x86_64 runner (`ubuntu-latest`) with direct Flatpak installation
- **aarch64 (Mobile)**: Native ARM64 runner (`ubuntu-24.04-arm`) with direct Flatpak installation
- **No Cross-compilation**: Each build runs on native hardware for its target architecture
- **No Containers**: Direct Ubuntu environment eliminates container complexity and compatibility issues

### Why Native Approach?
- **Consistency**: Same build process and environment for all architectures
- **Reliability**: No dependency on third-party container image availability
- **Performance**: Native compilation provides optimal performance for each platform
- **Simplicity**: Easier to debug, maintain, and understand
- **Mobile-First**: Perfectly optimized for PinePhone, Librem 5, and other ARM64 mobile devices

## 📱 Supported Mobile Devices

GNOME Wardrive is optimized for Linux mobile devices with native ARM64 support:

### Primary Target Devices
- **PinePhone / PinePhone Pro** (Manjaro ARM, postmarketOS, Mobian)
- **Librem 5** (PureOS) 
- **OnePlus 6/6T** (postmarketOS)
- **Fairphone 4** (Ubuntu Touch, postmarketOS)
- **Raspberry Pi 4+** (Any ARM64 Linux distribution)

### Mobile Linux Distributions
- **postmarketOS**: Alpine-based mobile Linux
- **Mobian**: Debian-based mobile Linux  
- **Manjaro ARM**: Arch-based mobile Linux
- **PureOS**: Debian-based (Librem 5 default)
- **Ubuntu Touch**: Convergent mobile OS
- **Fedora Mobile**: Red Hat mobile variant

## 🚀 Installation on Mobile Devices

### Method 1: Direct Installation (Recommended)

1. **Download the ARM64 bundle** to your mobile device:
   ```bash
   # On your mobile device
   wget https://github.com/andrew-stclair/gnome-wardrive/releases/latest/download/com.andrewstclair.Wardrive-aarch64.flatpak
   ```

2. **Install Flatpak** (if not already installed):
   ```bash
   # Debian/Ubuntu based (Mobian, PureOS)
   sudo apt install flatpak
   
   # Alpine based (postmarketOS)
   sudo apk add flatpak
   
   # Arch based (Manjaro ARM)
   sudo pacman -S flatpak
   
   # Add Flathub repository
   flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
   ```

3. **Install GNOME Wardrive**:
   ```bash
   flatpak install com.andrewstclair.Wardrive-aarch64.flatpak
   ```

4. **Launch the application**:
   ```bash
   flatpak run com.andrewstclair.Wardrive
   ```

### Method 2: Transfer from Desktop

1. **Download on desktop** and transfer via SSH/USB:
   ```bash
   # On desktop
   wget https://github.com/andrew-stclair/gnome-wardrive/releases/latest/download/com.andrewstclair.Wardrive-aarch64.flatpak
   
   # Transfer to mobile device (replace with your device IP)
   scp com.andrewstclair.Wardrive-aarch64.flatpak user@mobile-device-ip:~/
   ```

2. **Install on mobile device**:
   ```bash
   # On mobile device
   flatpak install ~/com.andrewstclair.Wardrive-aarch64.flatpak
   ```

## 🔧 Mobile-Specific Configuration

### Touch Interface Optimization
The application is designed with mobile-first principles:
- **48px minimum touch targets** for finger navigation
- **Adaptive layout** that works from 320px to desktop sizes
- **Bottom action bar** for thumb-friendly access
- **Swipe-friendly list views** for network browsing

### Battery Optimization
For extended mobile wardriving sessions:

1. **Enable battery saver mode** in your mobile OS
2. **Reduce screen brightness** when not actively viewing
3. **Use airplane mode + WiFi** to disable cellular radio
4. **Close unnecessary background apps**

### Permission Requirements
The app uses D-Bus interfaces that work in Flatpak sandboxes:
- **NetworkManager access**: Passive WiFi scanning (no special permissions)
- **GeoClue access**: GPS location services
- **Home directory access**: For exporting scan data

## 📊 Mobile Wardriving Tips

### Optimal Mobile Setup
1. **Portable power bank**: Extended battery life for long sessions
2. **Car mount**: Hands-free operation while mobile
3. **External GPS antenna**: Better location accuracy (if supported)
4. **Offline maps**: For correlating WiFi data with locations

### Data Management
- **Regular exports**: Save scan data frequently (CSV/KML/GPX formats)
- **Cloud sync**: Upload data to prevent loss
- **Storage monitoring**: Keep adequate free space for scan data

### Mobile Performance
- **ARM64 native builds**: No emulation overhead
- **Lightweight UI**: Optimized for mobile CPUs
- **Efficient scanning**: Passive monitoring minimizes battery drain

## 🛠️ Troubleshooting Mobile Issues

### Common Mobile Problems

**GPS not working:**
```bash
# Check if location services are enabled
systemctl --user status geoclue
```

**WiFi scanning not finding networks:**
```bash
# Verify NetworkManager is running
systemctl status NetworkManager

# Check if WiFi device is available
nmcli device status
```

**Touch interface not responsive:**
- Ensure GTK4 touch support is enabled
- Check if compositor supports touch events
- Verify screen calibration

**Performance issues:**
- Close background applications
- Ensure adequate RAM (minimum 1GB recommended)
- Check CPU thermal throttling

### Mobile-Specific Logs
View application logs for mobile debugging:
```bash
# Run with debug output
flatpak run --command=sh com.andrewstclair.Wardrive -c "gnome-wardrive --verbose"

# Check system logs
journalctl --user -u app.flatpak.com.andrewstclair.Wardrive
```

## 🌐 Mobile Linux Community

### Getting Help
- **Matrix**: #mobile-linux:matrix.org
- **Reddit**: r/LinuxPhone, r/postmarketOS
- **IRC**: #postmarketos on OFTC

### Contributing Mobile Improvements
- Test on different mobile devices
- Report mobile-specific bugs
- Suggest UI/UX improvements for small screens
- Contribute translations for mobile interfaces

## 📈 Mobile Wardriving Use Cases

### Research Applications
- **Network security auditing** on mobile networks
- **Dead zone mapping** for cellular/WiFi coverage
- **Urban connectivity analysis** while walking/driving
- **IoT device discovery** in smart city environments

### Field Work
- **Site surveys** for WiFi planning
- **Network troubleshooting** in remote locations  
- **Coverage verification** for deployed networks
- **Compliance testing** for wireless regulations

The mobile-optimized build ensures professional wardriving capabilities in a pocket-sized, battery-efficient package! 📱🔍