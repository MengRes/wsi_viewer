from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=(512, 512)):
    # Create a new image with a white background
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate dimensions
    width, height = size
    padding = width * 0.1
    box_size = width - (2 * padding)
    
    # Draw main rectangle (slide)
    slide_color = (65, 105, 225, 255)  # Royal Blue
    draw.rectangle(
        [(padding, padding), (width - padding, height - padding)],
        fill=slide_color,
        outline=(255, 255, 255, 255),
        width=int(width * 0.02)
    )
    
    # Draw grid lines to represent tiles
    grid_lines = 3
    grid_color = (255, 255, 255, 128)
    line_width = int(width * 0.01)
    
    # Vertical lines
    for i in range(1, grid_lines):
        x = padding + (box_size * i / grid_lines)
        draw.line(
            [(x, padding), (x, height - padding)],
            fill=grid_color,
            width=line_width
        )
    
    # Horizontal lines
    for i in range(1, grid_lines):
        y = padding + (box_size * i / grid_lines)
        draw.line(
            [(padding, y), (width - padding, y)],
            fill=grid_color,
            width=line_width
        )
    
    # Draw magnifying glass
    glass_center = (width * 0.65, height * 0.35)
    glass_radius = width * 0.15
    glass_handle_length = width * 0.2
    glass_handle_width = int(width * 0.03)
    
    # Draw glass circle
    draw.ellipse(
        [(glass_center[0] - glass_radius, glass_center[1] - glass_radius),
         (glass_center[0] + glass_radius, glass_center[1] + glass_radius)],
        outline=(255, 255, 255, 255),
        width=glass_handle_width
    )
    
    # Draw handle
    from math import cos, sin, pi
    angle = pi * 0.25  # 45 degrees
    end_x = glass_center[0] + cos(angle) * (glass_radius + glass_handle_length)
    end_y = glass_center[1] + sin(angle) * (glass_radius + glass_handle_length)
    
    draw.line(
        [(glass_center[0] + cos(angle) * glass_radius,
          glass_center[1] + sin(angle) * glass_radius),
         (end_x, end_y)],
        fill=(255, 255, 255, 255),
        width=glass_handle_width
    )
    
    return image

def save_icon_files():
    # Create resources directory if it doesn't exist
    if not os.path.exists('resources'):
        os.makedirs('resources')
    
    # Create main icon
    icon = create_icon((512, 512))
    icon.save('resources/wsi_viewer.png', 'PNG')
    
    # Create different sizes for macOS
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        resized = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'resources/wsi_viewer_{size}.png', 'PNG')

if __name__ == '__main__':
    save_icon_files() 