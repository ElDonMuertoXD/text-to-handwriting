from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import os
import numpy as np
import cv2

# ts adds a sublte yellow tint and noise to simulate paper texture
def add_paper_texture(image):
    """Add realistic paper texture to the image"""
    width, height = image.size
    noise = np.random.normal(0, 8, (height, width, 3))
    img_array = np.array(image)
    textured = img_array.astype(np.float32) + noise
    textured = np.clip(textured, 0, 255).astype(np.uint8)
    
    # Create slight color variation for aged paper effect
    tint = np.ones_like(textured) * [252, 248, 240]
    textured = (textured * 0.95 + tint * 0.05).astype(np.uint8)
    
    return Image.fromarray(textured)

def draw_pencil_margins(draw, width, height, margin_left, margin_top):
    """Draw realistic hand-drawn pencil margins using straight lines"""
    
    def draw_straight_pencil_line(start_x, start_y, end_x, end_y, color=(100, 100, 120)):
        """Draw a straight pencil line with very slight natural tilt"""
        # Add very subtle tilt variation (much smaller than hand-drawn)
        if start_x == end_x:  # Vertical line
            # Very slight horizontal drift for vertical lines
            tilt_variation = random.uniform(-0.5, 0.5)  # Very small tilt
            end_x += tilt_variation
        else:  # Horizontal line  
            # Very slight vertical drift for horizontal lines
            tilt_variation = random.uniform(-0.5, 0.5)  # Very small tilt
            end_y += tilt_variation
        
        # Draw main line
        draw.line([start_x, start_y, end_x, end_y], fill=color, width=1)
        
        # Add slight pencil texture by drawing parallel lines with slight opacity variation
        for offset in [-0.5, 0.5]:
            if abs(start_x - end_x) < 1:  # Vertical line (accounting for slight tilt)
                texture_color = (color[0] + 5, color[1] + 5, color[2] + 5)  # Reduced texture variation
                draw.line([start_x + offset, start_y, end_x + offset, end_y], fill=texture_color, width=1)
            else:  # Horizontal line
                texture_color = (color[0] + 5, color[1] + 5, color[2] + 5)  # Reduced texture variation
                draw.line([start_x, start_y + offset, end_x, end_y + offset], fill=texture_color, width=1)

    # Gray/slate pencil color
    pencil_color = (168, 170, 173)
    
    # Vertical left margin line - spans full height of page
    start_y = 0  # Start from very top
    end_y = height  # End at very bottom
    margin_x = margin_left - 25  # Position for margin line
    draw_straight_pencil_line(margin_x, start_y, margin_x, end_y, pencil_color)
    
    # Horizontal top margin line - spans full width of page
    start_x = 0  # Start from very left edge
    end_x = width  # End at very right edge
    margin_y = margin_top - 25  # Position for margin line
    draw_straight_pencil_line(start_x, margin_y, end_x, margin_y, pencil_color)
    
    # Add intersection reinforcement where lines meet (also with reduced opacity)
    intersection_x = margin_x
    intersection_y = margin_y
    # Draw a small circle at intersection to make it look more realistic
    draw.ellipse([intersection_x-1, intersection_y-1, intersection_x+1, intersection_y+1], 
                 fill=pencil_color)
    
    # Add some margin dots/marks (like notebook paper) - positioned after the lines
    dot_color = (185, 188, 190) 
    for i in range(3):
        y_pos = margin_top + 10 + i * 15  # No random variation
        x_pos = margin_left - 35  # Positioned between margin line and text
        draw.ellipse([x_pos-1, y_pos-1, x_pos+1, y_pos+1], fill=dot_color)
    
    # Optional: Add some small tick marks along the margins for notebook-like appearance
    tick_color = (200, 202, 205)
    
    # Small ticks along the vertical margin
    for i in range(3, int((height - margin_top - 50) / 120)):
        tick_y = margin_top + i * 120  # No random variation
        tick_x = margin_x
        draw.line([tick_x-3, tick_y, tick_x+3, tick_y], fill=tick_color, width=1)
    
    # Small ticks along the horizontal margin
    for i in range(2, int((width - margin_left - 100) / 180)):
        tick_x = margin_left + i * 180  # No random variation
        tick_y = margin_y
        draw.line([tick_x, tick_y-3, tick_x, tick_y+3], fill=tick_color, width=1)

