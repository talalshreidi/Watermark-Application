# 🖼️ Watermark Application

A Tkinter watermark application made by Talal Shreidi.

## ✨ Features

### Text Watermarks
- **Customizable Text**: Add any text as watermark
- **Font Size Control**: Range from 12px to 144px for perfect visibility
- **Color Picker**: Choose any color with visual preview
- **Position Control**: 5 position options (center, corners)
- **Opacity Control**: Adjust transparency (0-100%)

### Image Watermarks
- **Logo Support**: Add PNG/JPG logos as watermarks
- **Scale Control**: Resize from 5% to 100% of original
- **Position Control**: Place anywhere on the image
- **Opacity Control**: Semi-transparent overlays
- **Format Support**: PNG, JPG, JPEG, BMP, TIFF, GIF

### User Interface
- **Before/After Preview**: See original and watermarked side by side
- **Tabbed Interface**: Separate panels for text and image watermarks
- **Error Handling**: Helpful error messages and validation

## 🚀 Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

## 💡 Usage

### Adding Text Watermarks
1. Click **"Open Image"** to load your photo
2. Switch to **"Text Watermark"** tab
3. Enter your watermark text
4. Adjust font size, color, position, and opacity
5. Click **"Apply Text Watermark"**
6. Click **"Save Image"** to export

### Adding Image Watermarks
1. Click **"Open Image"** to load your photo  
2. Switch to **"Image Watermark"** tab
3. Click **"Select Watermark"** to choose your logo
4. Adjust scale, position, and opacity
5. Click **"Apply Image Watermark"**
6. Click **"Save Image"** to export

## 🎯 Perfect Settings for Great Results (Now Default!)

### Text Watermarks ✨ NEW DEFAULTS
- **Font Size**: **Auto** - Dynamically calculates optimal size based on image dimensions
- **Opacity**: **85%** for excellent visibility with professional subtlety
- **Position**: **bottom-right** for professional branding placement
- **Color**: **White with black stroke** for maximum visibility on any background
- **Enhanced Features**: Automatic text stroke/outline, subtle drop shadows, bold font variants

### Image Watermarks ✨ NEW DEFAULTS
- **Scale**: **Auto** - Intelligently calculates 15% of image area for perfect proportion
- **Opacity**: **75%** for professional semi-transparent effect
- **Position**: **bottom-right** corner for standard placement
- **Enhanced Features**: Automatic drop shadows, high-quality scaling, opacity blending

## 🛠️ Technical Details

- **Framework**: Tkinter (Python standard library)
- **Image Processing**: Pillow (PIL Fork)
- **Architecture**: Modular design with separate UI and core logic
- **Supported Formats**: PNG, JPG, JPEG, BMP, TIFF, GIF

## 📁 Project Structure

```
watermark_app/
├── main.py                 # Application entry point
├── ui/
│   ├── main_window.py      # Main application window
│   ├── preview_canvas.py   # Image display and watermark logic
│   ├── text_watermark_panel.py   # Text watermark controls
│   └── image_watermark_panel.py  # Image watermark controls
├── core/
│   └── utils.py            # Helper functions
├── assets/                 # Sample images
├── output/                 # Saved watermarked images
├── fonts/                  # Custom fonts (optional)
└── requirements.txt        # Dependencies
```

## 🎨 Enhanced Features & Polish

### ✨ Smart Watermark Technology
- **Auto Font Sizing**: Dynamically calculates perfect font size based on image dimensions
- **Auto Image Scaling**: Intelligently sizes watermarks to 15% of image area
- **Text Stroke & Shadow**: Automatic outlines and shadows for maximum visibility
- **Professional Positioning**: Adaptive margins that scale with image size

### 🔧 Technical Excellence
- **High-Quality Rendering**: LANCZOS resampling with enhanced blending
- **Cross-Platform Fonts**: Bold font variants with comprehensive fallbacks
- **Perfect Defaults**: Zero configuration needed - beautiful results immediately
- **Advanced Opacity**: Sophisticated alpha blending for natural integration
- **Memory Optimized**: Efficient image processing with quality preservation

### 🎯 Professional Features
- **Copyright Symbol**: Default "© Your Watermark" template
- **White-on-Dark Design**: Maximum visibility with automatic stroke detection
- **Bottom-Right Placement**: Industry standard professional positioning
- **Batch-Ready**: Optimized settings work perfectly across different image sizes

---

Made by Talal Shreidi