from text_processor import process_text
from handwriting_generator import text_to_handwriting_pillow as generate_handwriting_image
from pdf_converter import convert_image_to_pdf
import os

def main():
    # Get user input
    user_input = input("Enter the text you want to convert to handwriting: ")

    # Process the text
    processed_text = process_text(user_input)

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate handwritten image in output folder
    image_path = os.path.join(output_dir, "handwriting.png")
    image_path = generate_handwriting_image(processed_text, image_path)
    print(f"Handwritten image saved as: {image_path}")

    # Convert image to PDF (will be saved in same directory as image)
    pdf_path = convert_image_to_pdf(image_path)

    print(f"Handwritten text has been saved as a PDF: {pdf_path}")

if __name__ == "__main__":
    main()