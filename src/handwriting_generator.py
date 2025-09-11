from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import os
import numpy as np
import cv2
import math

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

def create_character_variations():
    """Create random variations for character rendering"""
    return {
        'scale_x': random.uniform(0.92, 1.08),
        'scale_y': random.uniform(0.94, 1.06),
        'rotation': random.uniform(-2.5, 2.5),  # degrees
        'baseline_offset': random.uniform(-1.5, 1.5),
        'thickness_variation': random.uniform(0.85, 1.15),
        'letter_spacing': random.uniform(-2, 4),  # pixels
    }

def add_character_imperfections(image, char_bbox, imperfection_chance=0.15):
    """Add subtle imperfections to individual characters"""
    if random.random() > imperfection_chance:
        return image
    
    img_array = np.array(image)
    x1, y1, x2, y2 = char_bbox
    
    # Add slight ink blobs occasionally
    if random.random() < 0.3:
        blob_x = random.randint(max(0, x1), min(img_array.shape[1]-1, x2))
        blob_y = random.randint(max(0, y1), min(img_array.shape[0]-1, y2))
        blob_size = random.randint(1, 2)
        
        # Create small ink blob
        y_start = max(0, blob_y - blob_size)
        y_end = min(img_array.shape[0], blob_y + blob_size + 1)
        x_start = max(0, blob_x - blob_size)
        x_end = min(img_array.shape[1], blob_x + blob_size + 1)
        
        ink_color = (random.randint(20, 40), random.randint(20, 40), random.randint(50, 80))
        img_array[y_start:y_end, x_start:x_end] = ink_color
    
    return Image.fromarray(img_array)

def add_writing_surface_roughness(draw, text_position, text_size, text_content, font):
    """Add micro-variations to simulate paper texture affecting writing"""
    x, y = text_position
    
    # Create multiple slightly offset versions of the text for roughness
    for offset_x, offset_y in [(-0.3, 0.2), (0.2, -0.3), (0.1, 0.4)]:
        rough_x = x + offset_x
        rough_y = y + offset_y
        
        # Use slightly lighter color for roughness effect
        rough_color = (random.randint(180, 220), random.randint(180, 220), random.randint(200, 240))
        draw.text((rough_x, rough_y), text_content, fill=rough_color, font=font)

def apply_writing_fatigue(line_number, total_lines):
    """Apply fatigue effects - writing gets slightly less neat over time"""
    fatigue_factor = min(line_number / max(total_lines * 0.7, 1), 1.0)
    
    return {
        'extra_spacing_variation': fatigue_factor * 2,
        'extra_tilt_variation': fatigue_factor * 0.3,
        'extra_size_variation': fatigue_factor * 0.02,
        'tremor_intensity': fatigue_factor * 0.5,
    }

def render_character_with_variations(draw, char, position, font, base_color, variations, temp_draw):
    """Render a single character with realistic variations"""
    char_x, char_y = position
    
    # Apply baseline offset
    char_y += variations['baseline_offset']
    
    # Create slightly varied color for this character
    color_variation = variations['thickness_variation']
    varied_color = (
        int(base_color[0] * color_variation),
        int(base_color[1] * color_variation), 
        int(base_color[2] * color_variation)
    )
    varied_color = tuple(max(0, min(255, c)) for c in varied_color)
    
    # Add surface roughness first (lighter background texture)
    if random.random() < 0.4:  # 40% chance for roughness
        add_writing_surface_roughness(draw, (char_x, char_y), None, char, font)
    
    # Render main character
    draw.text((char_x, char_y), char, fill=varied_color, font=font)
    
    # Calculate character width for spacing
    char_bbox = temp_draw.textbbox((0, 0), char, font=font)
    char_width = char_bbox[2] - char_bbox[0]
    
    return char_width

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
                # Apply writing fatigue effects
                fatigue = apply_writing_fatigue(i, len(all_lines))
                
                # Add horizontal and vertical variation for natural handwriting look (increased)
                base_x_offset = margin_left + random.randint(-8, 8)
                base_y_offset = y_offset + random.randint(-7, 7)
                
                # Add line tilt with fatigue effect
                base_tilt = random.uniform(-0.8, 0.8)
                line_tilt_angle = base_tilt + random.uniform(-fatigue['extra_tilt_variation'], fatigue['extra_tilt_variation'])
                line_length = len(line) * (font_size * 0.6)
                
                # Render character by character with realistic variations
                current_x = base_x_offset
                
                # Process each character individually
                for char_idx, char in enumerate(line):
                    if char == ' ':
                        # Variable space width
                        space_width = font_size * 0.3 + random.uniform(-3, 6) + fatigue['extra_spacing_variation']
                        current_x += space_width
                        continue
                    
                    # Create character variations
                    char_variations = create_character_variations()
                    
                    # Calculate position with line tilt
                    char_progress = current_x / max(line_length, 1)
                    tilt_offset = char_progress * line_length * (line_tilt_angle * 0.017453)
                    
                    # Add character-level variation with fatigue
                    char_x = current_x + random.uniform(-1.2, 1.2) + char_variations['letter_spacing']
                    char_y = base_y_offset + tilt_offset + random.uniform(-0.8, 0.8) + char_variations['baseline_offset']
                    
                    # Add tremor effect for fatigue
                    if fatigue['tremor_intensity'] > 0:
                        tremor_x = random.uniform(-fatigue['tremor_intensity'], fatigue['tremor_intensity'])
                        tremor_y = random.uniform(-fatigue['tremor_intensity'], fatigue['tremor_intensity'])
                        char_x += tremor_x
                        char_y += tremor_y
                    
                    # Use varied ink color
                    base_ink_color = (random.randint(10, 30), random.randint(10, 30), random.randint(35, 65))
                    
                    # Render character with all variations
                    char_width = render_character_with_variations(
                        draw, char, (char_x, char_y), font, base_ink_color, char_variations, temp_draw
                    )
                    
                    # Move cursor with variable spacing
                    current_x += char_width + char_variations['letter_spacing']
                    
                    # Occasionally add small ink artifacts
                    if random.random() < 0.08:  # 8% chance
                        artifact_x = char_x + random.randint(-3, char_width + 3)
                        artifact_y = char_y + random.randint(-2, font_size + 2)
                        artifact_color = (random.randint(40, 80), random.randint(40, 80), random.randint(60, 100))
                        draw.ellipse([artifact_x-0.5, artifact_y-0.5, artifact_x+0.5, artifact_y+0.5], fill=artifact_color)
                
                y_offset += line_height + random.randint(-2, 3)  # Variable line spacing
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