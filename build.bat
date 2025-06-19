@echo off
echo WSI Viewer Build Script
echo ======================

REM Check if we're in the right directory
if not exist "wsi_viewer.py" (
    echo Error: wsi_viewer.py not found. Please run this script from the project root.
    exit /b 1
)

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Create Windows icon
echo Creating Windows icon...
python create_windows_icon.py

REM Build for Windows
echo Building for Windows...
pyinstaller --clean --windowed ^
    --name="WSI Viewer" ^
    --icon=resources/wsi_viewer.ico ^
    --add-data="resources;resources" ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=openslide ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageQt ^
    wsi_viewer.py

echo Build completed! Check the 'dist' directory for the executable.
pause 