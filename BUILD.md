# Building WSI Viewer

This document explains how to build WSI Viewer into standalone executables for different platforms.

## Prerequisites

### System Requirements
- Python 3.7 or higher
- pip package manager
- Sufficient disk space (at least 2GB free)

### Platform-Specific Requirements

#### macOS
- macOS 10.14 or higher
- Xcode Command Line Tools (install via `xcode-select --install`)

#### Windows
- Windows 10 or higher
- Visual Studio Build Tools (optional, for some dependencies)

#### Linux
- Ubuntu 18.04+ or similar distribution
- Build essentials: `sudo apt-get install build-essential`

## Quick Build

### macOS
```bash
# Make script executable
chmod +x build.sh

# Build for macOS
./build.sh
```

### Windows
```cmd
# Run the batch file
build.bat
```

### Linux
```bash
# Make script executable
chmod +x build.sh

# Build for Linux
./build.sh
```

## Advanced Build Options

### Using Python Script
```bash
# Build for current platform
python build_app.py

# Build for specific platform
python build_app.py --target macos
python build_app.py --target windows
python build_app.py --target linux

# Create icons for all platforms
python build_app.py --create-icons
```

### Manual PyInstaller Commands

#### macOS
```bash
pyinstaller --clean --windowed \
    --name="WSI Viewer" \
    --icon=resources/wsi_viewer.icns \
    --add-data="resources:resources" \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=openslide \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageQt \
    wsi_viewer.py
```

#### Windows
```cmd
pyinstaller --clean --windowed ^
    --name="WSI Viewer" ^
    --icon=resources/wsi_viewer.ico ^
    --add-data="resources;resources" ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=openslide ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageQt ^
    wsi_viewer.py
```

#### Linux
```bash
pyinstaller --clean --windowed \
    --name="wsi-viewer" \
    --add-data="resources:resources" \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=openslide \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageQt \
    wsi_viewer.py
```

## Output Files

After successful build, you'll find the following in the `dist` directory:

### macOS
- `WSI Viewer.app` - macOS application bundle
- Can be double-clicked to run
- Can be dragged to Applications folder

### Windows
- `WSI Viewer.exe` - Windows executable
- `WSI Viewer/` folder containing all dependencies
- Can be run directly or distributed as a folder

### Linux
- `wsi-viewer` - Linux executable
- `wsi-viewer/` folder containing all dependencies

## Distribution

### macOS
1. Create a DMG file (optional):
   ```bash
   # Install create-dmg if needed
   brew install create-dmg
   
   # Create DMG
   create-dmg \
     --volname "WSI Viewer" \
     --window-pos 200 120 \
     --window-size 600 300 \
     --icon-size 100 \
     --icon "WSI Viewer.app" 175 120 \
     --hide-extension "WSI Viewer.app" \
     --app-drop-link 425 120 \
     "WSI Viewer.dmg" \
     "dist/"
   ```

2. Or simply zip the `.app` file:
   ```bash
   cd dist
   zip -r "WSI Viewer.zip" "WSI Viewer.app"
   ```

### Windows
1. Create an installer using tools like Inno Setup or NSIS
2. Or distribute the entire `WSI Viewer` folder as a zip file

### Linux
1. Create a `.deb` package (Ubuntu/Debian):
   ```bash
   # Install checkinstall
   sudo apt-get install checkinstall
   
   # Create package
   cd dist
   sudo checkinstall --pkgname=wsi-viewer --pkgversion=1.0.0 --backup=no
   ```

2. Or distribute the executable and folder as a tar.gz:
   ```bash
   cd dist
   tar -czf wsi-viewer.tar.gz wsi-viewer/
   ```

## Troubleshooting

### Common Issues

1. **PyInstaller not found**
   ```bash
   pip install pyinstaller
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Icon file not found**
   ```bash
   python create_windows_icon.py
   ```

4. **OpenSlide library issues**
   - macOS: `brew install openslide`
   - Ubuntu: `sudo apt-get install libopenslide-dev`
   - Windows: Download from OpenSlide website

5. **Large executable size**
   - This is normal for PyQt5 applications
   - Consider using UPX compression (add `--upx-dir=/path/to/upx` to PyInstaller)

### Debug Build
For debugging, use the `--console` flag instead of `--windowed`:
```bash
pyinstaller --console --name="WSI Viewer" wsi_viewer.py
```

### Clean Build
To start fresh:
```bash
rm -rf build/ dist/ *.spec
```

## Performance Optimization

1. **Reduce executable size**:
   - Use `--exclude-module` to exclude unused modules
   - Use UPX compression
   - Strip debug symbols

2. **Improve startup time**:
   - Use `--onefile` for single executable (slower startup)
   - Use `--onedir` for folder distribution (faster startup)

3. **Memory usage**:
   - Monitor memory usage during build
   - Consider using `--optimize=2` for Python optimization

## Code Signing (macOS)

For distribution on macOS, you may want to code sign your application:

```bash
# Get a Developer ID certificate
# Then sign the app
codesign --force --deep --sign "Developer ID Application: Your Name" "dist/WSI Viewer.app"

# Verify signature
codesign --verify --deep --strict "dist/WSI Viewer.app"
``` 