def calculate_position(base_size, watermark_size, position):
    """Calculate watermark position coordinates."""
    base_w, base_h = base_size
    wm_w, wm_h = watermark_size
    
    # Adaptive margin based on image size (minimum 30px, maximum 80px)
    margin = min(80, max(30, min(base_w, base_h) // 15))
    
    positions = {
        'center': ((base_w - wm_w) // 2, (base_h - wm_h) // 2),
        'top-left': (margin, margin),
        'top-right': (base_w - wm_w - margin, margin),
        'bottom-left': (margin, base_h - wm_h - margin),
        'bottom-right': (base_w - wm_w - margin, base_h - wm_h - margin)
    }
    
    # Ensure positions are within bounds
    x, y = positions.get(position, positions['center'])
    x = max(0, min(x, base_w - wm_w))
    y = max(0, min(y, base_h - wm_h))
    
    return (x, y)

def calculate_optimal_font_size(image_size, base_size=48):
    """Calculate optimal font size based on image dimensions."""
    base_w, base_h = image_size
    # Scale font size based on image area, with reasonable bounds
    area_factor = (base_w * base_h) / (1920 * 1080)  # Normalized to 1080p
    optimal_size = int(base_size * (area_factor ** 0.3))  # Cube root scaling
    return max(24, min(144, optimal_size))  # Clamp between 24-144px

def calculate_optimal_image_scale(base_size, watermark_size, target_percentage=15):
    """Calculate optimal image watermark scale based on image sizes."""
    base_w, base_h = base_size
    wm_w, wm_h = watermark_size
    
    # Calculate scale to make watermark a target percentage of base image area
    base_area = base_w * base_h
    target_area = base_area * (target_percentage / 100)
    wm_area = wm_w * wm_h
    
    scale_factor = (target_area / wm_area) ** 0.5
    scale_percentage = int(scale_factor * 100)
    
    # Clamp to reasonable bounds
    return max(10, min(80, scale_percentage))

def normalize_opacity(opacity_percent):
    """Convert opacity percentage (0-100) to alpha value (0-255)."""
    return int(opacity_percent * 255 / 100)