from setuptools import setup, find_packages

setup(
    name="wsi-viewer",
    version="1.0.0",
    description="A high-performance Whole Slide Image (WSI) viewer",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "openslide-python>=3.4.1",
        "Pillow>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "wsi-viewer=wsi_viewer:main",
        ],
    },
    python_requires=">=3.7",
) 