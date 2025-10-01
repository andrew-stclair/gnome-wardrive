# Install UI files
install_data(
  'ui/window.ui',
  install_dir: pkgdatadir / 'ui'
)

# Install CSS
install_data(
  'style.css',
  install_dir: pkgdatadir
)

# Desktop file
desktop_file = i18n.merge_file(
  input: 'com.andrewstclair.Wardrive.desktop.in',
  output: 'com.andrewstclair.Wardrive.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

# AppStream metainfo
appstream_file = i18n.merge_file(
  input: 'com.andrewstclair.Wardrive.metainfo.xml.in',
  output: 'com.andrewstclair.Wardrive.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'metainfo'
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

# GSchema
install_data(
  'com.andrewstclair.Wardrive.gschema.xml',
  install_dir: datadir / 'glib-2.0/schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

# Icon
install_data(
  'icons/hicolor/scalable/apps/com.andrewstclair.Wardrive.svg',
  install_dir: datadir / 'icons/hicolor/scalable/apps'
)

install_data(
  'icons/hicolor/symbolic/apps/com.andrewstclair.Wardrive-symbolic.svg',
  install_dir: datadir / 'icons/hicolor/symbolic/apps'
)

# GResource
gnome = import('gnome')

gnome.compile_resources('gnome-wardrive',
  'gnome-wardrive.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)