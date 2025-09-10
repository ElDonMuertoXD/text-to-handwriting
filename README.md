# text-to-handwriting Project

This project converts text input into a handwritten style image and saves it as a PDF file. It utilizes the PyWhatkit library for handwriting generation.

## Project Structure

```
text-to-handwriting
├── src
│   ├── main.py
│   ├── text_processor.py
│   ├── handwriting_generator.py
│   └── pdf_converter.py
├── output
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd text-to-handwriting
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```
   python src/main.py
   ```

2. Follow the prompts to enter the text you want to convert to handwriting.

3. The output will be saved as a PDF in the `output` directory.

## Dependencies

- PyWhatkit
- Pillow (for image handling)
- FPDF (for PDF generation)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.