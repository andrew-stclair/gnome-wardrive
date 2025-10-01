# Contributing to GNOME Wardrive

Thank you for your interest in contributing to GNOME Wardrive! This document provides guidelines for contributing to the project.

## Code of Conduct

This project follows the [GNOME Code of Conduct](https://conduct.gnome.org/). Please be respectful and inclusive in all interactions.

## Getting Started

### Development Environment

1. Install required dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-nm-1.0 gir1.2-geoclue-2.0 meson ninja-build build-essential debhelper dh-python

   # Fedora
   sudo dnf install python3-gobject gtk4-devel libadwaita-devel NetworkManager-glib-devel geoclue2-devel meson ninja-build rpm-build
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gnome-wardrive.git
   cd gnome-wardrive
   ```

3. Install Python dependencies (if developing):
   ```bash
   pip install -r requirements.txt
   ```

4. Build and run:
   ```bash
   meson setup builddir
   meson compile -C builddir
   ./builddir/src/gnome-wardrive
   ```

### Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Write tests for new functionality

### Git Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write tests if applicable
5. Commit your changes with descriptive messages
6. Push to your fork: `git push origin feature/your-feature`
7. Create a Pull Request

### Commit Messages

Use clear, descriptive commit messages:
- Start with a capital letter
- Use imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add detailed description after a blank line if needed

Example:
```
Add export to GPX format

Implement GPX export functionality that includes both waypoints
for WiFi networks and a track from the GPS route.
```

## Types of Contributions

### Bug Reports

- Use the bug report template
- Include steps to reproduce
- Provide system information
- Include relevant logs or error messages

### Feature Requests

- Use the feature request template
- Explain the use case
- Consider alternative approaches
- Be open to discussion

### Code Contributions

#### Areas for Contribution

- **UI/UX improvements**: Enhance the user interface
- **Export formats**: Add new data export formats
- **Performance**: Optimize scanning and data processing
- **Testing**: Add unit and integration tests
- **Documentation**: Improve code documentation and user guides
- **Accessibility**: Improve keyboard navigation and screen reader support
- **Internationalization**: Add translations

#### Pull Request Guidelines

- Reference any related issues
- Include a clear description of changes
- Add tests for new functionality
- Update documentation as needed
- Ensure CI passes
- Be responsive to review feedback

### Documentation

- Fix typos and improve clarity
- Add examples and use cases
- Update installation instructions
- Improve API documentation

## Testing

### Running Tests

```bash
meson test -C builddir
```

### Adding Tests

- Add unit tests for new functions
- Test error conditions
- Mock external dependencies (NetworkManager, GeoClue)

## Debian Package Development

### Building Debian Package

```bash
./build-deb.sh
```

### Testing Debian Package

```bash
# Install the built package
sudo dpkg -i gnome-wardrive_*.deb

# Or run directly from build directory
./builddir/src/gnome-wardrive
```

## Security Considerations

Since this application deals with network scanning and location data:

- Be mindful of privacy implications
- Follow secure coding practices
- Validate all user inputs
- Handle sensitive data appropriately
- Consider legal implications of wardriving in different jurisdictions

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Create a new issue for discussion
3. Join the GNOME community channels

Thank you for contributing to GNOME Wardrive!