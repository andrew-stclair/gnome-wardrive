# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in GNOME Wardrive, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email security details to [your-security-email@example.com]
3. Include as much detail as possible:
   - Steps to reproduce the vulnerability
   - Potential impact
   - Suggested fix (if you have one)

## Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a more detailed response within 7 days
- We will work on a fix and coordinate disclosure timing with you

## Security Considerations for Users

Since GNOME Wardrive performs network scanning and location tracking:

### Privacy
- The application stores network and location data locally
- Be aware of local laws regarding WiFi scanning and data collection
- Consider the privacy implications of the data you collect

### Legal Compliance
- Wardriving laws vary by jurisdiction
- Ensure you comply with local regulations
- Only scan networks you own or have permission to scan
- Do not attempt to access secured networks

### Data Security
- Exported data may contain sensitive location information
- Secure your exported files appropriately
- Consider encrypting sensitive data exports

## Permissions Required

The application requires these system permissions:
- Network access (for WiFi scanning via NetworkManager)
- Location access (for GPS tracking via GeoClue)
- File system access (for data export)

These permissions are necessary for core functionality and are used only as intended.