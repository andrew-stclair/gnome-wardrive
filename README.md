# GNOME Wardrive

A modern GNOME application for WiFi wardriving built with Python, GTK4, and Libadwaita.  
**Optimized for Linux mobile devices** like PinePhone, Librem 5, and postmarketOS.

## Features

- **📱 Mobile Linux First** - Native ARM64 builds for PinePhone, Librem 5, postmarketOS devices
- **🔄 Adaptive Interface** - Touch-optimized UI that works from 320px phone screens to desktop
- **📡 Portable WiFi Scanning** - Uses NetworkManager D-Bus (works in Flatpak sandboxes, no root needed)
- **🌍 GPS Location Tracking** - Native GeoClue integration for accurate positioning
- **💾 Multiple Export Formats** - CSV, KML, GPX for analysis and mapping
- **👆 Touch-Friendly Design** - 48px minimum touch targets, bottom action bars
- **🎨 Native GNOME Integration** - Libadwaita styling, adaptive layouts
- **📦 Cross-Platform Packaging** - Flatpak bundles for x86_64 and aarch64

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
- GNOME Platform 47 (for Flatpak builds)

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

### Multi-Architecture Flatpak Bundles

Pre-built Flatpak bundles are available for multiple architectures from GitHub Actions or Releases:

**Supported Architectures:**
- **x86_64**: Intel/AMD 64-bit systems (most desktops and laptops)
- **aarch64**: ARM 64-bit systems (mobile devices, Raspberry Pi, ARM SBCs)

**Installation Steps:**
1. **Check your architecture**: `uname -m`
2. **Download** the appropriate bundle from [Releases](https://github.com/andrew-stclair/gnome-wardrive/releases) or [Actions](https://github.com/andrew-stclair/gnome-wardrive/actions)
3. **Install**: `flatpak install com.andrewstclair.Wardrive-{arch}.flatpak` 
4. **Run**: `flatpak run com.andrewstclair.Wardrive`

**Architecture Selection:**
- If `uname -m` shows `x86_64` → Download `com.andrewstclair.Wardrive-x86_64.flatpak`
- If `uname -m` shows `aarch64` or `arm64` → Download `com.andrewstclair.Wardrive-aarch64.flatpak`

### From Source

Build from source for development or custom configurations (see Building section above).

### 📱 Mobile Linux Installation

For detailed mobile device installation, optimization, and troubleshooting, see [MOBILE_LINUX.md](MOBILE_LINUX.md).

### Multi-Architecture Details

For comprehensive information about architecture support, compatibility, and troubleshooting, see [MULTI_ARCH.md](MULTI_ARCH.md).

## Privacy and Legal Considerations

This application collects GPS location data and WiFi network information. Users are responsible for:
- Compliance with local laws regarding WiFi scanning
- Following privacy regulations in their jurisdiction
- Securing any exported data containing sensitive information

See [PRIVACY.md](PRIVACY.md) for detailed privacy guidelines and data handling practices.

## License

GPL-3.0+

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

**Important for contributors**: Follow the privacy guidelines in [PRIVACY.md](PRIVACY.md) and [.github/.copilot-instructions.md](.github/.copilot-instructions.md) to ensure no personally identifiable information is committed to the repository.