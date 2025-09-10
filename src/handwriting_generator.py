from PIL import Image, ImageDraw, ImageFont
import random
import os
import textwrap

def text_to_handwriting_pillow(text: str, output_path: str = "handwriting.png"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Add more handwriting-style fonts here
    handwriting_fonts = [
        os.path.join(project_root, "fonts", "QEDonaldRoss.ttf"),
        os.path.join(project_root, "fonts", "QEHerbertCooper.ttf"),
        os.path.join(project_root, "fonts", "RumorsSkill.ttf"),
        # os.path.join(project_root, "fonts", "QEMamasAndPapas.ttf") #ts kinda bad
    ]
    
    # Improved parameters for more natural handwriting
    line_height = 60  # Increased line height for better spacing
    font_size = 32    # Bigger font size
    margin = 80       # Larger margins
    page_width = 1400  # Wider page
    page_height = 2000 # Taller page to accommodate more content naturally
    chars_per_line = 60  # Reduced characters per line for more natural look
    
    # Split text into lines and wrap them
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        if line.strip():
            # Wrap long lines
            wrapped = textwrap.wrap(line.strip(), width=chars_per_line)
            if wrapped:
                wrapped_lines.extend(wrapped)
            else:
                wrapped_lines.append('')
        else:
            # Empty line for paragraph separation
            wrapped_lines.append('')
    
    # Calculate number of pages needed
    lines_per_page = (page_height - 2 * margin) // line_height
    total_pages = max(1, (len(wrapped_lines) + lines_per_page - 1) // lines_per_page)
    
    images = []
    
    # Load font
    font = None
    for font_path in random.sample(handwriting_fonts, len(handwriting_fonts)):
        try:
            if os.path.exists(font_path):
                print(f"Loading font: {font_path}")
                font = ImageFont.truetype(font_path, font_size)
                break
        except Exception as e:
            print(f"Failed to load font {font_path}: {e}")
            continue
    
    if font is None:
        print("Using default font - no handwriting fonts found")
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
    
    # Generate pages
    for page_num in range(total_pages):
        img = Image.new('RGB', (page_width, page_height), color='white')
        draw = ImageDraw.Draw(img)
        
        y_offset = margin
        start_line = page_num * lines_per_page
        end_line = min(start_line + lines_per_page, len(wrapped_lines))
        
        for i in range(start_line, end_line):
            line = wrapped_lines[i]
            
            if line.strip():
                # Add horizontal variation for natural handwriting look
                x_offset = margin + random.randint(-10, 10)
                # Add slight vertical variation
                current_y = y_offset + random.randint(-3, 3)
                
                draw.text((x_offset, current_y), line, fill='black', font=font)
            
            # Always advance y_offset, even for empty lines (paragraph spacing)
            y_offset += line_height
            
            # Break if we're getting close to bottom margin
            if y_offset > page_height - margin:
                break
        
        images.append(img)
    
    # Save images
    if len(images) == 1:
        images[0].save(output_path)
    else:
        # Save multiple pages
        base_name = os.path.splitext(output_path)[0]
        saved_paths = []
        for i, img in enumerate(images):
            page_path = f"{base_name}_page_{i+1}.png"
            img.save(page_path)
            saved_paths.append(page_path)
        
        # Return the first page path (we'll handle multiple pages in PDF converter)
        output_path = saved_paths[0]
    
    return output_path, images if len(images) > 1 else None