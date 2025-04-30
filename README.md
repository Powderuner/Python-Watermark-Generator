# Image Watermark Script

This Python script allows you to add watermarks to images. You can add either text watermarks or image watermarks with customizable positions, opacity, and size.

## Requirements

- Python 3.x
- Pillow (PIL) library

Install the required dependencies using:
```bash
pip install -r requirements.txt
```

## Directory Structure

```
.
├── images/          # Place your source images here
├── logos/           # Place your logo files here
├── output/          # Watermarked images will be saved here
├── automata.py      # Main script
└── requirements.txt # Project dependencies
```

## Features

- Add text watermarks with customizable:
  - Font size
  - Color and opacity
  - Position (bottom-right, bottom-left, top-right, top-left, center)
- Add image watermarks with customizable:
  - Opacity
  - Scale
  - Position (bottom-right, bottom-left, top-right, top-left, center)

## Usage

1. Place your images in the `images/` folder
2. Place any logo files in the `logos/` folder
3. Run the script:
   ```bash
   python automata.py
   ```
4. Follow the interactive prompts to:
   - Select an image to watermark
   - Choose whether to add text watermark
   - Choose whether to add logo watermark
   - Select watermark position
   - Configure font size and other options

The script will create watermarked versions of your images in the `output/` folder.

## Position Options

Both text and image watermarks support the following position options:
- 'bottom-right'
- 'bottom-left'
- 'top-right'
- 'top-left'
- 'center' 