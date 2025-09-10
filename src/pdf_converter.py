from fpdf import FPDF
import os

def convert_image_to_pdf(image_path, pdf_path=None):
    """
    Convert image to PDF
    """
    if pdf_path is None:
        # Generate PDF path in same directory as image
        base_name = os.path.splitext(image_path)[0]
        pdf_path = f"{base_name}.pdf"
    
    pdf = FPDF()
    pdf.add_page()
    
    # Get page dimensions (A4: 210x297mm)
    page_width = pdf.w - 20  # Leave 10mm margin on each side
    page_height = pdf.h - 20  # Leave 10mm margin on top and bottom
    
    # Add image to fit A4 page
    pdf.image(image_path, x=10, y=10, w=page_width)
    pdf.output(pdf_path)
    
    print(f"PDF saved as: {pdf_path}")
    return pdf_path