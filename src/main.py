from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
import shutil
import zipfile
from typing import Optional

from gemini import GeminiAI
from text_processor import process_text
from handwriting_generator import text_to_handwriting_pillow
from pdf_converter import convert_image_to_pdf

app = FastAPI(title="Text to Handwriting API", version="1.0.0")

class AssignmentRequest(BaseModel):
    name: str
    class_roll: str
    university_roll: str
    subject_name: str
    subject_code: str
    question_topic: str
    output_filename: str
    gemini_api_key: str  # New required field
    other_details: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Text to Handwriting API is running"}

@app.post("/generate-assignment")
async def generate_assignment(request: AssignmentRequest):
    """
    Single route that:
    1. Uses Gemini AI to generate assignment content
    2. Converts text to handwriting image(s)
    3. Converts image(s) to PDF
    4. Returns PDF and cleans up temporary files
    """
    unique_id = None
    output_dir = None
    
    try:
        # Initialize Gemini AI with provided API key
        ai = GeminiAI(api_key=request.gemini_api_key)
        
        # Generate assignment content using AI
        full_text = ai.generate_complete_assignment(
            name=request.name,
            class_roll=request.class_roll,
            university_roll=request.university_roll,
            subject_name=request.subject_name,
            subject_code=request.subject_code,
            question_topic=request.question_topic,
            other_details=request.other_details
        )
        
        # Process the text
        processed_text = process_text(full_text)
        
        # Create unique output directory for this request
        unique_id = str(uuid.uuid4())
        output_dir = os.path.join("output", unique_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate handwritten image(s)
        image_filename = f"{request.output_filename}.png"
        image_path = os.path.join(output_dir, image_filename)
        result = text_to_handwriting_pillow(processed_text, image_path)
        
        # Handle single or multiple pages
        if isinstance(result, tuple):
            image_path, additional_images = result
        else:
            image_path = result
            additional_images = None
        
        # Convert to PDF
        pdf_filename = f"{request.output_filename}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        convert_image_to_pdf(image_path, pdf_path, additional_images)
        
        # Return the PDF file with cleanup
        async def cleanup():
            try:
                if output_dir and os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
            except Exception as e:
                print(f"Error cleaning up files: {e}")
        
        return FileResponse(
            path=pdf_path,
            filename=pdf_filename,
            media_type='application/pdf',
            background=cleanup
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Clean up on error
        if output_dir and os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)