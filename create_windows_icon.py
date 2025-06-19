#!/usr/bin/env python3
"""
Script to create Windows .ico file from PNG images
"""

from PIL import Image
import os

def create_ico_file():
    """Create Windows .ico file from PNG images"""
    # Icon sizes for Windows
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    # Load PNG images and resize them
    for size in sizes:
        png_path = f"resources/wsi_viewer_{size}.png"
        if os.path.exists(png_path):
            img = Image.open(png_path)
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(img)
        else:
            print(f"Warning: {png_path} not found")
    
    if images:
        # Save as ICO file
        ico_path = "resources/wsi_viewer.ico"
        images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        print(f"Created {ico_path}")
    else:
        print("No images found to create ICO file")

if __name__ == "__main__":
    create_ico_file() 