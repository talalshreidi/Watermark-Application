import tkinter as tk
from PIL import Image, ImageTk

class PreviewCanvas(tk.Canvas):
    def __init__(self, master=None, max_width=600, max_height=290, **kwargs):
        super().__init__(master, **kwargs)
        self.image = None # Original PIL Image
        self.display_image = None # Resized image for display
        self.photo_image = None # Tkinter PhotoImage
        self.max_width = max_width
        self.max_height = max_height

    def show_image(self, img):
        """Display an image on the canvas.
            Accepts a file path or a Pil.Image.Image object.
        """

        self.clear()

        if isinstance(img, str):
            self.image = Image.open(img)
        elif isinstance(img, Image.Image):
            self.image = img
        else:
            raise TypeError("Invalid image type. Please provide a file path or a PIL.Image.Image object.")

        # Creates the resized version
        self.display_image = self.resize_for_preview(self.image)

        # Create a PhotoImage for displaying in Tkinter
        self.photo_image = ImageTk.PhotoImage(self.display_image)

        # Center the image in the canvas
        canvas_width = self.winfo_width() if self.winfo_width() > 1 else 400
        canvas_height = self.winfo_height() if self.winfo_height() > 1 else 280
        
        x_center = (canvas_width - self.display_image.width) // 2
        y_center = (canvas_height - self.display_image.height) // 2
        
        # Ensure minimum positioning
        x_center = max(0, x_center)
        y_center = max(0, y_center)
        
        self.create_image(x_center, y_center, anchor=tk.NW, image=self.photo_image)



    def resize_for_preview(self, img):
        """Resize image to fit canvas dimensions while maintaining aspect ratio."""
        canvas_width = self.winfo_width() if self.winfo_width() > 1 else 400
        canvas_height = self.winfo_height() if self.winfo_height() > 1 else 290  # Fix this line
        

        height_scale = canvas_height / img.height
        new_width = int(img.width * height_scale)
        new_height = canvas_height
    

        if new_width > canvas_width:
            width_scale = canvas_width / img.width
            new_width = canvas_width
            new_height = int(img.height * width_scale)
        
        return img.resize((new_width, new_height), Image.LANCZOS)
    
    def clear(self):
        """Clear the canvas and reset images."""

        self.delete("all")
        self.display_image = None
        self.image = None
        self.photo_image = None

    def apply_text_watermark(self, text, font_size=48, color="#FFFFFF", position="bottom-right", opacity=85):
        """Apply text watermark to the current image with enhanced visual effects."""
        if not self.image:
            return
        
        from PIL import ImageDraw, ImageFont
        from core.utils import calculate_position, normalize_opacity, calculate_optimal_font_size
        
        # Work with original image
        watermarked = self.image.copy().convert("RGBA")
        
        # Calculate optimal font size if using default
        if font_size == 48:  # Default size
            font_size = calculate_optimal_font_size(watermarked.size)
        
        # Create overlay with higher resolution for better text quality
        overlay = Image.new("RGBA", watermarked.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Load font with better fallbacks and bold variants
        try:
            font_paths = [
                f"C:/Windows/Fonts/arialbd.ttf",  # Arial Bold
                f"C:/Windows/Fonts/arial.ttf",    # Arial Regular
                f"/System/Library/Fonts/Arial Bold.ttf",  # macOS Bold
                f"/System/Library/Fonts/Arial.ttf",       # macOS Regular
                f"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux Bold
                f"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"        # Linux Regular
            ]
            font = None
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
            if font is None:
                # Try to use default font but make it larger
                try:
                    from PIL import ImageFont
                    font = ImageFont.load_default()
                except:
                    # Ultimate fallback
                    font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text dimensions with padding
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Add padding for shadow/stroke effects
        padding = max(4, font_size // 12)
        text_size_with_padding = (text_width + padding * 2, text_height + padding * 2)
        
        # Calculate position
        x, y = calculate_position(watermarked.size, text_size_with_padding, position)
        
        # Adjust for padding
        text_x = x + padding
        text_y = y + padding
        
        # Convert color
        if color.startswith('#'):
            text_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        else:
            text_color = (255, 255, 255)  # Default white
        
        # Calculate stroke color (opposite brightness)
        brightness = sum(text_color) / 3
        if brightness > 127:
            stroke_color = (0, 0, 0)  # Black stroke for light text
        else:
            stroke_color = (255, 255, 255)  # White stroke for dark text
        
        # Calculate alpha values
        text_alpha = normalize_opacity(opacity)
        stroke_alpha = normalize_opacity(max(40, opacity - 20))  # Slightly less opaque stroke
        
        # Draw text with stroke/outline for better visibility
        stroke_width = max(1, font_size // 24)
        
        # Draw stroke/outline
        for adj_x in range(-stroke_width, stroke_width + 1):
            for adj_y in range(-stroke_width, stroke_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text((text_x + adj_x, text_y + adj_y), text, font=font, 
                             fill=stroke_color + (stroke_alpha,))
        
        # Draw main text
        draw.text((text_x, text_y), text, font=font, 
                 fill=text_color + (text_alpha,))
        
        # Optional: Add subtle shadow for depth
        if opacity > 60:  # Only add shadow for more opaque text
            shadow_offset = max(2, font_size // 20)
            shadow_alpha = normalize_opacity(20)
            draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, 
                     fill=(0, 0, 0, shadow_alpha))
        
        # Composite with high quality
        result = Image.alpha_composite(watermarked, overlay).convert("RGB")
        return result

    def apply_image_watermark(self, watermark_image, scale=None, position="bottom-right", opacity=75):
        """Apply image watermark to the current image with optimal sizing."""
        if not self.image or not watermark_image:
            return
        
        from core.utils import calculate_position, normalize_opacity, calculate_optimal_image_scale
        
        # Work with original image
        base = self.image.copy().convert("RGBA")
        watermark = watermark_image.copy().convert("RGBA")
        
        # Calculate optimal scale if not provided
        if scale is None:
            scale = calculate_optimal_image_scale(base.size, watermark.size)
        
        # Scale watermark with high quality
        scale_factor = scale / 100
        new_width = int(watermark.width * scale_factor)
        new_height = int(watermark.height * scale_factor)
        
        # Ensure minimum size for visibility
        min_size = min(base.width, base.height) // 20
        if new_width < min_size or new_height < min_size:
            aspect_ratio = watermark.width / watermark.height
            if aspect_ratio > 1:
                new_width = min_size * 2
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min_size * 2
                new_width = int(new_height * aspect_ratio)
        
        watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply opacity with better blending
        if watermark.mode == 'RGBA':
            # Apply opacity to the alpha channel
            alpha = watermark.split()[3]  # Get alpha channel
            alpha = alpha.point(lambda p: int(p * opacity / 100))
            watermark.putalpha(alpha)
        else:
            # Convert to RGBA and add alpha
            watermark = watermark.convert("RGBA")
            alpha_value = normalize_opacity(opacity)
            # Create uniform alpha channel
            alpha = Image.new('L', watermark.size, alpha_value)
            watermark.putalpha(alpha)
        
        # Add subtle drop shadow for better integration
        if opacity > 50:
            shadow_offset = max(2, min(new_width, new_height) // 50)
            shadow = Image.new('RGBA', 
                             (watermark.width + shadow_offset * 2, 
                              watermark.height + shadow_offset * 2), 
                             (0, 0, 0, 0))
            
            # Create shadow
            shadow_alpha = normalize_opacity(min(30, opacity // 3))
            shadow_fill = Image.new('RGBA', watermark.size, (0, 0, 0, shadow_alpha))
            shadow.paste(shadow_fill, (shadow_offset, shadow_offset))
            shadow.paste(watermark, (0, 0), watermark)
            
            # Calculate position for shadow
            x, y = calculate_position(base.size, shadow.size, position)
            
            # Paste shadow first, then watermark
            base = Image.alpha_composite(base, 
                                       Image.new('RGBA', base.size, (0, 0, 0, 0)))
            
            # Create a temporary base for shadow
            temp_base = Image.new('RGBA', base.size, (0, 0, 0, 0))
            temp_base.paste(shadow, (x, y), shadow)
            base = Image.alpha_composite(base, temp_base)
        else:
            # Calculate position without shadow
            x, y = calculate_position(base.size, watermark.size, position)
            
            # Create transparent base and paste watermark
            temp_base = Image.new('RGBA', base.size, (0, 0, 0, 0))
            temp_base.paste(watermark, (x, y), watermark)
            base = Image.alpha_composite(base, temp_base)
        
        return base.convert("RGB")

    def load_image(self, filepath):
        """Load image from file path."""
        try:
            self.show_image(filepath)
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False

    def save_image(self, filepath):
        """Save current image to file."""
        if not self.image:
            return False
        try:
            self.image.save(filepath)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False