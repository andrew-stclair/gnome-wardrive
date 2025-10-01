# GNOME Wardrive

A modern GNOME application for WiFi wardriving built with Python, GTK4, and Libadwaita.

## Features

- **Native GNOME integration** with Libadwaita
- **Portable WiFi monitoring** using NetworkManager (works in Flatpak sandboxes)
- **GPS location tracking** via GeoClue
- **Multiple export formats** (CSV, KML, GPX)
- **Modern GTK4 interface** designed for mobile and desktop
- **Flatpak packaging** for easy cross-platform distribution

## WiFi Scanning

This application uses a **passive WiFi monitoring** approach that works reliably across different systems and inside Flatpak sandboxes:

- **Passive Monitoring**: Detects networks that are actively beaconing or being scanned by other devices
- **No System Configuration**: Works out-of-the-box without requiring special permissions or system modifications  
- **Flatpak Compatible**: Full functionality when installed as a sandboxed Flatpak application
- **Cross-Platform**: Same behavior across different Linux distributions and device types

The app continuously monitors NetworkManager's cache of visible access points, which is updated whenever:
- Networks broadcast beacon frames (most APs do this every 100ms)
- Other applications or the system perform WiFi scans
- Users manually refresh WiFi in system settings

## Requirements

- Python 3.8+
- GTK4 (4.14+)
- Libadwaita (1.5+)
- NetworkManager
- GeoClue2
- PyGObject
- GNOME Platform 48 (for Flatpak builds)

## Building

## Building

### Quick Start (Development Testing)

```bash
# 1. Install dependencies
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-nm-1.0 gir1.2-geoclue-2.0 python3-gpxpy

# 2. Test and run the application
./quick-test.sh
```

### Full Build with Meson

```bash
# Install build dependencies
sudo apt install meson ninja-build libadwaita-1-dev python-gi-dev

# Build
meson setup builddir
meson compile -C builddir

# Run
./builddir/src/gnome-wardrive
```

### Flatpak Build

```bash
flatpak-builder build-dir com.andrewstclair.Wardrive.yml --force-clean
flatpak-builder --run build-dir com.andrewstclair.Wardrive.yml gnome-wardrive
```

## Installation

Install from Flathub (coming soon) or build from source.

## License

GPL-3.0+

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.