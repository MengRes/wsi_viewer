#!/bin/bash

# Copy and rename icon files
cp resources/wsi_viewer_16.png resources/wsi_viewer.iconset/icon_16x16.png
cp resources/wsi_viewer_32.png resources/wsi_viewer.iconset/icon_16x16@2x.png
cp resources/wsi_viewer_32.png resources/wsi_viewer.iconset/icon_32x32.png
cp resources/wsi_viewer_64.png resources/wsi_viewer.iconset/icon_32x32@2x.png
cp resources/wsi_viewer_128.png resources/wsi_viewer.iconset/icon_128x128.png
cp resources/wsi_viewer_256.png resources/wsi_viewer.iconset/icon_128x128@2x.png
cp resources/wsi_viewer_256.png resources/wsi_viewer.iconset/icon_256x256.png
cp resources/wsi_viewer_512.png resources/wsi_viewer.iconset/icon_256x256@2x.png
cp resources/wsi_viewer_512.png resources/wsi_viewer.iconset/icon_512x512.png
cp resources/wsi_viewer_1024.png resources/wsi_viewer.iconset/icon_512x512@2x.png

# Create icns file
iconutil -c icns resources/wsi_viewer.iconset 