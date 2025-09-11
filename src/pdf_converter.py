from fpdf import FPDF
import os
from PIL import Image

def compress_image(image_path, quality=75, max_dimension=1600):
    """
    Compress image by reducing quality and dimensions
    """
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Resize if too large
        width, height = img.size
        if max(width, height) > max_dimension:
            ratio = max_dimension / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with compression
        compressed_path = f"compressed_{os.path.basename(image_path)}"
        img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
        
        return compressed_path

def convert_image_to_pdf(image_path, pdf_path=None, additional_images=None):
    """
    Convert image(s) to PDF with compression
    """
    if pdf_path is None:
        # Generate PDF path in same directory as image
        base_name = os.path.splitext(image_path)[0]
        pdf_path = f"{base_name}.pdf"
    
    pdf = FPDF()
    compressed_files = []
    
    try:
        # Compress first image - improved quality settings
        compressed_main = compress_image(image_path, quality=80, max_dimension=1600)
        compressed_files.append(compressed_main)
        
        # Add first page
        pdf.add_page()
        page_width = pdf.w - 20
        
        # Calculate image dimensions to fit page while maintaining aspect ratio
        pdf.image(compressed_main, x=10, y=10, w=page_width)
        
        # Add additional pages if provided
        if additional_images:
            for i, img in enumerate(additional_images):
                # Save PIL image as temporary file
                temp_path = f"temp_page_{i}.png"
                img.save(temp_path)
                compressed_files.append(temp_path)
                
                # Compress the temporary image - improved quality
                compressed_temp = compress_image(temp_path, quality=80, max_dimension=1600)
                compressed_files.append(compressed_temp)
                
                pdf.add_page()
                pdf.image(compressed_temp, x=10, y=10, w=page_width)
        
        # Output PDF
        pdf.output(pdf_path)
        
    finally:
        # Clean up all temporary and compressed files
        for file_path in compressed_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {file_path}: {e}")
    
    print(f"PDF saved as: {pdf_path}")
    return pdf_path