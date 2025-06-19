# GitHub Release Guide

## 📋 Preparation

### 1. Ensure the application is properly packaged
```bash
# Check application files
ls -la "dist/WSI Viewer.app"

# Create compressed package (completed)
cd dist && zip -r "WSI_Viewer_macOS.zip" "WSI Viewer.app"
```

### 2. Prepare release materials
- ✅ Application package: `WSI_Viewer_macOS.zip`
- ✅ Application icon: `resources/wsi_viewer_1024.png`
- ✅ Release notes: See content below

## 🚀 Creating a GitHub Release

### Step 1: Access GitHub Repository
1. Open your GitHub repository page
2. Click on the "Releases" tab
3. Click "Create a new release" or "Draft a new release"

### Step 2: Fill in Release Information

#### Tag Version
```
v1.0.0
```

#### Release Title
```
WSI Viewer v1.0.0 - Professional Whole Slide Image Viewer
```

#### Release Notes
```markdown
## 🎉 WSI Viewer v1.0.0 Official Release

WSI Viewer is a professional Whole Slide Image (WSI) viewer built with PyQt5 and OpenSlide.

### ✨ Key Features

#### 🔍 Image Viewing
- Support for multiple WSI formats: SVS, TIFF, NDPI, VMS, VMU, SCN, MRXS
- High-performance image rendering and display
- Smooth zoom and pan operations
- Multi-resolution support

#### 💾 File Operations
- Open WSI files
- Save current view as image
- Support for multiple output formats (PNG, JPEG, TIFF)

#### 🎛️ User Interface
- Modern PyQt5 interface
- Intuitive toolbar and menus
- Status bar showing image information
- Progress bar for loading status

#### ⚡ Performance Optimization
- Memory-optimized large file processing
- Asynchronous loading mechanism
- Smart caching strategy

### 🛠️ Technical Features

- **Framework**: PyQt5
- **Image Processing**: OpenSlide, PIL
- **Platform**: macOS 10.14+
- **Architecture**: Native macOS application

### 📥 Download and Installation

#### macOS Users
1. Download `WSI_Viewer_macOS.zip`
2. Extract the file
3. Drag `WSI Viewer.app` to the Applications folder
4. On first run, allow execution in System Preferences > Security & Privacy
5. Double-click to launch the application

### 🔧 System Requirements

- **Operating System**: macOS 10.14 or higher
- **Memory**: At least 4GB RAM
- **Storage**: 100MB available space
- **Supported File Formats**: SVS, TIFF, NDPI, VMS, VMU, SCN, MRXS, TIF, JPEG, PNG

### 🚀 Usage Instructions

#### Basic Operations
1. **Open File**: Click "Open" button or use Cmd+O
2. **Zoom**: Use mouse wheel or toolbar buttons
3. **Pan**: Hold left mouse button and drag
4. **Save**: Click "Save" button to save current view

#### Keyboard Shortcuts
- `Cmd+O`: Open file
- `Cmd+S`: Save image
- `Cmd+Q`: Quit application
- `+/-`: Zoom
- `Space`: Pan mode

### 🐛 Known Issues

- First launch may take longer (loading dependency libraries)
- Some very large files may require more memory
- Interface may appear small on low-resolution displays

### 🔮 Future Plans

- [ ] Windows version support
- [ ] Linux version support
- [ ] Batch processing functionality
- [ ] Image annotation features
- [ ] Plugin system

### 📞 Support and Feedback

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check README.md for detailed instructions
- **Contributions**: Pull requests are welcome

### 📄 License

This project is licensed under the MIT License.

---

Thank you for using WSI Viewer! 🎉
```

### Step 3: Upload Files
1. Click "Attach binaries by dropping them here or selecting them"
2. Select the `WSI_Viewer_macOS.zip` file
3. Wait for upload to complete

### Step 4: Set Release Options
- ✅ **Set as the latest release**: Check (set as latest version)
- ✅ **Create a discussion for this release**: Optional (create discussion)

### Step 5: Publish
Click the "Publish release" button

## 📊 Post-Release Management

### 1. Update README.md
Add download links to README.md:

```markdown
## 📥 Download

### Latest Version
- [WSI Viewer v1.0.0 for macOS](https://github.com/your-username/your-repo-name/releases/latest/download/WSI_Viewer_macOS.zip)

### System Requirements
- macOS 10.14 or higher
- At least 4GB RAM
```

### 2. Create Download Page
You can create a `downloads.md` file in the repository:

```markdown
# Download Page

## Latest Version v1.0.0

### macOS
- **File**: WSI_Viewer_macOS.zip
- **Size**: ~187MB
- **System Requirements**: macOS 10.14+
- **Download**: [GitHub Release](https://github.com/your-username/your-repo-name/releases/latest/download/WSI_Viewer_macOS.zip)

## Installation Instructions

1. Download the compressed package for your platform
2. Extract the file
3. Drag the application to the Applications folder
4. Allow execution on first run (System Preferences > Security & Privacy)
5. Double-click to launch the application

## Supported File Formats

- SVS (Aperio)
- TIFF (BigTIFF)
- NDPI (Hamamatsu)
- VMS, VMU (Ventana)
- SCN (Leica)
- MRXS (3DHistech)
- Standard image formats: PNG, JPEG, TIFF
```

## 🔄 Automated Releases

### Using GitHub Actions
You can create `.github/workflows/release.yml` to automate the release process:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build application
      run: |
        python build_app.py
    
    - name: Create release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/WSI_Viewer_macOS.zip
        body_path: RELEASE_NOTES.md
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📈 Release Statistics

After release, you can see on GitHub:
- Download count statistics
- User feedback and issue reports
- Community discussions

## 🎯 Best Practices

1. **Version Naming**: Use semantic versioning (e.g., v1.0.0)
2. **Release Notes**: Detailed description of new features and fixes
3. **File Naming**: Include platform and version information
4. **Testing**: Test on target platform before release
5. **Documentation**: Provide detailed installation and usage instructions

## 🔗 Related Links

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions) 