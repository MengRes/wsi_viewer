# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['wsi_viewer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),  # Include resource files
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'openslide',
        'openslide_bin',
        'PIL',
        'PIL.Image',
        'PIL.ImageQt',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add OpenSlide dynamic libraries
import os
import glob
from PyInstaller.utils.hooks import collect_dynamic_libs

# Collect OpenSlide dynamic libraries
openslide_libs = collect_dynamic_libs('openslide')
for lib_path, lib_name in openslide_libs:
    a.binaries.append((lib_name, lib_path, 'BINARY'))

# Also try to find OpenSlide libraries in common locations
openslide_paths = [
    '/usr/local/lib/libopenslide.dylib',
    '/opt/homebrew/lib/libopenslide.dylib',
    '/usr/lib/libopenslide.dylib',
]

for lib_path in openslide_paths:
    if os.path.exists(lib_path):
        a.binaries.append(('libopenslide.1.dylib', lib_path, 'BINARY'))
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/wsi_viewer.icns' if sys.platform == 'darwin' else 'resources/wsi_viewer.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WSI Viewer',
) 