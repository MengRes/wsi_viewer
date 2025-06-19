#!/usr/bin/env python3
"""
Cross-platform build script for WSI Viewer
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def clean_build():
    for path in ["dist", "build", "WSI Viewer.spec"]:
        if os.path.isdir(path):
            print(f"Cleaning directory: {path}")
            subprocess.run(["rm", "-rf", path])
        elif os.path.isfile(path):
            print(f"Deleting file: {path}")
            os.remove(path)

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def install_dependencies():
    """Install required packages for building"""
    packages = [
        "pyinstaller>=5.0.0",
        "setuptools",
        "wheel"
    ]
    
    for package in packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"Installing {package}"):
            return False
    return True

def create_windows_icon():
    """Create Windows icon if on Windows or if requested"""
    if platform.system() == "Windows" or "--create-icons" in sys.argv:
        if not run_command([sys.executable, "create_windows_icon.py"], 
                          "Creating Windows icon"):
            return False
    return True

def find_openslide_library():
    """Find OpenSlide library path"""
    openslide_paths = [
        '/usr/local/lib/libopenslide.dylib',
        '/opt/homebrew/lib/libopenslide.dylib',
        '/usr/lib/libopenslide.dylib',
        '/usr/local/lib/libopenslide.so',
        '/usr/lib/libopenslide.so',
    ]
    
    for path in openslide_paths:
        if os.path.exists(path):
            print(f"Found OpenSlide library: {path}")
            return path
    
    print("Warning: OpenSlide library not found in common locations")
    return None

def build_macos():
    """Build for macOS"""
    print("\n=== Building for macOS ===")
    
    # Find OpenSlide library
    openslide_lib = find_openslide_library()
    
    # Create .app bundle
    cmd = [
        "pyinstaller",
        "--clean",
        "--windowed",  # No console window
        "--name=WSI Viewer",
        "--icon=resources/wsi_viewer.icns",
        "--add-data=resources:resources",
        "--additional-hooks-dir=.",  # Use local hook files
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=openslide",
        "--hidden-import=openslide_bin",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageQt",
    ]
    
    # Add OpenSlide library if found
    if openslide_lib:
        cmd.extend(["--add-binary", f"{openslide_lib}:."])
    
    cmd.append("wsi_viewer.py")
    
    if not run_command(cmd, "Building macOS app"):
        return False
    
    # Fix symlink issue
    print("\nFixing symlink issue...")
    frameworks_dir = "dist/WSI Viewer.app/Contents/Frameworks"
    libopenslide_1_symlink = os.path.join(frameworks_dir, "libopenslide.1.dylib")
    libopenslide_dot_dir = os.path.join(frameworks_dir, "libopenslide__dot__1__dot__dylib")
    
    if os.path.islink(libopenslide_1_symlink) and os.path.exists(libopenslide_dot_dir):
        # Remove symlink
        os.remove(libopenslide_1_symlink)
        # Copy real file
        real_lib = os.path.join(libopenslide_dot_dir, "libopenslide.1.dylib")
        if os.path.exists(real_lib):
            import shutil
            shutil.copy2(real_lib, libopenslide_1_symlink)
            print("✓ Symlink fixed")
        else:
            # If not found, use libopenslide.dylib as fallback
            fallback_lib = os.path.join(frameworks_dir, "libopenslide.dylib")
            if os.path.exists(fallback_lib):
                import shutil
                shutil.copy2(fallback_lib, libopenslide_1_symlink)
                print("✓ Fallback library used to fix symlink")
    
    # Create DMG (optional)
    if "--create-dmg" in sys.argv:
        print("\nCreating DMG...")
        # You can add DMG creation logic here
        # For now, just copy the app to a folder
        os.makedirs("dist/WSI Viewer.app", exist_ok=True)
    
    return True

def build_windows():
    """Build for Windows"""
    print("\n=== Building for Windows ===")
    
    # Create Windows executable
    cmd = [
        "pyinstaller",
        "--clean",
        "--windowed",  # No console window
        "--name=WSI Viewer",
        "--icon=resources/wsi_viewer.ico",
        "--add-data=resources;resources",
        "--additional-hooks-dir=.",  # Use local hook files
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=openslide",
        "--hidden-import=openslide_bin",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageQt",
        "wsi_viewer.py"
    ]
    
    if not run_command(cmd, "Building Windows executable"):
        return False
    
    return True

def build_linux():
    """Build for Linux"""
    print("\n=== Building for Linux ===")
    
    cmd = [
        "pyinstaller",
        "--clean",
        "--windowed",
        "--name=wsi-viewer",
        "--add-data=resources:resources",
        "--additional-hooks-dir=.",  # Use local hook files
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=openslide",
        "--hidden-import=openslide_bin",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageQt",
        "wsi_viewer.py"
    ]
    
    if not run_command(cmd, "Building Linux executable"):
        return False
    
    return True

def main():
    """Main build function"""
    print("WSI Viewer Build Script")
    print("=" * 50)
    
    # Auto clean old build artifacts
    clean_build()
    
    # Check if we're in the right directory
    if not os.path.exists("wsi_viewer.py"):
        print("Error: wsi_viewer.py not found. Please run this script from the project root.")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create Windows icon if needed
    if not create_windows_icon():
        return 1
    
    # Determine target platform
    system = platform.system()
    target = None
    
    if "--target" in sys.argv:
        idx = sys.argv.index("--target")
        if idx + 1 < len(sys.argv):
            target = sys.argv[idx + 1].lower()
    
    if not target:
        target = system.lower()
    
    # Build for target platform
    success = False
    if target == "darwin" or target == "macos":
        success = build_macos()
    elif target == "windows":
        success = build_windows()
    elif target == "linux":
        success = build_linux()
    else:
        print(f"Unknown target: {target}")
        print("Supported targets: macos, windows, linux")
        return 1
    
    if success:
        print(f"\n✓ Build completed successfully for {target}")
        print("Output files are in the 'dist' directory")
        return 0
    else:
        print(f"\n✗ Build failed for {target}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 