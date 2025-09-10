from PIL import Image, ImageDraw, ImageFont
import random
import os

def text_to_handwriting_pillow(text: str, output_path: str = "handwriting.png"):
    # Array of good handwriting fonts (you'll need to download these)
    handwriting_fonts = [
        "fonts/Kalam-Regular.ttf",
        "fonts/Caveat-Regular.ttf",
        "fonts/Dancing_Script-Regular.ttf",
        "fonts/Indie_Flower.ttf",
        "fonts/Permanent_Marker.ttf",
        "fonts/Architects_Daughter.ttf",
        "fonts/Shadows_Into_Light.ttf",
        "fonts/Amatic_SC-Regular.ttf",
        "fonts/Gloria_Hallelujah.ttf",
        "fonts/Satisfy-Regular.ttf"
    ]
    
    # Create image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a random handwriting-style font
    font = None
    for font_path in random.sample(handwriting_fonts, len(handwriting_fonts)):
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 24)
                break
        except:
            continue
    
    # Fallback to default font if no handwriting fonts are available
    if font is None:
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