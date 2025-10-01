# Multi-Architecture Support

## Overview

GNOME Wardrive provides native support for multiple CPU architectures through Flatpak bundles, ensuring optimal performance across different device types.

## Supported Architectures

### x86_64 (Intel/AMD 64-bit)
- **Target Systems**: Desktop computers, laptops, workstations
- **Processors**: Intel Core series, AMD Ryzen, Xeon, EPYC
- **Use Cases**: Development workstations, high-performance wardriving setups
- **Bundle**: `com.andrewstclair.Wardrive-x86_64.flatpak`

### aarch64 (ARM 64-bit)  
- **Target Systems**: Mobile devices, single-board computers, ARM servers
- **Processors**: ARM Cortex-A series, Apple Silicon (M1/M2), Snapdragon, Raspberry Pi 4+
- **Use Cases**: Mobile wardriving, portable field research, embedded systems
- **Bundle**: `com.andrewstclair.Wardrive-aarch64.flatpak`

## Architecture Detection

### Automatic Detection
Run this command to identify your system architecture:
```bash
uname -m
```

**Output meanings:**
- `x86_64` → Use x86_64 bundle
- `aarch64` → Use aarch64 bundle  
- `arm64` → Use aarch64 bundle (macOS notation)
- `armv7l` → Not supported (use 64-bit ARM system)

### Manual Detection
If `uname -m` is not available:

**Linux Systems:**
```bash
# Check processor info
cat /proc/cpuinfo | grep -i "architecture\|model name" | head -5

# Check installed packages architecture
dpkg --print-architecture  # Debian/Ubuntu
rpm -qa --queryformat '%{ARCH}\n' | sort -u  # Red Hat/Fedora
```

**Alternative Methods:**
```bash
# Check with lscpu
lscpu | grep Architecture

# Check with file command on a system binary
file /bin/ls
```

## Installation Guide

### Step 1: Download Correct Bundle

**From GitHub Releases:**
1. Visit [Releases page](https://github.com/andrew-stclair/gnome-wardrive/releases)
2. Download the bundle matching your architecture:
   - `com.andrewstclair.Wardrive-x86_64.flatpak` for Intel/AMD systems
   - `com.andrewstclair.Wardrive-aarch64.flatpak` for ARM systems

**From GitHub Actions (Development Builds):**
1. Go to [Actions tab](https://github.com/andrew-stclair/gnome-wardrive/actions)
2. Click on the latest successful workflow run
3. Download the appropriate artifact from the Artifacts section

### Step 2: Install Flatpak Bundle

```bash
# Install the downloaded bundle (replace {arch} with your architecture)
flatpak install com.andrewstclair.Wardrive-{arch}.flatpak

# Verify installation
flatpak list | grep com.andrewstclair.Wardrive
```

### Step 3: Run Application

```bash
# Launch the application
flatpak run com.andrewstclair.Wardrive

# Or use the desktop launcher
# The app will appear in your applications menu as "GNOME Wardrive"
```

## Performance Considerations

### x86_64 Advantages
- **Mature Toolchain**: Highly optimized compilers and libraries
- **Maximum Performance**: Best single-threaded performance for complex operations
- **Full Feature Support**: All GNOME/GTK features available
- **Desktop Integration**: Optimal for multi-monitor setups and desktop workflows

### aarch64 Advantages  
- **Power Efficiency**: Excellent battery life for mobile/field use
- **Thermal Management**: Lower heat generation for fanless operation
- **Mobile Optimized**: Native support for touch interfaces and small screens
- **Embedded Friendly**: Suitable for dedicated wardriving devices

## Compatibility Notes

### Python Code Compatibility
- **Pure Python**: Core application logic is architecture-independent
- **Native Extensions**: PyGObject bindings compiled for each architecture
- **GTK4/Libadwaita**: Native libraries optimized per architecture

### System Integration
- **NetworkManager**: Cross-architecture D-Bus compatibility
- **GeoClue**: Location services work identically across architectures  
- **Flatpak Runtime**: GNOME Platform 46 supports both architectures natively

### Data Format Compatibility
- **Export Files**: CSV, KML, GPX files are identical across architectures
- **Settings**: GSettings schemas are architecture-independent
- **Cache Data**: Internal data structures maintain compatibility

## Troubleshooting

### Wrong Architecture Downloaded
**Symptoms**: Installation fails with "incompatible architecture" error
**Solution**: Download the correct bundle for your system architecture

### Performance Issues on ARM
**Symptoms**: Slow UI responsiveness on ARM devices
**Solutions**: 
- Ensure hardware acceleration is enabled (`--device=dri` in Flatpak)
- Check that you're using aarch64 bundle, not running x86_64 under emulation
- Verify adequate RAM (minimum 1GB recommended)

### Missing Dependencies
**Symptoms**: Application fails to start with missing library errors
**Solution**: Install GNOME Platform 46 runtime:
```bash
flatpak install org.gnome.Platform//{arch}/46
flatpak install org.gnome.Sdk//{arch}/46  # For development
```

### Cross-Architecture Installation
**Not Supported**: Installing x86_64 bundle on ARM system (or vice versa)
**Alternative**: Use architecture-appropriate bundle or build from source

## Development Considerations

### Building for Multiple Architectures
The CI/CD pipeline automatically builds for both architectures using GitHub Actions matrix strategy.

### Testing Multi-Architecture Support
- Automated builds verify compatibility across architectures
- Python code is inherently portable
- Native dependencies (GTK4, NetworkManager) are handled by Flatpak runtime

### Contributing Architecture-Specific Code
- Avoid architecture-specific code when possible
- Use runtime detection for any architecture-dependent behavior
- Test changes on both x86_64 and aarch64 systems when possible

## Future Architecture Support

### Potential Additions
- **riscv64**: RISC-V 64-bit support (pending GNOME Platform availability)
- **s390x**: IBM Z architecture (enterprise use cases)

### Requirements for New Architectures
- GNOME Platform runtime support
- PyGObject availability  
- NetworkManager and GeoClue compatibility
- Community demand and testing resources