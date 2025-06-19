# WSI Viewer - Whole Slide Image Viewer

A high-performance Whole Slide Image (WSI) viewer based on PyQt5 and OpenSlide, supporting multiple WSI file formats.

## Features

### 🖼️ Image Viewing
- Support for multiple WSI file formats (SVS, TIFF, NDPI, VMS, VMR, SCN, MRXS, TIF, SVSLIDE, TMA)
- Multi-level image display with automatic optimal level selection
- Smooth zooming and panning operations
- Real-time thumbnail display
- Intelligent memory management for large WSI files

### 📊 Metadata Management
- Tree-structured display of image metadata with expand/collapse support
- Automatic text wrapping for long content
- Tooltips showing complete information
- Support for saving metadata to text files

### 💾 Image Saving
- Save complete WSI image content (not just current view)
- Intelligent resolution selection (target ~4 million pixels)
- Support for multiple output formats: PNG, JPEG, BMP, TIFF
- Progress display and cancellation support
- Automatic embedding of image metadata

### 🎨 User Interface
- Modern interface design
- Collapsible left metadata panel
- Right main view area
- Top-right thumbnail
- Status bar with detailed information
- Mac dock icon support

## Requirements

### System Requirements
- Python 3.7+
- macOS (tested) or Linux/Windows
- Minimum 4GB RAM (8GB+ recommended)

### Dependencies
```
PyQt5>=5.15.0
openslide-python>=3.4.1
Pillow>=8.0.0
pyinstaller>=5.0.0
setuptools>=45.0.0
wheel>=0.37.0
```

## Installation

### Option 1: Run from Source
1. Clone or download the project:
```bash
git clone <repository-url>
cd wsi_tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python wsi_viewer.py
```

### Option 2: Use Pre-built Executable
Download the latest release for your platform:
- **macOS**: `WSI Viewer.app` (drag to Applications folder)
- **Windows**: `WSI Viewer.exe` 
- **Linux**: `wsi-viewer` executable

## Usage

### Basic Operations
1. **Open File**: Click "File" → "Open" or use Ctrl+O shortcut
2. **Zoom**: Use mouse wheel or toolbar zoom buttons
3. **Pan**: Hold left mouse button and drag
4. **View Metadata**: Expand/collapse metadata items in the left panel

### Saving Features
1. **Save Complete Image**: Click "File" → "Save Image"
   - Choose save format (PNG/JPEG/BMP/TIFF)
   - Program automatically selects optimal resolution
   - Support for canceling save operation

2. **Save Metadata**: Click "File" → "Save Metadata"
   - Save as formatted text file
   - Contains all image property information

### Interface Layout
- **Left Panel**: Tree-structured metadata, collapsible
- **Main View**: Image display area with zoom and pan support
- **Thumbnail**: Top-right small image showing current view position
- **Status Bar**: Shows current zoom level, image information, etc.

## Building from Source

### Quick Build
```bash
# macOS/Linux
chmod +x build.sh
./build.sh

# Windows
build.bat
```

### Advanced Build Options
```bash
# Build for specific platform
python build_app.py --target macos
python build_app.py --target windows
python build_app.py --target linux

# Create icons for all platforms
python build_app.py --create-icons
```

### Manual PyInstaller Commands
```bash
# macOS
pyinstaller --clean --windowed \
    --name="WSI Viewer" \
    --icon=resources/wsi_viewer.icns \
    --add-data="resources:resources" \
    wsi_viewer.py

# Windows
pyinstaller --clean --windowed ^
    --name="WSI Viewer" ^
    --icon=resources/wsi_viewer.ico ^
    --add-data="resources;resources" ^
    wsi_viewer.py

# Linux
pyinstaller --clean --windowed \
    --name="wsi-viewer" \
    --add-data="resources:resources" \
    wsi_viewer.py
```

For detailed build instructions, see [BUILD.md](BUILD.md) and [PACKAGING.md](PACKAGING.md).

## Technical Features

### Performance Optimization
- Intelligent level selection: Automatically selects optimal image level based on display area
- Memory management: Avoids loading oversized image data into memory
- Asynchronous loading: Large file loading doesn't block the interface

### Compatibility
- Support for multiple WSI formats
- Handles missing image levels gracefully
- Automatic handling of different image resolutions

### User Experience
- Progress display: Shows progress bars for long operations
- Error handling: User-friendly error messages
- Keyboard shortcuts: Common operations support keyboard shortcuts

## File Structure

```
wsi_tool/
├── wsi_viewer.py          # Main program file
├── run_wsi_viewer.py      # Launcher script
├── test_wsi_viewer.py     # Test file
├── requirements.txt       # Dependency list
├── README.md             # Documentation
├── BUILD.md              # Build instructions
├── PACKAGING.md          # Packaging guide
├── build_app.py          # Cross-platform build script
├── build.sh              # Unix build script
├── build.bat             # Windows build script
├── setup.py              # Package setup
├── wsi_viewer.spec       # PyInstaller spec
├── create_windows_icon.py # Icon generation
├── create_iconset.sh     # Icon generation script
├── resources/            # Resource files
│   ├── wsi_viewer.icns   # Mac application icon
│   ├── wsi_viewer.ico    # Windows icon
│   └── *.png            # Icons in various sizes
└── dist/                 # Build output (generated)
    ├── WSI Viewer.app    # macOS application
    ├── WSI Viewer.exe    # Windows executable
    └── wsi-viewer        # Linux executable
```

## Development

### Main Components
- `WSIViewer`: Main window class
- `ImageDisplayWidget`: Image display component
- `MetadataWidget`: Metadata display component
- `ThumbnailWidget`: Thumbnail component

### Key Features
- Multi-level image processing
- Metadata parsing and display
- Image saving and export
- User interface management

## Troubleshooting

### Common Issues
1. **Image won't load**: Check if file format is supported, ensure file is complete
2. **Insufficient memory**: Close other programs or use smaller WSI files
3. **Save fails**: Check disk space, ensure write permissions
4. **Build fails**: Install PyInstaller and check dependencies

### Performance Tips
- For large WSI files, use SSD storage
- Ensure sufficient memory (8GB+ recommended)
- Avoid opening multiple large files simultaneously

## Distribution

### Pre-built Packages
- **macOS**: Download `WSI Viewer.zip` and extract to Applications
- **Windows**: Download and run `WSI Viewer.exe`
- **Linux**: Download and run `wsi-viewer` executable

### Building for Distribution
See [BUILD.md](BUILD.md) for detailed instructions on creating distributable packages.

## Changelog

### v1.0.0
- Initial release
- Basic WSI viewing functionality
- Metadata display
- Image saving functionality

### Latest Updates
- Improved save functionality: Now saves complete image content
- Added progress display and cancellation
- Optimized memory usage
- Enhanced user interface
- Added cross-platform packaging support

## License

This project is licensed under the MIT License.

## Contributing

Issues and Pull Requests are welcome to improve this project.

## Contact

For questions or suggestions, please contact via GitHub Issues. 