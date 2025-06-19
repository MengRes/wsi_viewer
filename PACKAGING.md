# WSI Viewer 打包指南

## 快速开始

### macOS 打包
```bash
# 方法1：使用构建脚本
./build.sh

# 方法2：使用Python脚本
python build_app.py --target macos

# 方法3：直接使用PyInstaller
pyinstaller --clean --windowed \
    --name="WSI Viewer" \
    --icon=resources/wsi_viewer.icns \
    --add-data="resources:resources" \
    wsi_viewer.py
```

### Windows 打包
```cmd
# 方法1：使用批处理文件
build.bat

# 方法2：使用Python脚本
python build_app.py --target windows

# 方法3：直接使用PyInstaller
pyinstaller --clean --windowed ^
    --name="WSI Viewer" ^
    --icon=resources/wsi_viewer.ico ^
    --add-data="resources;resources" ^
    wsi_viewer.py
```

### Linux 打包
```bash
# 方法1：使用构建脚本
./build.sh

# 方法2：使用Python脚本
python build_app.py --target linux

# 方法3：直接使用PyInstaller
pyinstaller --clean --windowed \
    --name="wsi-viewer" \
    --add-data="resources:resources" \
    wsi_viewer.py
```

## 输出文件

打包完成后，在 `dist` 目录中会生成：

### macOS
- `WSI Viewer.app` - 可直接双击运行的应用包
- 可以拖拽到 Applications 文件夹安装

### Windows  
- `WSI Viewer.exe` - 可执行文件
- `WSI Viewer/` 文件夹 - 包含所有依赖

### Linux
- `wsi-viewer` - 可执行文件
- `wsi-viewer/` 文件夹 - 包含所有依赖

## 分发方式

### macOS
```bash
# 压缩为zip文件
cd dist
zip -r "WSI Viewer.zip" "WSI Viewer.app"

# 或创建DMG文件（需要安装create-dmg）
brew install create-dmg
create-dmg --volname "WSI Viewer" "WSI Viewer.dmg" "dist/"
```

### Windows
- 将整个 `WSI Viewer` 文件夹压缩为zip文件
- 或使用 Inno Setup 创建安装程序

### Linux
```bash
# 压缩为tar.gz
cd dist
tar -czf wsi-viewer.tar.gz wsi-viewer/
```

## 常见问题

### 1. PyInstaller 未安装
```bash
pip install pyinstaller
```

### 2. 缺少依赖
```bash
pip install -r requirements.txt
```

### 3. 图标文件缺失
```bash
python create_windows_icon.py
```

### 4. OpenSlide 库问题
- macOS: `brew install openslide`
- Ubuntu: `sudo apt-get install libopenslide-dev`
- Windows: 从 OpenSlide 官网下载

### 5. 应用无法启动
- 检查是否有错误信息
- 尝试使用 `--console` 参数重新打包以显示控制台输出

## 优化建议

### 减小文件大小
```bash
# 使用UPX压缩（需要安装UPX）
pyinstaller --upx-dir=/path/to/upx --clean --windowed wsi_viewer.py
```

### 单文件打包
```bash
# 生成单个可执行文件（启动较慢）
pyinstaller --onefile --windowed wsi_viewer.py
```

### 调试模式
```bash
# 显示控制台输出以便调试
pyinstaller --console wsi_viewer.py
```

## 代码签名（macOS）

如果需要分发到 App Store 或避免安全警告：

```bash
# 获取开发者证书后签名
codesign --force --deep --sign "Developer ID Application: Your Name" "dist/WSI Viewer.app"

# 验证签名
codesign --verify --deep --strict "dist/WSI Viewer.app"
```

## 自动化构建

可以设置 CI/CD 流水线自动构建：

```yaml
# GitHub Actions 示例
name: Build WSI Viewer
on: [push, pull_request]
jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build
        run: python build_app.py --target ${{ matrix.os }}
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: wsi-viewer-${{ matrix.os }}
          path: dist/
``` 