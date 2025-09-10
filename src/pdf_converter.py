from fpdf import FPDF
import os

def convert_image_to_pdf(image_path, pdf_path=None, additional_images=None):
    """
    Convert image(s) to PDF
    """
    if pdf_path is None:
        # Generate PDF path in same directory as image
        base_name = os.path.splitext(image_path)[0]
        pdf_path = f"{base_name}.pdf"
    
    pdf = FPDF()
    
    # Add first page
    pdf.add_page()
    page_width = pdf.w - 20
    page_height = pdf.h - 20
    
    # Calculate image dimensions to fit page while maintaining aspect ratio
    pdf.image(image_path, x=10, y=10, w=page_width)
    
    # Add additional pages if provided
    if additional_images:
        for img in additional_images:
            # Save temporary image file for each PIL image
            temp_path = f"temp_page_{len(pdf.pages)}.png"
            img.save(temp_path)
            
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=page_width)
            
            # Clean up temporary file
            os.remove(temp_path)
    
    pdf.output(pdf_path)
    
    print(f"PDF saved as: {pdf_path}")
    return pdf_path