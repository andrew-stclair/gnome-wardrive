project('gnome-wardrive', 
  version: '1.0.0',
  meson_version: '>= 0.60.0',
  default_options: [
    'warning_level=2',
  ],
)

# Dependencies
python = import('python')
i18n = import('i18n')
py_installation = python.find_installation('python3')

# Required dependencies check
dependency('gtk4')
dependency('libadwaita-1')
dependency('pygobject-3.0')

# Install directories
bindir = get_option('bindir')
libexecdir = get_option('libexecdir')
datadir = get_option('datadir')

pkgdatadir = datadir / meson.project_name()
moduledir = pkgdatadir / 'gnome_wardrive'

# Configuration
conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

# Subdirectories
subdir('data')
subdir('src')
subdir('po')