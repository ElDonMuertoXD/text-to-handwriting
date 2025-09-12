from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
import shutil
from typing import Optional, List
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from gemini import GeminiAI
from text_processor import process_text
from handwriting_generator import text_to_handwriting_pillow
from pdf_converter import convert_image_to_pdf

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Text to Handwriting API", version="1.0.0")

# Add the limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssignmentRequest(BaseModel):
    name: str
    class_roll: str
    university_roll: str
    subject_name: str
    subject_code: str
    topics: List[str]  # Changed from question_topic to topics as a list
    output_filename: str
    gemini_api_key: str
    handwriting_id: int  # Added handwriting selection (1-6)
    other_details: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Text to Handwriting API is running"}

@app.post("/generate-assignment")
@limiter.limit("5/minute")  # Allow 1 request per minute per IP
async def generate_assignment(request: Request, assignment_request: AssignmentRequest):
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
        # Validate handwriting_id
        if not (1 <= assignment_request.handwriting_id <= 6):
            raise ValueError("handwriting_id must be between 1 and 6")
        
        ai = GeminiAI(api_key=assignment_request.gemini_api_key)
        full_text = ai.generate_complete_assignment(
            name=assignment_request.name,
            class_roll=assignment_request.class_roll,
            university_roll=assignment_request.university_roll,
            subject_name=assignment_request.subject_name,
            subject_code=assignment_request.subject_code,
            topics=assignment_request.topics,  # Changed from question_topic to topics
            other_details=assignment_request.other_details
        )
        processed_text = process_text(full_text)
        unique_id = str(uuid.uuid4())
        output_dir = os.path.join("output", unique_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate handwritten image(s) with selected handwriting
        image_filename = f"{assignment_request.output_filename}.png"
        image_path = os.path.join(output_dir, image_filename)
        result = text_to_handwriting_pillow(processed_text, image_path, assignment_request.handwriting_id)
        if isinstance(result, tuple):
            image_path, additional_images = result
        else:
            image_path = result
            additional_images = None
        
        # Convert to PDF
        pdf_filename = f"{assignment_request.output_filename}.pdf"
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
        if output_dir and os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)