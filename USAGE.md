# WSI Viewer 使用指南

## 快速开始

### 1. 启动程序
- **macOS**: 双击 `WSI Viewer.app` 或从 Applications 文件夹启动
- **Windows**: 双击 `WSI Viewer.exe`
- **Linux**: 在终端运行 `./wsi-viewer`

### 2. 打开 WSI 文件
- 点击菜单栏 "File" → "Open"
- 或使用快捷键 `Ctrl+O` (Windows/Linux) / `Cmd+O` (macOS)
- 选择支持的 WSI 文件格式：SVS, TIFF, NDPI, VMS, VMR, SCN, MRXS, TIF, SVSLIDE, TMA

## 界面说明

### 左侧面板 - 元数据
- **文件信息**: 显示文件路径、大小、格式等基本信息
- **图像属性**: 显示图像尺寸、层级信息、分辨率等
- **属性列表**: 显示所有可用的元数据属性
- **操作**: 点击展开/折叠按钮查看详细信息

### 右侧主视图
- **图像显示**: 显示当前 WSI 图像
- **缩放控制**: 使用鼠标滚轮或工具栏按钮进行缩放
- **平移操作**: 按住鼠标左键拖拽移动视图
- **状态栏**: 显示当前缩放比例、图像信息等

### 右上角缩略图
- **全局视图**: 显示整个 WSI 图像的缩略图
- **当前位置**: 红色框显示当前查看区域
- **快速导航**: 点击缩略图快速跳转到指定位置

## 基本操作

### 图像浏览
1. **缩放**
   - 鼠标滚轮：向上滚动放大，向下滚动缩小
   - 工具栏按钮：点击 "+" 放大，"-" 缩小
   - 双击：快速缩放到适合窗口大小

2. **平移**
   - 鼠标拖拽：按住左键拖拽移动视图
   - 缩略图导航：点击缩略图跳转到指定位置

3. **重置视图**
   - 双击图像区域：重置到适合窗口大小
   - 工具栏重置按钮：回到初始视图

### 元数据查看
1. **展开/折叠**
   - 点击左侧面板的展开/折叠按钮
   - 查看详细的图像属性信息

2. **长文本处理**
   - 长文本会自动换行显示
   - 鼠标悬停显示完整内容

3. **搜索信息**
   - 使用浏览器的搜索功能 (Ctrl+F) 在元数据中搜索

## 保存功能

### 保存完整图像
1. 点击 "File" → "Save Image"
2. 选择保存格式：
   - **PNG**: 无损压缩，文件较大
   - **JPEG**: 有损压缩，文件较小
   - **BMP**: 无压缩，文件最大
   - **TIFF**: 高质量，支持多种压缩
3. 程序会自动选择最佳分辨率（约400万像素）
4. 支持取消保存操作

### 保存元数据
1. 点击 "File" → "Save Metadata"
2. 选择保存位置和文件名
3. 保存为格式化的文本文件
4. 包含所有图像属性信息

## 高级功能

### 性能优化
- **智能层级选择**: 程序自动选择最佳显示层级
- **内存管理**: 避免加载过大的图像数据
- **异步加载**: 大文件加载时不会阻塞界面

### 文件格式支持
- **SVS**: Aperio 格式，最常见的 WSI 格式
- **TIFF**: 标准图像格式，支持多层级
- **NDPI**: Hamamatsu 格式
- **VMS/VMR**: Ventana 格式
- **SCN**: Leica 格式
- **MRXS**: 3DHistech 格式
- **SVSLIDE**: 其他 SVS 变体
- **TMA**: 组织微阵列格式

### 快捷键
- `Ctrl+O` / `Cmd+O`: 打开文件
- `Ctrl+S` / `Cmd+S`: 保存图像
- `Ctrl+Q` / `Cmd+Q`: 退出程序
- `F11`: 全屏模式（如果支持）

## 故障排除

### 常见问题

1. **程序无法启动**
   - 检查系统要求（Python 3.7+, 4GB+ RAM）
   - 确保有足够的磁盘空间
   - 检查防火墙设置

2. **图像无法加载**
   - 确认文件格式支持
   - 检查文件是否完整
   - 尝试其他 WSI 文件

3. **内存不足**
   - 关闭其他程序释放内存
   - 使用较小的 WSI 文件
   - 增加系统虚拟内存

4. **保存失败**
   - 检查磁盘空间
   - 确认写入权限
   - 尝试不同的保存位置

5. **界面显示异常**
   - 检查显示分辨率设置
   - 更新图形驱动程序
   - 尝试不同的缩放设置

### 性能优化建议

1. **硬件要求**
   - 推荐 8GB+ RAM
   - SSD 存储提高加载速度
   - 独立显卡改善显示性能

2. **软件设置**
   - 关闭不必要的后台程序
   - 定期清理临时文件
   - 保持系统更新

3. **使用技巧**
   - 避免同时打开多个大型文件
   - 使用适当的缩放级别
   - 定期保存工作进度

## 技术支持

### 获取帮助
- 查看程序内置帮助信息
- 参考在线文档
- 提交 GitHub Issues

### 报告问题
请提供以下信息：
- 操作系统版本
- 程序版本
- 错误信息截图
- 复现步骤
- 系统配置信息

### 功能建议
欢迎提出新功能建议和改进意见，请通过 GitHub Issues 提交。 