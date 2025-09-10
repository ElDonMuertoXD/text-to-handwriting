from PIL import Image, ImageDraw, ImageFont
import random
import os

def text_to_handwriting_pillow(text: str, output_path: str = "handwriting.png"):
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Array of good handwriting fonts with absolute paths
    handwriting_fonts = [
        os.path.join(project_root, "fonts", "QEDonaldRoss.ttf"),
        os.path.join(project_root, "fonts", "QEHerbertCooper.ttf"),
        os.path.join(project_root, "fonts", "QEMamasAndPapas.ttf")
    ]
    
    # Create image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a random handwriting-style font
    font = None
    for font_path in random.sample(handwriting_fonts, len(handwriting_fonts)):
        try:
            if os.path.exists(font_path):
                print(f"Loading font: {font_path}")  # Debug message
                font = ImageFont.truetype(font_path, 24)
                break
        except Exception as e:
            print(f"Failed to load font {font_path}: {e}")  # Debug message
            continue
    
    # Fallback to default font if no handwriting fonts are available
    if font is None:
        print("Using default font - no handwriting fonts found")  # Debug message
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
    
    # Add some handwriting-like variations
    lines = text.split('\n')
    y_offset = 50
    
    for line in lines:
        # Add slight random variations to make it look more handwritten
        x_offset = 50
        draw.text((x_offset, y_offset), line, fill='black', font=font)
        y_offset += 40
    
    img.save(output_path)
    return output_path