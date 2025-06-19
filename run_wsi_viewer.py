#!/usr/bin/env python3
"""
WSI Viewer Launcher Script
Includes dependency checking and error handling
"""

import sys
import os

def check_dependencies():
    """Check required dependencies"""
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    try:
        import openslide
    except ImportError:
        missing_deps.append("openslide-python")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow")
    
    if missing_deps:
        print("Error: Missing the following dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease run the following command to install dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("Starting WSI Viewer...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and start WSI viewer
        from wsi_viewer import main as wsi_main
        wsi_main()
    except ImportError as e:
        print(f"Error: Cannot import WSI viewer module: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An error occurred while starting WSI viewer: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 