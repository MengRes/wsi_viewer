#!/bin/bash

# WSI Viewer Build Script
echo "WSI Viewer Build Script"
echo "======================"

# Check if we're in the right directory
if [ ! -f "wsi_viewer.py" ]; then
    echo "Error: wsi_viewer.py not found. Please run this script from the project root."
    exit 1
fi

# Install PyInstaller if not already installed
echo "Installing PyInstaller..."
pip install pyinstaller

# Create Windows icon if needed
if [ "$1" = "--create-icons" ] || [ "$(uname)" = "Darwin" ]; then
    echo "Creating Windows icon..."
    python create_windows_icon.py
fi

# Find OpenSlide library
find_openslide_lib() {
    local paths=(
        "/usr/local/lib/libopenslide.dylib"
        "/opt/homebrew/lib/libopenslide.dylib"
        "/usr/lib/libopenslide.dylib"
        "/usr/local/lib/libopenslide.so"
        "/usr/lib/libopenslide.so"
    )
    
    for path in "${paths[@]}"; do
        if [ -f "$path" ]; then
            echo "Found OpenSlide library: $path"
            echo "$path"
            return 0
        fi
    done
    
    echo "Warning: OpenSlide library not found in common locations"
    echo ""
    return 1
}

# Build based on platform
if [ "$(uname)" = "Darwin" ]; then
    echo "Building for macOS..."
    
    # Find OpenSlide library
    openslide_lib=$(find_openslide_lib)
    
    # Build command
    cmd="pyinstaller --clean --windowed \
        --name=\"WSI Viewer\" \
        --icon=resources/wsi_viewer.icns \
        --add-data=\"resources:resources\" \
        --additional-hooks-dir=. \
        --hidden-import=PyQt5.QtCore \
        --hidden-import=PyQt5.QtGui \
        --hidden-import=PyQt5.QtWidgets \
        --hidden-import=openslide \
        --hidden-import=openslide_bin \
        --hidden-import=PIL \
        --hidden-import=PIL.Image \
        --hidden-import=PIL.ImageQt"
    
    # Add OpenSlide library if found
    if [ -n "$openslide_lib" ]; then
        cmd="$cmd --add-binary \"$openslide_lib:.\""
    fi
    
    cmd="$cmd wsi_viewer.py"
    
    eval $cmd
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Building for Windows..."
    pyinstaller --clean --windowed \
        --name="WSI Viewer" \
        --icon=resources/wsi_viewer.ico \
        --add-data="resources;resources" \
        --additional-hooks-dir=. \
        --hidden-import=PyQt5.QtCore \
        --hidden-import=PyQt5.QtGui \
        --hidden-import=PyQt5.QtWidgets \
        --hidden-import=openslide \
        --hidden-import=openslide_bin \
        --hidden-import=PIL \
        --hidden-import=PIL.Image \
        --hidden-import=PIL.ImageQt \
        wsi_viewer.py
else
    echo "Building for Linux..."
    pyinstaller --clean --windowed \
        --name="wsi-viewer" \
        --add-data="resources:resources" \
        --additional-hooks-dir=. \
        --hidden-import=PyQt5.QtCore \
        --hidden-import=PyQt5.QtGui \
        --hidden-import=PyQt5.QtWidgets \
        --hidden-import=openslide \
        --hidden-import=openslide_bin \
        --hidden-import=PIL \
        --hidden-import=PIL.Image \
        --hidden-import=PIL.ImageQt \
        wsi_viewer.py
fi

echo "Build completed! Check the 'dist' directory for the executable." 