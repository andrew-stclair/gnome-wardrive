# Install Python modules
python_sources = [
  '__init__.py',
  'main.py',
  'application.py',
  'window.py',
  'wifi_scanner.py',
  'location_service.py',
  'data_manager.py',
]

install_data(python_sources, install_dir: moduledir)

# Main executable
conf_file = configure_file(
  input: 'gnome-wardrive.in',
  output: 'gnome-wardrive',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)