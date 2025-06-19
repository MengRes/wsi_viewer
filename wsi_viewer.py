import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QTextEdit, QLabel, 
                             QScrollArea, QFrame, QFileDialog, QMenuBar, 
                             QAction, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                             QStackedLayout, QSlider, QPushButton, QProgressBar, QToolBar, QMessageBox, QTreeWidget, QTreeWidgetItem, QProgressDialog)
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QTimer, QThread, pyqtSignal, QPointF, QObject, QEvent
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage, QTransform, QIcon
import openslide
import numpy as np
from PIL import Image
import io
from collections import OrderedDict
import traceback
import math
import collections
import datetime

class LRUCache:
    """LRU Cache implementation for tile caching"""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def __getitem__(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        raise KeyError(key)
    
    def __setitem__(self, key, value):
        if key in self.cache:
            # Update existing key
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
    
    def __contains__(self, key):
        return key in self.cache
    
    def __len__(self):
        return len(self.cache)
    
    def clear(self):
        self.cache.clear()
        self.order.clear()
    
    def pop(self, key, default=None):
        if key in self.cache:
            self.order.remove(key)
            return self.cache.pop(key)
        return default
    
    def items(self):
        return self.cache.items()

class TileLoader(QObject):
    """Tile loading worker"""
    tile_loaded = pyqtSignal(QImage, name='tileLoaded')
    finished = pyqtSignal()
    
    def __init__(self, slide, level, region):
        """
        Initialize tile loader
        :param slide: OpenSlide object
        :param level: Image level
        :param region: Tuple (x, y, width, height) representing the region to load
        """
        super().__init__()
        self.slide = slide
        self.level = level
        self.region = region
        self._is_running = True
    
    def load_tile(self):
        """Load tile in background thread"""
        try:
            if not self._is_running:
                return
                
            # Read region
            region_data = self.slide.read_region(
                (self.region[0], self.region[1]),
                self.level,
                (self.region[2], self.region[3])
            )
            
            if not self._is_running:
                return
                
            # Convert to RGB mode
            region_data = region_data.convert('RGB')
            
            if not self._is_running:
                return
                
            # Convert to QImage
            region_image = QImage(
                region_data.tobytes('raw', 'RGB'),
                region_data.width,
                region_data.height,
                region_data.width * 3,
                QImage.Format_RGB888
            )
            
            if not self._is_running:
                return
                
            # Emit loaded signal
            self.tile_loaded.emit(region_image)
            
        except Exception as e:
            print(f"Error loading tile: {e}")
            if self._is_running:
                self.tile_loaded.emit(QImage())
            
        finally:
            if self._is_running:
                self.finished.emit()
    
    def stop(self):
        """Stop loading"""
        self._is_running = False

class TileManager:
    """Manages tile loading and caching"""
    
    def __init__(self, tile_size=512, cache_size=500, max_concurrent_loads=8):
        self.tile_size = tile_size
        self.cache = LRUCache(cache_size)
        self.max_concurrent_loads = max_concurrent_loads
        self.active_threads = []
        self.active_workers = []
    
    def get_tile_coordinates(self, level_size, view_rect):
        """Calculate tile coordinates for visible region"""
        tiles = []
        tile_size = self.tile_size
        
        # Calculate tile boundaries
        start_x = max(0, int(view_rect.x() // tile_size))
        start_y = max(0, int(view_rect.y() // tile_size))
        end_x = min(level_size[0] // tile_size, int((view_rect.x() + view_rect.width()) // tile_size) + 1)
        end_y = min(level_size[1] // tile_size, int((view_rect.y() + view_rect.height()) // tile_size) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tiles.append((x, y))
        
        return tiles
    
    def clear(self):
        """Clear all tiles and stop active threads"""
        for thread in self.active_threads:
            if thread.isRunning():
                thread.quit()
                thread.wait()
        self.active_threads.clear()
        self.active_workers.clear()
        self.cache.clear()
    
    def add_tile_to_queue(self, x, y, level):
        """Add tile to loading queue"""
        tile_key = (x, y, level)
        if tile_key not in self.cache:
            # Add to loading queue
            pass
    
    def clean_invisible_tiles(self, visible_rect):
        """Remove tiles that are no longer visible"""
        # Implementation for cleaning invisible tiles
        pass

class WSIImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'wsi_viewer.icns')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            # For macOS dock icon
            if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
                QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        else:
            # Fallback to PNG if ICNS is not available
            png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'wsi_viewer.png')
            if os.path.exists(png_path):
                self.setWindowIcon(QIcon(png_path))
        
        # Initialize variables
        self.slide = None
        self.current_file_path = None
        self.current_level = None  # Will be set when loading image
        self.zoom_factor = 1.0
        self._is_closing = False
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.hide()
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('WSI Viewer')
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu()
        
        # Create status bar
        self.statusBar().showMessage('Ready - Please open WSI file')
        self.statusBar().addWidget(self.progress_bar)
        
        # Create main window widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create horizontal splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Metadata
        self.metadata_panel = self.create_metadata_panel()
        splitter.addWidget(self.metadata_panel)
        
        # Right panel - WSI display
        self.wsi_panel = self.create_wsi_panel()
        splitter.addWidget(self.wsi_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 1100])
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.addWidget(splitter)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        open_action = QAction('&Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_wsi_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('&Save L3 Image...', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_thumbnail)
        file_menu.addAction(save_action)
        
        save_meta_action = QAction('Save &Metadata...', self)
        save_meta_action.setShortcut('Ctrl+M')
        save_meta_action.triggered.connect(self.save_metadata)
        file_menu.addAction(save_meta_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
    def create_metadata_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        panel.setMaximumWidth(350)
        
        layout = QVBoxLayout(panel)
        
        # Title
        title_label = QLabel('WSI Metadata')
        title_label.setStyleSheet('font-size: 14px; font-weight: bold; margin: 5px;')
        layout.addWidget(title_label)
        
        # Create tree widget for metadata
        self.metadata_tree = QTreeWidget()
        self.metadata_tree.setHeaderHidden(True)  # Hide the header
        self.metadata_tree.setAlternatingRowColors(True)  # 交替行颜色
        self.metadata_tree.setWordWrap(True)  # 启用自动换行
        self.metadata_tree.setTextElideMode(Qt.ElideMiddle)  # 在中间使用省略号
        
        # 设置工具提示的显示时间（10秒）
        self.metadata_tree.setToolTipDuration(10000)
        
        self.metadata_tree.setStyleSheet("""
            QTreeWidget {
                font-family: monospace;
                font-size: 10px;
                border: 1px solid #ccc;
                background-color: white;
            }
            QTreeWidget::item {
                padding: 2px;
                min-height: 20px;  /* 设置最小高度以适应换行 */
            }
            QTreeWidget::item:hover {
                background-color: #e6f3ff;
            }
            QTreeWidget::item:selected {
                background-color: #cce8ff;
            }
            QToolTip {
                font-family: monospace;
                font-size: 10px;
                padding: 5px;
                border: 1px solid #ccc;
                background-color: #ffffd0;
                color: black;
            }
        """)
        layout.addWidget(self.metadata_tree)
        
        return panel

    def add_tree_item(self, parent, text, full_text=None):
        """Helper function to add items to the tree with tooltips"""
        item = QTreeWidgetItem(parent, [text])
        if full_text:
            item.setToolTip(0, full_text)
        return item

    def display_metadata(self):
        if not self.slide:
            return
            
        # Clear existing items
        self.metadata_tree.clear()
        
        # Get basic information
        dimensions = self.slide.dimensions
        level_count = self.slide.level_count
        level_dimensions = self.slide.level_dimensions
        level_downsamples = self.slide.level_downsamples
        
        # Get pixel size information
        mpp_x = self.slide.properties.get('openslide.mpp-x', 'Unknown')
        mpp_y = self.slide.properties.get('openslide.mpp-y', 'Unknown')
        
        # File information
        file_item = QTreeWidgetItem(["File Information"])
        file_item.setExpanded(True)
        self.metadata_tree.addTopLevelItem(file_item)
        
        # 为长路径添加工具提示
        path_item = self.add_tree_item(file_item, 
            f"Path: {os.path.basename(self.current_file_path)}", 
            f"Full path:\n{self.current_file_path}")
        
        # Basic information
        basic_item = QTreeWidgetItem(["Basic Information"])
        basic_item.setExpanded(True)
        self.metadata_tree.addTopLevelItem(basic_item)
        
        # 添加基本信息项，为长文本添加工具提示
        size_text = f"Size: {dimensions[0]} x {dimensions[1]}"
        self.add_tree_item(basic_item, size_text, 
            f"Width: {dimensions[0]} pixels\nHeight: {dimensions[1]} pixels")
        
        self.add_tree_item(basic_item, f"Level Count: {level_count}")
        
        pixel_size_text = f"Pixel Size: {mpp_x} × {mpp_y} µm/pixel"
        self.add_tree_item(basic_item, pixel_size_text,
            f"X Resolution: {mpp_x} µm/pixel\nY Resolution: {mpp_y} µm/pixel")
        
        # Level information
        levels_item = QTreeWidgetItem(["Level Information"])
        levels_item.setExpanded(False)
        self.metadata_tree.addTopLevelItem(levels_item)
        
        for level in range(level_count):
            level_item = QTreeWidgetItem(levels_item, [f"Level {level}"])
            
            # 为每个层级的信息添加详细的工具提示
            size_text = f"Size: {level_dimensions[level][0]} x {level_dimensions[level][1]}"
            self.add_tree_item(level_item, size_text,
                f"Width: {level_dimensions[level][0]} pixels\nHeight: {level_dimensions[level][1]} pixels")
            
            downsample_text = f"Downsample: {level_downsamples[level]:.2f}x"
            self.add_tree_item(level_item, downsample_text,
                f"Each pixel represents {level_downsamples[level]:.2f} pixels in the original image")
            
            if mpp_x != 'Unknown' and mpp_y != 'Unknown':
                actual_mpp_x = float(mpp_x) * level_downsamples[level]
                actual_mpp_y = float(mpp_y) * level_downsamples[level]
                resolution_text = f"Resolution: {actual_mpp_x:.2f} × {actual_mpp_y:.2f} µm/pixel"
                self.add_tree_item(level_item, resolution_text,
                    f"X Resolution: {actual_mpp_x:.2f} µm/pixel\nY Resolution: {actual_mpp_y:.2f} µm/pixel")
        
        # Properties
        props_item = QTreeWidgetItem(["Properties"])
        props_item.setExpanded(False)
        self.metadata_tree.addTopLevelItem(props_item)
        
        # Group properties by vendor
        vendor_props = {}
        for key, value in self.slide.properties.items():
            vendor = key.split('.')[0] if '.' in key else 'Other'
            if vendor not in vendor_props:
                vendor_props[vendor] = []
            vendor_props[vendor].append((key, value))
        
        # Add properties by vendor
        for vendor, props in vendor_props.items():
            vendor_item = QTreeWidgetItem(props_item, [vendor])
            for key, value in props:
                # 为属性值添加工具提示，显示完整的键值对
                prop_text = f"{key.split('.')[-1]}: {value}"
                self.add_tree_item(vendor_item, prop_text, f"{key}:\n{value}")
        
        # Associated images
        if self.slide.associated_images:
            assoc_item = QTreeWidgetItem(["Associated Images"])
            assoc_item.setExpanded(False)
            self.metadata_tree.addTopLevelItem(assoc_item)
            for name, img in self.slide.associated_images.items():
                image_text = f"{name}: {img.size[0]} x {img.size[1]}"
                self.add_tree_item(assoc_item, image_text,
                    f"Name: {name}\nWidth: {img.size[0]} pixels\nHeight: {img.size[1]} pixels")

    def create_wsi_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        
        # Use QVBoxLayout to layout main view and zoom controls
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a container widget to contain main view and thumbnail
        container = QWidget()
        container.setLayout(QStackedLayout())
        layout.addWidget(container)
        
        # WSI display area
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Set view properties
        self.graphics_view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graphics_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphics_view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.graphics_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        # Connect viewport change signals
        self.graphics_view.viewport().installEventFilter(self)

        # Create thumbnail
        self.thumbnail_widget = QWidget(container)
        self.thumbnail_widget.setFixedSize(200, 150)
        thumbnail_layout = QVBoxLayout(self.thumbnail_widget)
        thumbnail_layout.setContentsMargins(5, 5, 5, 5)
        
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(190, 140)
        self.thumbnail_label.setStyleSheet('border: 1px solid gray; background-color: white;')
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        thumbnail_layout.addWidget(self.thumbnail_label)
        
        # Add main view and thumbnail to container
        container.layout().addWidget(self.graphics_view)
        
        # Set thumbnail position to top right corner
        self.thumbnail_widget.raise_()  # Ensure thumbnail is on top
        
        # Create zoom control bar
        zoom_widget = QWidget()
        zoom_layout = QHBoxLayout(zoom_widget)
        zoom_layout.setContentsMargins(5, 0, 5, 5)
        
        # Zoom buttons and display
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.setFixedSize(30, 30)
        zoom_out_btn.setToolTip("Zoom Out")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_out_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        zoom_layout.addWidget(zoom_out_btn)

        # Zoom value display
        self.zoom_value_label = QLabel("100.0%")
        self.zoom_value_label.setMinimumWidth(90)
        self.zoom_value_label.setAlignment(Qt.AlignCenter)
        self.zoom_value_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        zoom_layout.addWidget(self.zoom_value_label)
        
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setFixedSize(30, 30)
        zoom_in_btn.setToolTip("Zoom In")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_in_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        zoom_layout.addWidget(zoom_in_btn)
        
        # Add reset zoom button
        reset_zoom_btn = QPushButton()
        reset_zoom_btn.setFixedSize(30, 30)
        reset_zoom_btn.setToolTip("Fit Window")
        reset_zoom_btn.clicked.connect(self.reset_zoom)
        
        # Create icon for fit window (using text as icon)
        reset_zoom_btn.setText("⤢")
        reset_zoom_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        zoom_layout.addWidget(reset_zoom_btn)
        
        # Add elastic space
        zoom_layout.addStretch()
        
        # Add zoom control bar to main layout
        layout.addWidget(zoom_widget)
        
        return panel

    def open_wsi_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select WSI File', 
            '', 
            'WSI Files (*.svs *.tif *.tiff *.ndpi *.vms *.vmu *.scn *.mrxs *.svslide);;All Files (*)'
        )
        
        if file_path:
            try:
                self.load_wsi_file(file_path)
            except Exception as e:
                self.metadata_tree.clear()
                self.metadata_tree.addTopLevelItem(QTreeWidgetItem(["Error"]))
                self.metadata_tree.topLevelItem(0).setText(0, str(e))
                
    def load_wsi_file(self, file_path):
        try:
            if self._is_closing:
                return
                
            self.statusBar().showMessage('Loading WSI file...')
            
            # Close previous slide
            if self.slide:
                self.slide.close()
            
            # Save file path
            self.current_file_path = file_path
                
            # Open new slide
            self.slide = openslide.OpenSlide(file_path)
            
            # Choose initial level based on image size
            dimensions = self.slide.dimensions
            target_size = 1024 * 1024  # Target: ~1 million pixels
            actual_size = dimensions[0] * dimensions[1]
            
            # Calculate ideal level
            ideal_downsample = (actual_size / target_size) ** 0.5
            
            # Find the closest level
            downsamples = self.slide.level_downsamples
            closest_level = min(range(len(downsamples)), 
                              key=lambda i: abs(downsamples[i] - ideal_downsample))
            
            # Set current level
            self.current_level = closest_level
            
            # Display metadata
            self.display_metadata()
            
            # Display WSI image
            self.display_wsi_image()
            
            # Update thumbnail
            self.update_thumbnail()
            
            # Update status bar
            filename = os.path.basename(file_path)
            level_size = self.slide.level_dimensions[self.current_level]
            self.statusBar().showMessage(
                f'Loaded: {filename} - Original Size: {dimensions[0]}x{dimensions[1]} - '
                f'Display Level: {self.current_level} ({level_size[0]}x{level_size[1]})'
            )
            
        except Exception as e:
            self.statusBar().showMessage(f'Error: {str(e)}')
            self.metadata_tree.clear()
            self.metadata_tree.addTopLevelItem(QTreeWidgetItem(["Error"]))
            self.metadata_tree.topLevelItem(0).setText(0, str(e))
            raise

    def display_wsi_image(self):
        """Display WSI image"""
        if not self.slide or self._is_closing:
            return
            
        try:
            # Clear previous scene
            self.graphics_scene.clear()
            
            # Get current level dimensions
            level_width, level_height = self.slide.level_dimensions[self.current_level]
            
            # Load full image directly
            self.load_full_image()
            
        except Exception as e:
            print(f"Error displaying WSI image: {e}")
            self.statusBar().showMessage(f'Error displaying image: {str(e)}')

    def load_full_image(self):
        """Load full image"""
        if not self.slide or self._is_closing:
            return
            
        try:
            # Get current level dimensions
            level_width, level_height = self.slide.level_dimensions[self.current_level]
            
            # Show progress bar
            self.progress_bar.setValue(0)
            self.progress_bar.show()
            
            # Read entire image
            image_data = self.slide.read_region(
                (0, 0),
                self.current_level,
                (level_width, level_height)
            )
            
            # Convert to RGB mode
            image_data = image_data.convert('RGB')
            
            # Convert to QImage
            qimage = QImage(
                image_data.tobytes('raw', 'RGB'),
                image_data.width,
                image_data.height,
                image_data.width * 3,
                QImage.Format_RGB888
            )
            
            # Create graphics item and add to scene
            pixmap = QPixmap.fromImage(qimage)
            item = QGraphicsPixmapItem(pixmap)
            self.graphics_scene.addItem(item)
            
            # Set scene rectangle
            self.graphics_scene.setSceneRect(item.boundingRect())
            
            # Adjust view to show full image (fill main view)
            self.graphics_view.fitInView(item, Qt.KeepAspectRatio)
            
            # Get actual zoom factor
            transform = self.graphics_view.transform()
            self.zoom_factor = transform.m11()
            
            # Update zoom display
            self.update_zoom_display()
            
            # Update status bar
            self.update_status_info()
            
            # Hide progress bar
            self.progress_bar.hide()
            
        except Exception as e:
            print(f"Error loading full image: {e}")
            self.progress_bar.hide()
            self.statusBar().showMessage(f'Error loading image: {str(e)}')

    def update_visible_region(self):
        """Update visible region - simplified version, no longer using tile loading"""
        if not self.slide or self._is_closing:
            return
        
        # Simplified version: only update thumbnail and status info
        try:
            self.update_thumbnail_box()
            self.update_status_info()
        except Exception as e:
            print(f"Error updating visible region: {e}")

    def on_region_loaded(self, image, pos_x, pos_y):
        """Handle loaded region - simplified version"""
        # This method is no longer used, but kept to avoid errors
        pass

    def update_thumbnail(self):
        if not self.slide or self._is_closing:
            return
            
        try:
            # Use highest level for thumbnail
            level = self.slide.level_count - 1
            thumb_size = self.slide.level_dimensions[level]
            
            # Calculate scale to ensure thumbnail fits display area
            max_size = 190  # Slightly smaller than thumbnail container to leave border space
            scale = min(max_size / thumb_size[0], max_size / thumb_size[1])
            target_size = (int(thumb_size[0] * scale), int(thumb_size[1] * scale))
            
            # Limit thumbnail size
            if target_size[0] * target_size[1] > 1000000:  # Limit to 1 million pixels
                scale = (1000000 / (thumb_size[0] * thumb_size[1])) ** 0.5
                target_size = (int(thumb_size[0] * scale), int(thumb_size[1] * scale))
            
            # Read image
            img = self.slide.read_region((0, 0), level, self.slide.level_dimensions[level])
            img = img.convert('RGB')  # Convert to RGB mode
            
            # Scale image
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Convert to QPixmap
            img_data = img.tobytes('raw', 'RGB')
            qimg = QImage(img_data, img.width, img.height, img.width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Save original thumbnail
            self.thumbnail_pixmap = pixmap.copy()
            
            # Set thumbnail
            self.thumbnail_label.setPixmap(pixmap)
            
            # Initial update of thumbnail box
            self.update_thumbnail_box()
            
        except Exception as e:
            print(f"Error updating thumbnail: {str(e)}")
            self.statusBar().showMessage(f"Error updating thumbnail: {str(e)}")

    def update_thumbnail_box(self):
        if not self.slide or not hasattr(self, 'thumbnail_pixmap') or self._is_closing:
            return
            
        try:
            # Create thumbnail with box
            pixmap = self.thumbnail_pixmap.copy()
            painter = QPainter(pixmap)
            
            # Set red border, 2 pixel width
            pen = QPen(QColor(255, 0, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            
            # Get thumbnail and original image dimensions
            thumb_width = pixmap.width()
            thumb_height = pixmap.height()
            original_width, original_height = self.slide.dimensions
            
            # Get current view region position in scene coordinates
            view_rect = self.graphics_view.mapToScene(self.graphics_view.viewport().rect()).boundingRect()
            
            # Get current level downsample ratio
            level_scale = self.slide.level_downsamples[self.current_level]
            
            # Calculate current view position in level 0
            view_x = view_rect.x() * level_scale
            view_y = view_rect.y() * level_scale
            view_width = view_rect.width() * level_scale
            view_height = view_rect.height() * level_scale
            
            # Calculate thumbnail scale ratio (relative to original image)
            thumb_scale_x = thumb_width / original_width
            thumb_scale_y = thumb_height / original_height
            
            # Calculate box position and size in thumbnail
            box_x = view_x * thumb_scale_x
            box_y = view_y * thumb_scale_y
            box_width = view_width * thumb_scale_x
            box_height = view_height * thumb_scale_y
            
            # Ensure box is within thumbnail bounds
            box_x = max(0, min(box_x, thumb_width))
            box_y = max(0, min(box_y, thumb_height))
            box_width = min(box_width, thumb_width - box_x)
            box_height = min(box_height, thumb_height - box_y)
            
            # If box is too small, set minimum size
            min_size = 5
            if 0 < box_width < min_size:
                box_width = min_size
            if 0 < box_height < min_size:
                box_height = min_size
            
            # Draw box
            if box_width > 0 and box_height > 0:
                # Use semi-transparent red fill
                painter.setBrush(QColor(255, 0, 0, 50))
                painter.drawRect(int(box_x), int(box_y), int(box_width), int(box_height))
                
                # Draw border
                painter.setBrush(Qt.NoBrush)
                painter.drawRect(int(box_x), int(box_y), int(box_width), int(box_height))
            
            painter.end()
            
            # Update thumbnail
            self.thumbnail_label.setPixmap(pixmap)
            
        except Exception as e:
            print(f"Error updating thumbnail box: {str(e)}")
            traceback.print_exc()

    def update_zoom_display(self):
        """Update zoom display"""
        if not self.slide or self._is_closing:
            return
            
        # Get current level downsample ratio
        level_scale = self.slide.level_downsamples[self.current_level]
        
        # Calculate actual zoom ratio (considering level downsample)
        effective_zoom = self.zoom_factor / level_scale
        
        # Convert to percentage display
        zoom_percentage = effective_zoom * 100
        
        # Update zoom display
        self.zoom_value_label.setText(f'{zoom_percentage:.1f}%')

    def update_status_info(self):
        if not self.slide or self._is_closing:
            return
            
        # Get current zoom level
        transform = self.graphics_view.transform()
        zoom_level = transform.m11()  # Horizontal zoom factor
        
        # Get current level downsample ratio
        level_scale = self.slide.level_downsamples[self.current_level]
        
        # Calculate actual zoom ratio (considering level downsample)
        effective_zoom = zoom_level / level_scale
        
        # Convert to percentage
        zoom_percentage = effective_zoom * 100
        
        # Get current view region
        view_rect = self.graphics_view.mapToScene(self.graphics_view.viewport().rect()).boundingRect()
        
        # Calculate actual position and size in level 0
        x_level_0 = int(view_rect.x() * level_scale)
        y_level_0 = int(view_rect.y() * level_scale)
        width_level_0 = int(view_rect.width() * level_scale)
        height_level_0 = int(view_rect.height() * level_scale)
        
        # Update status bar
        status_text = (f'Level: {self.current_level} | '
                      f'Downsample: {level_scale:.2f}x | '
                      f'Zoom: {zoom_percentage:.1f}% | '
                      f'Position: ({x_level_0}, {y_level_0}) | '
                      f'View Size: {width_level_0}x{height_level_0}')
        self.statusBar().showMessage(status_text)

    def eventFilter(self, obj, event):
        """Event filter, handle viewport changes"""
        if obj == self.graphics_view.viewport() and not self._is_closing:
            if event.type() in [QEvent.Resize, QEvent.MouseMove, QEvent.Wheel]:
                # Update thumbnail box and status info
                self.update_thumbnail_box()
                self.update_status_info()
        return super().eventFilter(obj, event)

    def zoom_in(self):
        """Zoom in"""
        if self._is_closing:
            return
        # Zoom in by 20%
        self.set_zoom(self.zoom_factor * 1.2)

    def zoom_out(self):
        """Zoom out"""
        if self._is_closing:
            return
        # Zoom out to 83.33% of original (i.e., reduce by 16.67%)
        self.set_zoom(self.zoom_factor / 1.2)

    def set_zoom(self, factor):
        if not self.slide or self._is_closing:
            return
            
        # Limit zoom range (1% to 1000%)
        factor = max(0.01, min(10.0, factor))
        
        # Save current view center
        center = self.graphics_view.mapToScene(self.graphics_view.viewport().rect().center())
        
        # Apply zoom
        transform = QTransform()
        transform.scale(factor, factor)
        self.graphics_view.setTransform(transform)
        
        # Update zoom factor
        self.zoom_factor = factor
        
        # Update zoom display
        self.update_zoom_display()
        
        # Update status bar and thumbnail
        self.update_status_info()
        self.update_thumbnail_box()
        
        # Force view update
        self.graphics_view.viewport().update()

    def reset_zoom(self):
        """Reset to initial zoom level"""
        if not self.slide or self._is_closing or not self.graphics_scene:
            return
            
        try:
            # Get image item from scene
            items = self.graphics_scene.items()
            if not items:
                return
                
            # Find image item
            image_item = None
            for item in items:
                if isinstance(item, QGraphicsPixmapItem):
                    image_item = item
                    break
                    
            if not image_item:
                return
                
            # Re-fit to window size (return to initial state)
            self.graphics_view.fitInView(image_item, Qt.KeepAspectRatio)
            
            # Get actual zoom factor
            transform = self.graphics_view.transform()
            self.zoom_factor = transform.m11()
            
            # Update zoom display
            self.update_zoom_display()
            
            # Update status bar and thumbnail
            self.update_status_info()
            self.update_thumbnail_box()
            
            # Force view update
            self.graphics_view.viewport().update()
            
        except Exception as e:
            print(f"Error resetting zoom: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # When window size changes, adjust view and thumbnail position
        if hasattr(self, 'graphics_view') and hasattr(self, 'thumbnail_widget') and not self._is_closing:
            # Update thumbnail position to top right corner
            view_rect = self.graphics_view.rect()
            self.thumbnail_widget.setGeometry(
                view_rect.width() - 210,  # 10 pixel margin from right edge
                10,                       # 10 pixel margin from top
                200,                      # Thumbnail width
                150                       # Thumbnail height
            )
            
            # If scene is created, ensure image is fully displayed
            if self.graphics_scene and self.graphics_scene.sceneRect().width() > 0:
                # Re-fit to new window size
                self.graphics_view.fitInView(self.graphics_scene.sceneRect(), Qt.KeepAspectRatio)
                # Get actual zoom factor
                transform = self.graphics_view.transform()
                self.zoom_factor = transform.m11()
                self.update_zoom_display()
                self.update_thumbnail_box()
                self.update_status_info()

    def closeEvent(self, event):
        """Close event handler"""
        try:
            self._is_closing = True
            
            # Close image
            if self.slide:
                self.slide.close()
                self.slide = None
            
            # Accept close event
            event.accept()
            
        except Exception as e:
            print(f"Error in closeEvent: {e}")
            event.accept()

    def save_thumbnail(self):
        """Save WSI image at appropriate resolution"""
        if not self.slide or self._is_closing:
            QMessageBox.warning(self, "Warning", "No image loaded")
            return
            
        try:
            # Calculate target level based on full image size
            dimensions = self.slide.dimensions
            target_size = 2048 * 2048  # Target max size ~4 million pixels
            actual_size = dimensions[0] * dimensions[1]
            
            # Calculate ideal downsample
            ideal_downsample = (actual_size / target_size) ** 0.5 if actual_size > target_size else 1.0
            
            # Find best available level
            downsamples = self.slide.level_downsamples
            target_level = min(range(len(downsamples)), 
                             key=lambda i: abs(downsamples[i] - ideal_downsample))
            
            # Get target dimensions
            target_width, target_height = self.slide.level_dimensions[target_level]
            
            # Show progress dialog
            progress = QProgressDialog("Saving image...", "Cancel", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            progress.setValue(0)
            
            try:
                # Read the entire image at target level
                region = self.slide.read_region(
                    (0, 0),  # Start from top-left
                    target_level,
                    (target_width, target_height)
                )
                progress.setValue(50)
                
                if progress.wasCanceled():
                    return
                
                # Convert to RGB
                region = region.convert('RGB')
                progress.setValue(70)
                
                if progress.wasCanceled():
                    return
                
                # Convert PIL image to QImage
                img_data = region.tobytes('raw', 'RGB')
                img = QImage(
                    img_data,
                    region.width,
                    region.height,
                    region.width * 3,
                    QImage.Format_RGB888
                )
                progress.setValue(80)
                
                if progress.wasCanceled():
                    return
                
                # Add metadata to image
                img.setText("Level", str(target_level))
                img.setText("Downsample", f"{self.slide.level_downsamples[target_level]:.2f}x")
                img.setText("Original Size", f"{dimensions[0]}x{dimensions[1]}")
                img.setText("Original File", self.current_file_path)
                img.setText("Image Size", f"{target_width}x{target_height}")
                
                # Get suggested filename
                base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
                suggested_name = f"{base_name}_full_L{target_level}_{target_width}x{target_height}"
                
                # Show save dialog with multiple format options
                file_path, selected_filter = QFileDialog.getSaveFileName(
                    self,
                    'Save Full Image', 
                    suggested_name,
                    'PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp);;TIFF Files (*.tiff);;All Files (*)'
                )
                
                if file_path:
                    # Determine format based on selected filter
                    if 'PNG' in selected_filter:
                        format = 'PNG'
                    elif 'JPEG' in selected_filter:
                        format = 'JPEG'
                    elif 'BMP' in selected_filter:
                        format = 'BMP'
                    elif 'TIFF' in selected_filter:
                        format = 'TIFF'
                    else:
                        format = 'PNG'  # Default to PNG
                    
                    progress.setValue(90)
                    
                    if progress.wasCanceled():
                        return
                    
                    # Save image
                    success = img.save(file_path, format)
                    progress.setValue(100)
                    
                    if success:
                        self.statusBar().showMessage(
                            f'Saved full image: {os.path.basename(file_path)} '
                            f'(Level {target_level}, {target_width}x{target_height})'
                        )
                    else:
                        QMessageBox.critical(self, "Error", "Failed to save image")
            
            finally:
                progress.close()
            
        except Exception as e:
            print(f"Error saving image: {e}")
            QMessageBox.critical(self, "Error", "Failed to save image")

    def generate_metadata_text(self):
        """Generate formatted metadata text"""
        if not self.slide:
            return "No image loaded"
            
        # Get basic information
        dimensions = self.slide.dimensions
        level_count = self.slide.level_count
        level_dimensions = self.slide.level_dimensions
        level_downsamples = self.slide.level_downsamples
        
        # Get pixel size information
        mpp_x = self.slide.properties.get('openslide.mpp-x', 'Unknown')
        mpp_y = self.slide.properties.get('openslide.mpp-y', 'Unknown')
        
        # Format text
        metadata_text = f"""WSI File Metadata
================

File Information
---------------
Path: {self.current_file_path}

Basic Information
---------------
Size: {dimensions[0]} x {dimensions[1]} pixels
Level Count: {level_count}
Pixel Size: {mpp_x} µm/pixel (X) × {mpp_y} µm/pixel (Y)

Level Information
---------------"""

        for level in range(level_count):
            metadata_text += f"""
Level {level}:
    Size: {level_dimensions[level][0]} x {level_dimensions[level][1]} pixels
    Downsample: {level_downsamples[level]:.2f}x"""
            if mpp_x != 'Unknown' and mpp_y != 'Unknown':
                actual_mpp_x = float(mpp_x) * level_downsamples[level]
                actual_mpp_y = float(mpp_y) * level_downsamples[level]
                metadata_text += f"""
    Resolution: {actual_mpp_x:.2f} × {actual_mpp_y:.2f} µm/pixel"""

        metadata_text += "\n\nProperties\n----------\n"
        
        # Group properties by vendor
        vendor_props = {}
        for key, value in self.slide.properties.items():
            vendor = key.split('.')[0] if '.' in key else 'Other'
            if vendor not in vendor_props:
                vendor_props[vendor] = []
            vendor_props[vendor].append((key, value))
        
        # Add properties by vendor
        for vendor, props in sorted(vendor_props.items()):
            metadata_text += f"\n{vendor}:\n"
            for key, value in sorted(props):
                metadata_text += f"    {key}: {value}\n"
        
        # Add associated images
        if self.slide.associated_images:
            metadata_text += "\nAssociated Images\n----------------\n"
            for name, img in self.slide.associated_images.items():
                metadata_text += f"{name}: {img.size[0]} x {img.size[1]} pixels\n"
        
        # Add export information
        metadata_text += f"\nExport Information\n-----------------\n"
        metadata_text += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return metadata_text

    def save_metadata(self):
        """Save metadata to text file"""
        if not self.slide:
            QMessageBox.warning(self, "Warning", "No image loaded")
            return
            
        try:
            # Generate metadata text
            metadata_text = self.generate_metadata_text()
            
            # Get suggested filename
            base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
            suggested_name = f"{base_name}_metadata.txt"
            
            # Show save dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Save Metadata',
                suggested_name,
                'Text Files (*.txt);;All Files (*)'
            )
            
            if file_path:
                # Save metadata to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(metadata_text)
                
                self.statusBar().showMessage(f'Metadata saved: {os.path.basename(file_path)}')
                
        except Exception as e:
            print(f"Error saving metadata: {e}")
            QMessageBox.critical(self, "Error", "Failed to save metadata")

def main():
    """Main function"""
    import sys
    
    app = QApplication(sys.argv)
    app.setApplicationName("WSI Viewer")
    
    # Set application icon for macOS dock
    if sys.platform == 'darwin':
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'wsi_viewer.icns')
        if os.path.exists(icon_path):
            import PyQt5.QtGui
            app.setWindowIcon(QIcon(icon_path))
    
    viewer = WSIImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
