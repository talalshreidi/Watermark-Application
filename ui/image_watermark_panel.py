import tkinter as tk
from tkinter import filedialog, ttk, messagebox  # Add messagebox
from PIL import Image, ImageTk

# Class Takes in params: tk.Frame, pass a preview canvas object to interact with it

class ImageWatermarkPanel(tk.Frame):
    def __init__(self, master=None, preview_canvas=None, watermark_canvas=None, **kwargs):
        super().__init__(master, **kwargs)
        self.watermark_image_path = None
        self.watermark_image = None
        self.preview_canvas = preview_canvas
        self.watermark_canvas = watermark_canvas  # Add this line
        self.setup_widgets()

    def setup_widgets(self):
        # Title
        tk.Label(self, text="Image Watermark Panel", font=("Arial", 12, "bold")).pack(pady=10)
        
        # === WATERMARK IMAGE SELECTION ===
        watermark_frame = tk.LabelFrame(self, text="Watermark Image", font=("Arial", 10, "bold"))
        watermark_frame.pack(pady=10, fill="x", padx=10)
        
        # Watermark selection buttons
        btn_row = tk.Frame(watermark_frame)
        btn_row.pack(pady=5, fill="x", padx=5)
        
        tk.Button(btn_row, text="Select Watermark", command=self.select_watermark_dialog,
                 bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side="left", padx=5)
        
        tk.Button(btn_row, text="Remove", command=self.remove_watermark,
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(side="left", padx=5)
        
        # Selected file display
        self.watermark_label = tk.Label(watermark_frame, text="No watermark image selected", 
                                      wraplength=300, font=("Arial", 9), fg="gray")
        self.watermark_label.pack(pady=5, padx=5)
        
        # === WATERMARK SETTINGS ===
        settings_frame = tk.LabelFrame(self, text="Watermark Settings", font=("Arial", 10, "bold"))
        settings_frame.pack(pady=10, fill="x", padx=10)
        
        # Scale setting
        scale_frame = tk.Frame(settings_frame)
        scale_frame.pack(pady=5, fill="x", padx=5)
        
        tk.Label(scale_frame, text="Scale:", font=("Arial", 10)).pack(anchor="w")
        
        # Add Auto checkbox
        self.auto_scale = tk.BooleanVar(value=True)
        auto_frame = tk.Frame(scale_frame)
        auto_frame.pack(fill="x", pady=2)
        tk.Checkbutton(auto_frame, text="Auto Scale", variable=self.auto_scale, 
                      command=self.toggle_auto_scale).pack(side="left")
        
        self.scale_var = tk.IntVar(value=15)
        self.scale_slider = tk.Scale(scale_frame, from_=5, to=100, orient="horizontal",
                                   variable=self.scale_var, length=200, state="disabled")
        self.scale_slider.pack(pady=2)
        self.scale_label = tk.Label(scale_frame, text="Auto")
        self.scale_slider.config(command=self.update_scale_label)
        self.scale_label.pack()
        self.scale_slider.config(command=self.update_scale_label)
        
        # Position setting
        position_frame = tk.Frame(settings_frame)
        position_frame.pack(pady=5, fill="x", padx=5)
        
        tk.Label(position_frame, text="Position:", font=("Arial", 10)).pack(anchor="w")
        self.position = ttk.Combobox(position_frame, values=["center", "top-left", "top-right", 
                                                           "bottom-left", "bottom-right"], width=15)
        self.position.current(4)  # Default to bottom-right
        self.position.pack(pady=2)
        
        # Opacity setting
        opacity_frame = tk.Frame(settings_frame)
        opacity_frame.pack(pady=5, fill="x", padx=5)
        
        tk.Label(opacity_frame, text="Opacity:", font=("Arial", 10)).pack(anchor="w")
        self.opacity_var = tk.IntVar(value=70)
        self.opacity_slider = tk.Scale(opacity_frame, from_=0, to=100, orient="horizontal",
                                     variable=self.opacity_var, length=200)
        self.opacity_slider.pack(pady=2)
        self.opacity_label = tk.Label(opacity_frame, text="70%")
        self.opacity_label.pack()
        self.opacity_slider.config(command=self.update_opacity_label)
        
        # === SEPARATOR ===
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=15, padx=10)
        
        # === ACTION BUTTONS ===
        controls_frame = tk.LabelFrame(self, text="🛠️ Actions", font=("Arial", 10, "bold"))
        controls_frame.pack(pady=15, fill="x", padx=10, side=tk.BOTTOM, expand=False)
        
        # Create organized button layout
        button_container = tk.Frame(controls_frame)
        button_container.pack(pady=10, fill="x", padx=10)
        
        # Primary action button (full width)
        tk.Button(button_container, text="🎨 Apply Image Watermark", 
                 command=self.apply_watermark,
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), 
                 height=2, relief=tk.RAISED, bd=2).pack(pady=(0, 10), fill="x")
        
        # Secondary action buttons (side by side)
        secondary_frame = tk.Frame(button_container)
        secondary_frame.pack(fill="x")
        
        # Three buttons in a row
        tk.Button(secondary_frame, text="📁 Open Image", command=self.open_image,
                 bg="#9C27B0", fg="white", font=("Arial", 9), 
                 height=2, relief=tk.RAISED, bd=2).pack(side="left", padx=(0, 3), expand=True, fill="x")
        
        tk.Button(secondary_frame, text="💾 Save Result", command=self.save_image,
                 bg="#2196F3", fg="white", font=("Arial", 9), 
                 height=2, relief=tk.RAISED, bd=2).pack(side="left", padx=3, expand=True, fill="x")
        
        tk.Button(secondary_frame, text="🔄 Reset Settings", command=self.reset,
                 bg="#FF9800", fg="white", font=("Arial", 9), 
                 height=2, relief=tk.RAISED, bd=2).pack(side="right", padx=(3, 0), expand=True, fill="x")

    def select_watermark_dialog(self):
        """Open dialog to select watermark image."""
        filename = filedialog.askopenfilename(
            title="Select Watermark Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.watermark_image_path = filename
            # Show just the filename, not full path
            display_name = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
            self.watermark_label.config(text=f"Selected: {display_name}", fg="green")
            
            try:
                # Load and store the watermark image
                self.watermark_image = Image.open(filename)
                print(f"Watermark image loaded: {display_name}")
            except Exception as e:
                self.watermark_label.config(text=f"Error loading: {display_name}", fg="red")
                print(f"Error loading watermark: {e}")

    def remove_watermark(self):
        """Remove selected watermark image."""
        self.watermark_image_path = None
        self.watermark_image = None
        self.watermark_label.config(text="No watermark image selected", fg="gray")
        print("Watermark image removed")

    def update_scale_label(self, value):
        """Update scale percentage label."""
        self.scale_label.config(text=f"{value}%")

    def update_opacity_label(self, value):
        """Update opacity percentage label."""
        self.opacity_label.config(text=f"{value}%")
    
    def toggle_auto_scale(self):
        """Toggle between auto and manual scale."""
        if self.auto_scale.get():
            self.scale_slider.config(state="disabled")
            self.scale_label.config(text="Auto")
        else:
            self.scale_slider.config(state="normal")
            self.scale_label.config(text=f"{self.scale_var.get()}%")

    

    def apply_watermark(self):
        """Apply image watermark to the current image."""
        if not self.watermark_image_path:
            messagebox.showwarning("No Watermark", "Please select a watermark image first!")
            return
            
        if not self.preview_canvas or not self.preview_canvas.image:
            messagebox.showwarning("No Image", "Please load an image first!")
            return
            
        # Handle scale (Auto or manual)
        if self.auto_scale.get():
            scale = None  # Will be auto-calculated
        else:
            scale = self.scale_var.get()
        
        position = self.position.get()
        opacity = self.opacity_var.get()
        
        # Apply watermark
        result = self.preview_canvas.apply_image_watermark(
            self.watermark_image, scale, position, opacity
        )
        
        if result and self.watermark_canvas:
            self.watermark_canvas.show_image(result)
            # Update preview canvas image for saving
            self.preview_canvas.image = result

    def open_image_dialog(self):
        """Open dialog to select base image."""
        filename = filedialog.askopenfilename(
            title="Select Image to Watermark",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if filename:
            if self.preview_canvas:
                success = self.preview_canvas.load_image(filename)
                if success and self.watermark_canvas:
                    self.watermark_canvas.clear()
                    image_name = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
                    print(f"✅ Loaded image: {image_name}")
                    messagebox.showinfo("Success", f"Image loaded successfully!\n{image_name}")
                else:
                    messagebox.showerror("Error", "Failed to load image!")
            else:
                messagebox.showerror("Error", "No preview canvas available!")

    def save_image(self):
        """Save the watermarked image with automatic naming."""
        try:
            if self.preview_canvas and hasattr(self.preview_canvas, 'image'):
                image = self.preview_canvas.image
                if isinstance(image, Image.Image):
                    import os
                    from datetime import datetime
                    
                    # Create output directory if it doesn't exist
                    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(output_dir, f"watermarked_image_{timestamp}.png")
                    
                    image.save(filename)
                    messagebox.showinfo("✅ Success", f"Image saved successfully!\n{os.path.basename(filename)}")
                    print(f"💾 Saved: {filename}")
                else:
                    messagebox.showwarning("⚠️ Warning", "No watermarked image to save.")
            else:
                messagebox.showerror("❌ Error", "No image available to save!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to save image: {e}")
            print(f"Error saving image: {e}")

    def save_image_dialog(self):
        """Open dialog to save the watermarked image."""
        filename = filedialog.asksaveasfilename(
            title="Save Watermarked Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        if filename:
            print(f"Saving watermarked image to: {filename}")
            # Save the current image in the preview canvas
            try:
                image = self.preview_canvas.image
                if isinstance(image, Image.Image):
                    image.save(filename)
                    messagebox.showinfo("Image Saved", f"Watermarked image saved as:\n{filename}")
                else:
                    messagebox.showwarning("No Image", "No watermarked image to save.")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving image: {e}")

    def save_image(self):
        """Save the watermarked image with auto-generated filename."""
        try:
            import os
            from datetime import datetime
            
            # Create output directory if it doesn't exist
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"watermarked_image_{timestamp}.png")
            
            # Save the current image from the preview canvas
            if self.preview_canvas and hasattr(self.preview_canvas, 'image'):
                image = self.preview_canvas.image
                if isinstance(image, Image.Image):
                    image.save(filename)
                    print(f"✅ Image saved: {filename}")
                    messagebox.showinfo("Success", f"Image saved successfully!\n{filename}")
                else:
                    messagebox.showwarning("No Image", "No watermarked image to save.")
            else:
                messagebox.showwarning("No Image", "No watermarked image to save.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving image: {e}")

    def open_image(self):
        """Open dialog to select and load a base image."""
        filename = filedialog.askopenfilename(
            title="Select Base Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if filename and self.preview_canvas:
            success = self.preview_canvas.load_image(filename)
            if success:
                image_name = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
                print(f"✅ Loaded base image: {image_name}")
                messagebox.showinfo("Success", f"Base image loaded successfully!\n{image_name}")
            else:
                messagebox.showerror("Error", "Failed to load image!")

    def reset(self):
        """Reset all settings to defaults."""
        # Remove watermark
        self.remove_watermark()
        
        # Reset scale
        self.auto_scale.set(True)
        self.scale_var.set(15)
        self.scale_slider.config(state="disabled")
        self.scale_label.config(text="Auto")
        
        # Reset position
        self.position.current(4)  # Back to bottom-right
        
        # Reset opacity
        self.opacity_var.set(70)
        self.opacity_label.config(text="70%")
        
        print("Image watermark settings reset to defaults")

    def get_settings(self):
        """Get current watermark settings as a dictionary."""
        return {
            'watermark_path': self.watermark_image_path,
            'watermark_image': self.watermark_image,
            'scale': self.scale_var.get(),
            'position': self.position.get(),
            'opacity': self.opacity_var.get()
        }