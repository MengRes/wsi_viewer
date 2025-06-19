# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wsi_viewer.py'],
    pathex=[],
    binaries=[('/opt/homebrew/lib/libopenslide.dylib', '.')],
    datas=[('resources', 'resources')],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'openslide', 'openslide_bin', 'PIL', 'PIL.Image', 'PIL.ImageQt'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WSI Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/wsi_viewer.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WSI Viewer',
)
app = BUNDLE(
    coll,
    name='WSI Viewer.app',
    icon='resources/wsi_viewer.icns',
    bundle_identifier=None,
)
