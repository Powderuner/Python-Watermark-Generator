from PIL import Image, ImageDraw, ImageFont
import os

def add_text_watermark(
    image_path,
    output_path,
    text,
    font_size=36,
    font_color=(255, 255, 255, 128),  # White with 50% opacity
    position='bottom-right'
):
    """
    Add a text watermark to an image
    
    Args:
        image_path (str): Path to the source image
        output_path (str): Path to save the watermarked image
        text (str): Text to use as watermark
        font_size (int): Size of the font
        font_color (tuple): RGBA color tuple for the text
        position (str): Position of the watermark ('bottom-right', 'bottom-left', 'top-right', 'top-left', 'center')
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGBA if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a copy of the image
            watermarked = img.copy()
            
            # Create drawing context
            draw = ImageDraw.Draw(watermarked)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype("Arial", font_size)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Calculate position
            margin = 10
            if position == 'bottom-right':
                text_position = (img.width - text_width - margin, img.height - text_height - margin)
            elif position == 'bottom-left':
                text_position = (margin, img.height - text_height - margin)
            elif position == 'top-right':
                text_position = (img.width - text_width - margin, margin)
            elif position == 'top-left':
                text_position = (margin, margin)
            else:  # center
                text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
            
            # Add text watermark
            draw.text(text_position, text, font=font, fill=font_color)
            
            # Save the watermarked image
            watermarked.save(output_path)
            print(f"Successfully added text watermark to {output_path}")
            
    except Exception as e:
        print(f"Error adding text watermark: {str(e)}")

def add_image_watermark(
    image_path,
    watermark_image_path,
    output_path,
    position='bottom-right',
    opacity=0.5,
    scale=0.25
):
    """
    Add an image watermark to an image
    
    Args:
        image_path (str): Path to the source image
        watermark_image_path (str): Path to the watermark image
        output_path (str): Path to save the watermarked image
        position (str): Position of the watermark ('bottom-right', 'bottom-left', 'top-right', 'top-left', 'center')
        opacity (float): Opacity of the watermark (0-1)
        scale (float): Scale factor for the watermark size relative to the main image
    """
    try:
        # Open the main image
        with Image.open(image_path) as img:
            # Convert to RGBA if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Open and resize the watermark image
            with Image.open(watermark_image_path) as watermark:
                if watermark.mode != 'RGBA':
                    watermark = watermark.convert('RGBA')
                
                # Calculate new size for watermark
                new_width = int(img.width * scale)
                new_height = int(new_width * watermark.height / watermark.width)
                watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create a copy of the watermark with desired opacity
                watermark.putalpha(int(255 * opacity))
                
                # Calculate position
                margin = 10
                if position == 'bottom-right':
                    paste_position = (img.width - watermark.width - margin, img.height - watermark.height - margin)
                elif position == 'bottom-left':
                    paste_position = (margin, img.height - watermark.height - margin)
                elif position == 'top-right':
                    paste_position = (img.width - watermark.width - margin, margin)
                elif position == 'top-left':
                    paste_position = (margin, margin)
                else:  # center
                    paste_position = ((img.width - watermark.width) // 2, (img.height - watermark.height) // 2)
                
                # Create a new blank image with the same size as the original
                watermarked = Image.new('RGBA', img.size, (0, 0, 0, 0))
                watermarked.paste(img, (0, 0))
                watermarked.paste(watermark, paste_position, watermark)
                
                # Save the watermarked image
                watermarked.save(output_path)
                print(f"Successfully added image watermark to {output_path}")
                
    except Exception as e:
        print(f"Error adding image watermark: {str(e)}")

def list_images(directory):
    """List all image files in a directory"""
    images = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            images.append(file)
    return images

def get_user_choice(options, prompt):
    """Get user choice from a list of options"""
    if not options:
        return None
        
    print("\n" + prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Skip/No selection")
    
    while True:
        try:
            choice = input("\nEnter number: ")
            if choice == "0":
                return None
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def process_images(
    image_file,
    logos_directory="logos",
    output_directory="output",
    text="",
    logo_filename=None,
    add_text=True,
    add_logo=True,
    font_size=36,
    logo_opacity=0.3,
    logo_scale=0.2,
    position='bottom-right'
):
    """Process a single image with watermarks"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Full path to the logo file if logo watermarking is enabled
    logo_path = os.path.join(logos_directory, logo_filename) if logo_filename else None
    
    name, ext = os.path.splitext(image_file)
    input_path = os.path.join("images", image_file)
    
    # Add text watermark
    if add_text and text:
        text_output = os.path.join(output_directory, f"{name}_text{ext}")
        try:
            add_text_watermark(
                image_path=input_path,
                output_path=text_output,
                text=text,
                font_size=font_size,
                position=position
            )
            print(f"Added text watermark to {image_file}")
        except Exception as e:
            print(f"Error adding text watermark to {image_file}: {str(e)}")
    
    # Add logo watermark
    if add_logo and logo_path:
        logo_output = os.path.join(output_directory, f"{name}_logo{ext}")
        try:
            add_image_watermark(
                image_path=input_path,
                watermark_image_path=logo_path,
                output_path=logo_output,
                opacity=logo_opacity,
                scale=logo_scale,
                position=position
            )
            print(f"Added logo watermark to {image_file}")
        except Exception as e:
            print(f"Error adding logo watermark to {image_file}: {str(e)}")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("images", exist_ok=True)
    os.makedirs("logos", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # List available images
    images = list_images("images")
    if not images:
        print("No images found in the 'images' folder!")
        print("\nDirectory structure:")
        print("- logos/     (place your logo files here)")
        print("- images/    (place images to watermark here)")
        print("- output/    (watermarked images will appear here)")
        exit(1)
    
    # Get image selection from user
    image_file = get_user_choice(images, "Select an image to watermark:")
    if not image_file:
        print("No image selected. Exiting...")
        exit(0)
    
    # Ask about text watermark
    add_text = input("\nAdd text watermark? (y/n): ").lower().startswith('y')
    text = ""
    font_size = 36
    if add_text:
        text = input("Enter text for watermark: ")
        try:
            size = input("Enter font size (default 36): ")
            if size:
                font_size = int(size)
        except ValueError:
            print("Invalid font size. Using default (36)")
    
    # Ask about logo watermark
    add_logo = input("\nAdd logo watermark? (y/n): ").lower().startswith('y')
    logo_filename = None
    if add_logo:
        logos = list_images("logos")
        if logos:
            logo_filename = get_user_choice(logos, "Select a logo:")
            if not logo_filename:
                add_logo = False
        else:
            print("No logo files found in the 'logos' folder. Skipping logo watermark.")
            add_logo = False
    
    # Get position
    positions = ['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center']
    position = get_user_choice(positions, "Select watermark position:")
    if not position:
        position = 'bottom-right'
        print("Using default position (bottom-right)")
    
    # Process the image
    process_images(
        image_file=image_file,
        logos_directory="logos",
        output_directory="output",
        text=text,
        logo_filename=logo_filename,
        add_text=add_text,
        add_logo=add_logo,
        font_size=font_size,
        position=position
    )
    
    print("\nProcessing complete! Check the 'output' folder for your watermarked images.") 