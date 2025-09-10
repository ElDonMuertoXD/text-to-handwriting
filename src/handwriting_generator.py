from PIL import Image, ImageDraw, ImageFont
import random
import os

def text_to_handwriting_pillow(text: str, output_path: str = "handwriting.png"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Add more handwriting-style fonts here
    handwriting_fonts = [
        # os.path.join(project_root, "fonts", "QEDonaldRoss.ttf"),
        # os.path.join(project_root, "fonts", "QEHerbertCooper.ttf"),
        os.path.join(project_root, "fonts", "RumorsSkill.ttf"),
        # os.path.join(project_root, "fonts", "english_essay.ttf"),
        # os.path.join(project_root, "fonts", "QEMamasAndPapas.ttf") #ts kinda bad
    ]
    
    # Improved parameters for more natural handwriting - A4 size proportions
    font_size = 40       # Larger, more readable handwriting size
    line_height = font_size + 15  # More natural line spacing
    margin_left = 80     # Left margin
    margin_top = 70     # Top margin
    margin_right = 80    # Right margin
    margin_bottom = 10  # Bottom margin
    page_width = 1240    # A4-like width
    page_height = 1754   # A4-like height
    
    # Calculate usable text area
    max_text_width = page_width - margin_left - margin_right
    max_text_height = page_height - margin_top - margin_bottom
    
    # Load font first to calculate text dimensions properly
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
    
    # Create temporary image for text measurement
    temp_img = Image.new('RGB', (page_width, page_height), color='white')
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Handle custom line breaks - replace /LINE_BREAK with actual line breaks
    text = text.replace('/LINE_BREAK', '\n')
    
    # Split text into paragraphs - similar to original code approach
    paragraphs = text.split('\n')
    all_lines = []
    
    # Process each paragraph similar to the original code
    for paragraph in paragraphs:
        if not paragraph.strip():
            # Preserve empty lines for paragraph separation (like original code)
            all_lines.append('')
            continue
        
        # Word wrap based on actual text width, not character count
        words = paragraph.split(' ')
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            
            # Use textbbox to get actual text width
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_text_width:
                current_line = test_line
            else:
                # Line is too long, add current line and start new one
                if current_line.strip():
                    all_lines.append(current_line.strip())
                current_line = word + " "
        
        # Add the remaining text in current_line
        if current_line.strip():
            all_lines.append(current_line.strip())
        
        # Add extra space between paragraphs (matching original code behavior)
        # But only if this isn't the last paragraph and the paragraph has content
        if paragraph.strip():  # Only add spacing after non-empty paragraphs
            all_lines.append('')  # Add empty line for paragraph spacing
    
    # Remove trailing empty lines to clean up
    while all_lines and not all_lines[-1].strip():
        all_lines.pop()
    
    # Calculate pages needed based on actual content
    lines_per_page = max_text_height // line_height
    total_pages = max(1, (len(all_lines) + lines_per_page - 1) // lines_per_page)
    
    images = []
    
    # Generate pages
    for page_num in range(total_pages):
        img = Image.new('RGB', (page_width, page_height), color='white')
        draw = ImageDraw.Draw(img)
        
        y_offset = margin_top
        start_line = page_num * lines_per_page
        end_line = min(start_line + lines_per_page, len(all_lines))
        
        for i in range(start_line, end_line):
            if i >= len(all_lines):
                break
                
            line = all_lines[i]
            
            if line.strip():
                # Add subtle horizontal and vertical variation for natural handwriting look
                x_offset = margin_left + random.randint(-3, 3)
                current_y = y_offset + random.randint(-2, 2)
                
                draw.text((x_offset, current_y), line, fill='black', font=font)
                y_offset += line_height
            else:
                # Empty line - add spacing for paragraph separation (like original code)
                y_offset += line_height // 2
            
            # Break if we're getting close to bottom margin
            if y_offset > page_height - margin_bottom:
                break
        
        images.append(img)
    
    if len(images) == 1:
        images[0].save(output_path)
        return output_path, None
    else:
        # Save first page with original name
        images[0].save(output_path)
        
        # Save additional pages
        base_name = os.path.splitext(output_path)[0]
        additional_page_paths = []
        for i in range(1, len(images)):
            page_path = f"{base_name}_page_{i+1}.png"
            images[i].save(page_path)
            additional_page_paths.append(page_path)
        
        return output_path, images[1:]  # Return first page path and additional images