def add_ink_bleeding_effect(image, text_color=(0, 0, 0)):
    """Add subtle ink bleeding effect to text"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Find text pixels (non-white pixels)
    text_mask = np.any(img_array < 250, axis=2)
    
    # Create a slightly larger version for bleeding effect
    bleeding_img = image.copy()
    bleeding_img = bleeding_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Blend original with bleeding version
    blended = Image.blend(image, bleeding_img, 0.15)
    
    return blended

def apply_phone_scan_distortion(image):
    """Apply realistic phone scan perspective distortion"""
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Define source points (perfect rectangle)
    src_points = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    
    # Define destination points (slightly skewed for phone scan effect)
    # Basically trying to make it so that it is narrower on the top and wider on the bottom
    top_offset = random.randint(5, 15)
    bottom_offset = random.randint(-3, 3)
    side_skew = random.randint(-5, 5)
    
    dst_points = np.float32([
        [top_offset, random.randint(-5, 5)],
        [w - top_offset + side_skew, random.randint(-5, 5)],
        [w + bottom_offset, h + random.randint(-5, 5)],
        [bottom_offset - side_skew, h + random.randint(-5, 5)]
    ])
    
    # Apply perspective transform
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(img_array, matrix, (w, h), borderValue=(255, 255, 255))
    
    return Image.fromarray(warped)

def add_realistic_lighting(image):
    """Add subtle lighting effects as if photographed with phone"""
    # Create a gradient overlay for lighting effect
    width, height = image.size
    gradient = Image.new('L', (width, height), 255)
    
    # Create subtle radial gradient (brighter in center, darker at edges)
    # so it looks like the picture has been clicked from phone
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2
    
    for y in range(height):
        for x in range(width):
            distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
            brightness = max(240, 255 - int((distance / max_radius) * 15))
            gradient.putpixel((x, y), brightness)
    
    # Apply gradient as overlay
    gradient_rgb = gradient.convert('RGB')
    result = Image.blend(image, gradient_rgb, 0.05)
    
    return result

def add_scan_noise(image):
    """Add realistic scanning noise and compression artifacts"""
    # Add subtle noise
    width, height = image.size
    noise_array = np.random.normal(0, 2, (height, width, 3))
    
    img_array = np.array(image).astype(np.float32)
    noisy = img_array + noise_array
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    
    result = Image.fromarray(noisy)
    
    # Simulate slight JPEG compression
    import io
    buffer = io.BytesIO()
    result.save(buffer, format='JPEG', quality=92)  # Slight compression
    buffer.seek(0)
    result = Image.open(buffer)
    
    return result

def text_to_handwriting_pillow(text: str, output_path: str = "handwriting.png"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Add more handwriting-style fonts here
    handwriting_fonts = [
        # os.path.join(project_root, "fonts", "RumorsSkill.ttf"),
        os.path.join(project_root, "fonts", "english_essay.ttf"),
    ]
    
    # Improved parameters for more natural handwriting - A4 size proportions
    font_size = 40       # Larger, more readable handwriting size
    line_height = font_size + 20  # More natural line spacing
    margin_left = 100    # Increased left margin to account for pencil margin
    margin_top = 90      # Increased top margin to account for pencil margin
    margin_right = 80    # Right margin
    margin_bottom = 10   # Bottom margin
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
        # Start with off-white background for realistic paper color
        img = Image.new('RGB', (page_width, page_height), color=(254, 252, 248))
        
        # Add paper texture first
        img = add_paper_texture(img)
        
        draw = ImageDraw.Draw(img)
        
        # Draw pencil margins
        draw_pencil_margins(draw, page_width, page_height, margin_left, margin_top)
        
        y_offset = margin_top
        start_line = page_num * lines_per_page
        end_line = min(start_line + lines_per_page, len(all_lines))
        
        for i in range(start_line, end_line):
            if i >= len(all_lines):
                break
                
            line = all_lines[i]
            if line.strip():
                # Add subtle horizontal and vertical variation for natural handwriting look
                base_x_offset = margin_left + random.randint(-3, 3)
                base_y_offset = y_offset + random.randint(-2, 2)
                
                # Add very subtle line tilt (simulate natural hand movement)
                # Calculate line tilt - very small angle variation
                line_tilt_angle = random.uniform(-0.5, 0.5)  # degrees, very subtle
                line_length = len(line) * (font_size * 0.6)  # approximate line width
                
                # For very subtle effect, we'll render character by character with slight vertical drift
                current_x = base_x_offset
                words = line.split(' ')
                
                for word_idx, word in enumerate(words):
                    if word_idx > 0:  # Add space between words
                        word = ' ' + word
                    
                    # Calculate slight vertical drift based on line tilt
                    char_progress = current_x / max(line_length, 1)  # 0 to 1 progress across line
                    tilt_offset = char_progress * line_length * (line_tilt_angle * 0.017453)  # Convert degrees to radians
                    
                    # Add character-level variation for more natural look
                    char_x = current_x + random.uniform(-0.5, 0.5)
                    char_y = base_y_offset + tilt_offset + random.uniform(-0.3, 0.3)
                    
                    # Use slightly varied dark blue/black for ink
                    ink_color = (random.randint(15, 25), random.randint(15, 25), random.randint(40, 60))
                    draw.text((char_x, char_y), word, fill=ink_color, font=font)
                    
                    # Calculate width of this word to move cursor
                    word_bbox = temp_draw.textbbox((0, 0), word, font=font)
                    word_width = word_bbox[2] - word_bbox[0]
                    current_x += word_width
                
                y_offset += line_height
            else:
                # Empty line - add spacing for paragraph separation
                y_offset += line_height // 2
            
            # Break if we're getting close to bottom margin
            if y_offset > page_height - margin_bottom:
                break
        
        # Apply post-processing effects for realism
        img = add_ink_bleeding_effect(img)
        img = apply_phone_scan_distortion(img)
        img = add_realistic_lighting(img)
        img = add_scan_noise(img)
        
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