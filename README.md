# GNOME Wardrive

A modern GNOME application for WiFi wardriving built with Python, GTK4, and Libadwaita.  
**Optimized for Linux mobile devices** like PinePhone, Librem 5, and postmarketOS.

## Features

- **📱 Mobile Linux First** - Native ARM64 builds for PinePhone, Librem 5, postmarketOS devices
- **🔄 Adaptive Interface** - Touch-optimized UI that works from 320px phone screens to desktop
- **📡 System WiFi Scanning** - Uses NetworkManager D-Bus API (no root required)
- **🌍 GPS Location Tracking** - Native GeoClue integration for accurate positioning
- **💾 Multiple Export Formats** - CSV, KML, GPX for analysis and mapping
- **👆 Touch-Friendly Design** - 48px minimum touch targets, bottom action bars
- **🎨 Native GNOME Integration** - Libadwaita styling, adaptive layouts
- **📦 Native Packaging** - Debian packages for x86_64 and aarch64

## WiFi Scanning

This application uses a **passive WiFi monitoring** approach that works reliably across different Linux systems:

- **Passive Monitoring**: Detects networks that are actively beaconing or being scanned by other devices
- **No System Configuration**: Works out-of-the-box without requiring special permissions or system modifications  
- **Native Integration**: Direct access to NetworkManager for optimal performance
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

## Building & Installation

### Debian Package (Recommended)

For Debian/Ubuntu systems, build and install as a native package:

```bash
# 1. Install dependencies and build the package
./build-deb.sh

# 2. Install the package
sudo dpkg -i ../gnome-wardrive_*.deb
sudo apt-get install -f  # Fix any missing dependencies
```

#### Manual Debian Package Build

If you prefer to build manually:

```bash
# Install build dependencies
sudo apt-get install debhelper dh-python python3-all python3-setuptools \
                     meson ninja-build pkg-config libgtk-4-dev \
                     libadwaita-1-dev python3-gi-dev gir1.2-gtk-4.0 \
                     gir1.2-adw-1 gir1.2-nm-1.0 libnm-dev libglib2.0-dev \
                     glib-compile-resources desktop-file-utils appstream-util \
                     build-essential devscripts lintian

# Build the package
debuild -us -uc -b
```

### Development & Testing

```bash
# 1. Install runtime dependencies
./install-deps.sh

# 2. Test and run the application
./quick-test.sh
```

### Manual Build with Meson

```bash
# Install build dependencies
sudo apt install meson ninja-build libadwaita-1-dev python3-gi-dev

# Build
meson setup builddir
meson compile -C builddir

# Run
./builddir/src/gnome-wardrive
```

## Installation

Download pre-built packages from the [Releases](https://github.com/andrew-stclair/gnome-wardrive/releases) page:

### Debian/Ubuntu Systems
1. Download the appropriate `.deb` file for your architecture (`amd64` for Intel/AMD, `arm64` for ARM)
2. Install: `sudo dpkg -i gnome-wardrive_*_{arch}.deb`
3. Fix dependencies: `sudo apt-get install -f`
4. Run: `gnome-wardrive`

### Architecture Detection
Run `dpkg --print-architecture` to check your system:
- `amd64` → Download the amd64 package
- `arm64` → Download the arm64 package

### From Source

Build from source for development or custom configurations (see Building section above).

### 📱 Mobile Linux Installation

For detailed mobile device installation and optimization, see [MOBILE_LINUX.md](MOBILE_LINUX.md).

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