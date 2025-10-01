# Privacy and Data Handling Notice

## Overview

This document outlines privacy considerations and data handling practices for the GNOME Wardrive application and its development.

## Personal Information Protection

### Development Guidelines

**All contributors and maintainers must ensure:**
- No real GPS coordinates are committed to the repository
- No real WiFi network names (SSIDs) or MAC addresses (BSSIDs) are included in code or documentation  
- Test data uses generic, non-identifying placeholders
- Debug output is sanitized to prevent personal information leaks
- Documentation examples use privacy-safe placeholder data

### Example Safe Placeholder Data

**GPS Coordinates:**
- Use generic locations: `40.7128, -74.0060` (NYC), `51.5074, -0.1278` (London)
- Avoid coordinates that could identify specific locations

**Network Information:**  
- SSIDs: `ExampleNetwork`, `WiFi_Network_1`, `TestAP`
- BSSIDs: `00:11:22:33:44:55`, `AA:BB:CC:DD:EE:FF`
- Use documentation-safe MAC address ranges

**Debug Output Sanitization:**
- Location updates: "Location updated: coordinates available (±1.0m accuracy)"
- Network detection: "Network detected: signal 75%" (no SSID/BSSID)
- Device info: "Found 2 WiFi devices" (no interface names)

### Runtime Data Handling

**The application handles sensitive data as follows:**

1. **GPS Coordinates**: Displayed in the UI and stored temporarily for export, but never logged to console with full precision
2. **WiFi Networks**: SSID and BSSID information is collected for wardriving purposes but should be handled according to local privacy laws
3. **Export Data**: Users are responsible for securing exported CSV/KML/GPX files containing sensitive location and network data

### User Privacy Responsibilities

**Users should be aware that:**
- GPS location data is collected and can be exported
- WiFi network information (names and MAC addresses) is collected
- Exported files contain potentially sensitive information
- Users are responsible for compliance with local privacy and data protection laws
- The app does not transmit data over the network, all data stays local

### Developer Privacy Responsibilities  

**When contributing:**
- Test with synthetic/mock data when possible
- Redact any real coordinates or network information from commits
- Use privacy-preserving examples in documentation
- Ensure debug output doesn't expose sensitive information
- Follow the sanitization guidelines in `.github/.copilot-instructions.md`

## Legal Considerations

**This application is intended for:**
- Educational purposes
- Network security research
- Personal WiFi network documentation
- Location tracking for legitimate purposes

**Users must ensure compliance with:**
- Local laws regarding WiFi network scanning
- Privacy regulations in their jurisdiction  
- Terms of service for networks they interact with
- Data protection requirements for any collected information

## Data Security

**The application:**
- Stores all data locally (no cloud transmission)
- Does not require internet connectivity for core functionality
- Uses standard file permissions for exported data
- Provides CSV/KML/GPX export formats for user control over data

**Users should:**
- Secure exported files appropriately
- Consider encryption for sensitive wardrive data
- Regularly clean up old scan data
- Be mindful of who has access to their device and exported files