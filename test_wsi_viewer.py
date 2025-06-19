#!/usr/bin/env python3
"""
WSI Viewer Test Script
Used to verify that the program can start and run normally
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported normally"""
    try:
        import PyQt5
        print("✓ PyQt5 import successful")
    except ImportError as e:
        print(f"✗ PyQt5 import failed: {e}")
        return False
    
    try:
        import openslide
        print("✓ OpenSlide import successful")
    except ImportError as e:
        print(f"✗ OpenSlide import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy import successful")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow import successful")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    return True

def test_wsi_viewer_import():
    """Test if WSI viewer module can be imported normally"""
    try:
        from wsi_viewer import WSIImageViewer
        print("✓ WSI viewer module import successful")
        return True
    except ImportError as e:
        print(f"✗ WSI viewer module import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error occurred while importing WSI viewer module: {e}")
        return False

def main():
    print("WSI Viewer Test")
    print("=" * 50)
    
    # Test module imports
    if not test_imports():
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    # Test WSI viewer import
    if not test_wsi_viewer_import():
        print("\nWSI viewer module has issues, please check the code")
        return False
    
    print("\n✓ All tests passed!")
    print("You can run the following command to start WSI viewer:")
    print("python wsi_viewer.py")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 