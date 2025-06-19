# WSI Viewer v1.0.0 Release Notes

## 🎉 New Version Release

WSI Viewer is a professional Whole Slide Image (WSI) viewer built with PyQt5 and OpenSlide.

## ✨ Key Features

### 🔍 Image Viewing
- Support for multiple WSI formats: SVS, TIFF, NDPI, VMS, VMU, SCN, MRXS
- High-performance image rendering and display
- Smooth zoom and pan operations
- Multi-resolution support

### 💾 File Operations
- Open WSI files
- Save current view as image
- Support for multiple output formats (PNG, JPEG, TIFF)

### 🎛️ User Interface
- Modern PyQt5 interface
- Intuitive toolbar and menus
- Status bar showing image information
- Progress bar for loading status

### ⚡ Performance Optimization
- Memory-optimized large file processing
- Asynchronous loading mechanism
- Smart caching strategy

## 🛠️ Technical Features

- **Framework**: PyQt5
- **Image Processing**: OpenSlide, PIL
- **Platform**: macOS 10.14+
- **Architecture**: Native macOS application

## 📥 Download and Installation

### macOS Users
1. Download `WSI_Viewer_macOS.zip`
2. Extract the file
3. Drag `WSI Viewer.app` to the Applications folder
4. On first run, allow execution in System Preferences > Security & Privacy
5. Double-click to launch the application

## 🔧 System Requirements

- **Operating System**: macOS 10.14 or higher
- **Memory**: At least 4GB RAM
- **Storage**: 100MB available space
- **Supported File Formats**: SVS, TIFF, NDPI, VMS, VMU, SCN, MRXS, TIF, JPEG, PNG

## 🚀 Usage Instructions

### Basic Operations
1. **Open File**: Click "Open" button or use Cmd+O
2. **Zoom**: Use mouse wheel or toolbar buttons
3. **Pan**: Hold left mouse button and drag
4. **Save**: Click "Save" button to save current view

### Keyboard Shortcuts
- `Cmd+O`: Open file
- `Cmd+S`: Save image
- `Cmd+Q`: Quit application
- `+/-`: Zoom
- `Space`: Pan mode

## 🐛 Known Issues

- First launch may take longer (loading dependency libraries)
- Some very large files may require more memory
- Interface may appear small on low-resolution displays

## 🔮 Future Plans

- [ ] Windows version support
- [ ] Linux version support
- [ ] Batch processing functionality
- [ ] Image annotation features
- [ ] Plugin system

## 📞 Support and Feedback

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check README.md for detailed instructions
- **Contributions**: Pull requests are welcome

## 📄 License

This project is licensed under the MIT License.

---

Thank you for using WSI Viewer! 🎉 