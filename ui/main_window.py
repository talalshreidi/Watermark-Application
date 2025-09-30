import tkinter as tk
from ui.preview_canvas import PreviewCanvas
from ui.text_watermark_panel import TextWatermarkPanel
from ui.image_watermark_panel import ImageWatermarkPanel
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Watermark Application")
        self.resizable(False, False)
        self.geometry("1100x700")

        # Add status bar at the bottom FIRST
        self.status_bar = tk.Frame(self, relief=tk.SUNKEN, bd=1, height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)  # Prevent shrinking
        
        self.status_label = tk.Label(self.status_bar, text="Ready - Load an image to start watermarking", 
                                   font=("Arial", 9), anchor="w", padx=5, pady=2)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Main content frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Container Frame for Top and Bottom Canvases (LEFT SIDE)
        self.container_previews_frame = tk.Frame(main_frame, width=450)
        self.container_previews_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(10, 5), pady=10)
        self.container_previews_frame.pack_propagate(False)  # Maintain fixed width

        # Add label for original image
        tk.Label(self.container_previews_frame, text="📸 Original Image", 
                font=("Arial", 11, "bold")).pack(pady=(5, 0))

        self.top_frame = PreviewCanvas(self.container_previews_frame, highlightbackground="blue", 
                                     width=420, height=280)
        self.top_frame.pack(pady=5)

        # Add horizontal separator
        sep = ttk.Separator(self.container_previews_frame, orient='horizontal')
        sep.pack(fill=tk.X, pady=8)

        # Add label for watermarked image
        tk.Label(self.container_previews_frame, text="✨ Watermarked Result", 
                font=("Arial", 11, "bold")).pack(pady=(0, 5))

        self.bottom_frame = PreviewCanvas(self.container_previews_frame, highlightbackground="red", 
                                        width=420, height=280)
        self.bottom_frame.pack(pady=5)

        # RIGHT SIDE: Controls Panel
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        self.notebook = ttk.Notebook(controls_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.text_watermark = TextWatermarkPanel(self.notebook, preview_canvas=self.top_frame, watermark_canvas=self.bottom_frame)
        self.notebook.add(self.text_watermark, text="📝 Text Watermark")

        self.image_watermark = ImageWatermarkPanel(self.notebook, preview_canvas=self.top_frame, watermark_canvas=self.bottom_frame)
        self.notebook.add(self.image_watermark, text="🖼️ Image Watermark")
    
    def update_status(self, message):
        """Update the status bar message."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            self.update_idletasks()  # Force immediate update