import google.generativeai as genai
import os
from typing import Optional

class GeminiAI:
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided either as parameter or environment variable")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_assignment_content(
        self,
        name: str,
        class_roll: str,
        university_roll: str,
        subject_name: str,
        subject_code: str,
        question_topic: str,
        other_details: Optional[str] = None
    ) -> str:
        """
        Generate assignment content based on the given parameters
        """
        # Create header information with proper line breaks
        header_info = f"""Name: {name} \n

            Class Roll: {class_roll} \n

            University Roll: {university_roll} \n

            Subject: {subject_name} \n

            Subject Code: {subject_code} \n
        """

        if other_details:
            header_info += f"\n\n{other_details}"
        
        # Create prompt for content generation
        prompt = f"""Write a detailed assignment answer for the following topic: {question_topic}

Please provide a comprehensive answer that would be suitable for a university-level assignment for the subject "{subject_name}". 
The answer should be:
- Well-structured with proper paragraphs
- Include relevant points and examples
- Be approximately 400-600 words long
- Sound like it's written by a student (not overly formal or academic)
- Include proper introduction, body, and conclusion
- Be informative and demonstrate understanding of the topic

Topic: {question_topic}"""
        
        try:
            response = self.model.generate_content(prompt)
            generated_content = response.text
            
            # Combine header and generated content with proper spacing
            full_text = header_info + "\n\n" + "Question: " + question_topic + "\n\nAnswer:\n\n" + generated_content
            
            return full_text
            
        except Exception as e:
            raise Exception(f"Error generating content with Gemini: {str(e)}")