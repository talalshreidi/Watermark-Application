import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox  # Add messagebox

class TextWatermarkPanel(tk.Frame):
    def __init__(self, master=None, preview_canvas=None, watermark_canvas=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_color = "#FFFFFF"  # Default to white for better visibility
        self.preview_canvas = preview_canvas
        self.watermark_canvas = watermark_canvas  # Add this line
        self.setup_widgets()

    def setup_widgets(self):
        # Create a scrollable frame for all content
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Title
        tk.Label(main_frame, text="Text Watermark Panel", font=("Arial", 12, "bold")).pack(pady=(5, 10))
        
        # === TEXT INPUT SECTION ===
        text_section = tk.LabelFrame(main_frame, text="Watermark Text", font=("Arial", 9, "bold"), pady=5)
        text_section.pack(fill="x", padx=5, pady=(0, 8))
        
        self.text_entry = tk.Entry(text_section, width=30, font=("Arial", 10))
        self.text_entry.pack(pady=8, padx=8, fill="x")
        self.text_entry.insert(0, "© Your Watermark")
        self.text_entry.config(fg='grey')
        self.text_entry.bind('<FocusIn>', self.on_entry_click)
        self.text_entry.bind('<FocusOut>', self.on_focusout)
        
        # === FONT & POSITION SETTINGS (Combined) ===
        settings_section = tk.LabelFrame(main_frame, text="Appearance Settings", font=("Arial", 9, "bold"), pady=5)
        settings_section.pack(fill="x", padx=5, pady=(0, 8))
        
        # Font Size
        font_row = tk.Frame(settings_section)
        font_row.pack(fill="x", padx=8, pady=5)
        tk.Label(font_row, text="Size:", font=("Arial", 9)).pack(side="left")
        self.font_size = ttk.Combobox(font_row, values=["Auto", 24, 32, 40, 48, 56, 64, 72, 80, 96, 120, 144], width=8)
        self.font_size.current(0)  # Default to Auto for optimal sizing
        self.font_size.pack(side="right")
        
        # Position
        position_row = tk.Frame(settings_section)
        position_row.pack(fill="x", padx=8, pady=5)
        tk.Label(position_row, text="Position:", font=("Arial", 9)).pack(side="left")
        self.position = ttk.Combobox(position_row, values=["center", "top-left", "top-right", "bottom-left", "bottom-right"], width=12)
        self.position.current(4)  # Default to bottom-right for professional look
        self.position.pack(side="right")
        
        # === COLOR SETTINGS SECTION ===
        color_section = tk.LabelFrame(main_frame, text="Color & Opacity", font=("Arial", 9, "bold"), pady=5)
        color_section.pack(fill="x", padx=5, pady=(0, 8))
        
        # Color picker
        color_row = tk.Frame(color_section)
        color_row.pack(fill="x", padx=8, pady=5)
        tk.Label(color_row, text="Color:", font=("Arial", 9)).pack(side="left")
        self.color_picker = tk.Label(color_row, text="Click to choose", bg="white", fg="black", 
                                   width=15, height=1, relief="raised", cursor="hand2", font=("Arial", 8))
        self.color_picker.pack(side="right", padx=(5, 0))
        self.color_picker.bind("<Button-1>", self.choose_color_dialog)
        
        # Opacity
        opacity_row = tk.Frame(color_section)
        opacity_row.pack(fill="x", padx=8, pady=5)
        tk.Label(opacity_row, text="Opacity:", font=("Arial", 9)).pack(side="left")
        self.opacity_var = tk.IntVar(value=80)
        
        opacity_control_frame = tk.Frame(opacity_row)
        opacity_control_frame.pack(side="right")
        
        self.opacity_scale = tk.Scale(opacity_control_frame, from_=0, to=100, orient="horizontal", 
                                    variable=self.opacity_var, length=120, font=("Arial", 8))
        self.opacity_scale.pack(side="left")
        
        self.opacity_label = tk.Label(opacity_control_frame, text="80%", font=("Arial", 9), width=4)
        self.opacity_label.pack(side="right", padx=(5, 0))
        self.opacity_scale.config(command=self.update_opacity_label)
        
        # === SEPARATOR ===
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=10, padx=5)
        
        # === ACTION BUTTONS ===
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(5, 10), fill="x", padx=5, side=tk.BOTTOM, expand=False)
        
        # Main action button
        tk.Button(button_frame, text="Apply Text Watermark", command=self.apply_watermark, 
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), 
                 height=2, relief=tk.RAISED, bd=2).pack(pady=(0, 8), fill="x")
        
        # File operation buttons in a grid
        file_ops_frame = tk.Frame(button_frame)
        file_ops_frame.pack(fill="x")
        
        tk.Button(file_ops_frame, text="📁 Open Image", command=self.open_image_dialog, 
                 bg="#2196F3", fg="white", font=("Arial", 9), width=13, 
                 height=1, relief=tk.RAISED, bd=1).pack(side="left", padx=(0, 3), fill="x", expand=True)
        
        tk.Button(file_ops_frame, text="💾 Save Image", command=self.save_image_dialog, 
                 bg="#FF9800", fg="white", font=("Arial", 9), width=13, 
                 height=1, relief=tk.RAISED, bd=1).pack(side="left", padx=3, fill="x", expand=True)
        
        tk.Button(file_ops_frame, text="🔄 Reset", command=self.reset, 
                 bg="#f44336", fg="white", font=("Arial", 9), width=13, 
                 height=1, relief=tk.RAISED, bd=1).pack(side="left", padx=(3, 0), fill="x", expand=True)

    def on_entry_click(self, event):
        """Handle placeholder text behavior when clicking on entry."""
        if self.text_entry.get() == "© Your Watermark":
            self.text_entry.delete(0, "end")
            self.text_entry.config(fg='black')

    def on_focusout(self, event):
        """Handle placeholder text behavior when losing focus."""
        if self.text_entry.get() == "":
            self.text_entry.insert(0, "© Your Watermark")
            self.text_entry.config(fg='grey')

    def update_opacity_label(self, value):
        """Update opacity percentage label."""
        self.opacity_label.config(text=f"{value}%")

    def choose_color_dialog(self, event=None):
        """Open color picker dialog."""
        color = colorchooser.askcolor(title="Choose watermark color", initialcolor=self.selected_color)
        if color[1]:  # If user didn't cancel
            self.selected_color = color[1]
            self.color_picker.config(bg=self.selected_color)
            # Set text color to white or black based on background brightness
            rgb_sum = sum(color[0])
            text_color = "white" if rgb_sum < 384 else "black"
            self.color_picker.config(fg=text_color)

    def apply_watermark(self):
        """Apply text watermark to the current image."""
        text = self.text_entry.get()
        if text and text != "© Your Watermark":
            if not self.preview_canvas or not self.preview_canvas.image:
                messagebox.showwarning("No Image", "Please load an image first!")
                return
                
            # Handle font size (Auto or specific size)
            font_size_value = self.font_size.get()
            if font_size_value == "Auto":
                font_size = 48  # Will be auto-calculated in apply_text_watermark
            else:
                font_size = int(font_size_value)
            
            position = self.position.get()
            opacity = self.opacity_var.get()
            
            # Apply watermark
            result = self.preview_canvas.apply_text_watermark(
                text, font_size, self.selected_color, position, opacity
            )
            
            if result and self.watermark_canvas:
                self.watermark_canvas.show_image(result)
                # Update preview canvas image for saving
                self.preview_canvas.image = result
                messagebox.showinfo("Success", "✨ Text watermark applied successfully!\nYou can now save the watermarked image.")
            else:
                messagebox.showerror("Error", "Failed to apply watermark. Please try again.")
                
        else:
            messagebox.showwarning("Input Error", "Please enter watermark text!")

    def open_image_dialog(self):
        """Open file dialog to select an image."""
        filename = filedialog.askopenfilename(
            title="Select Image",
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
        
    def save_image_dialog(self):
        """Open file dialog to save the current image."""
        filename = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        if filename:
            if self.preview_canvas and self.preview_canvas.image:
                success = self.preview_canvas.save_image(filename)
                if success:
                    messagebox.showinfo("Success", "Image saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save image!")
            else:
                messagebox.showwarning("No Image", "No image to save!")
        
    def reset(self):
        """Reset all settings to defaults."""
        # Reset text entry
        self.text_entry.delete(0, "end")
        self.text_entry.insert(0, "© Your Watermark")
        self.text_entry.config(fg='grey')
        
        # Reset font size
        self.font_size.current(0)  # Back to Auto
        
        # Reset color
        self.selected_color = "#FFFFFF"
        self.color_picker.config(bg="white", fg="black")
        
        # Reset position
        self.position.current(4)  # Back to bottom-right
        
        # Reset opacity
        self.opacity_var.set(80)
        self.opacity_label.config(text="80%")
        
        print("Text watermark settings reset to defaults")

    def get_settings(self):
        """Get current watermark settings as a dictionary."""
        text = self.text_entry.get()
        if text == "© Your Watermark":
            text = ""
        
        return {
            'text': text,
            'font_size': int(self.font_size.get()) if self.font_size.get() else 16,
            'color': self.selected_color,
            'position': self.position.get(),
            'opacity': self.opacity_var.get()
        }