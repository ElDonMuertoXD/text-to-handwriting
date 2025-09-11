import google.generativeai as genai
import os
from typing import Optional

class GeminiAI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided either as parameter or environment variable")
        
        genai.configure(api_key=self.api_key)
        
        system_instruction = """
        You are an assistant that writes plain text responses only for handwritten assignments.
        MANDATORY FORMATTING RULES:
        - NEVER use markdown formatting like *, **, _, __, #, ```, or any other special characters for formatting
        - Write as if you are handwriting on paper - use only regular text
        - When you want to create a line break or spacing, use /LINE_BREAK
        - Separate paragraphs naturally with double line breaks
        - Start writing the assignment content immediately without any introductory phrases
        - Do NOT write "Answer:" or any similar prefixes - just start with the content
        - Write in a natural, student-like tone suitable for handwritten assignments
        - Use proper paragraph structure with clear topic sentences"""
        
        self.model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
    
    def generate_header_section(
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
        Generate the header section with proper formatting for handwritten assignments
        """
        header_lines = [
            f"Name: {name}",
            f"Class Roll: {class_roll}", 
            f"University Roll: {university_roll}",
            f"Subject: {subject_name}",
            f"Subject Code: {subject_code}"
        ]

        header_info = "/LINE_BREAK".join(header_lines)
        
        if other_details:
            header_info += f"/LINE_BREAK/LINE_BREAK{other_details}"
        
        header_info += f"/LINE_BREAK/LINE_BREAK/LINE_BREAKTopic: {question_topic}/LINE_BREAK/LINE_BREAK"
        
        return header_info
    
    def generate_assignment_content(
        self,
        subject_name: str,
        question_topic: str
    ) -> str:
        """
        Generate only the assignment answer content (no header information)
        """
        prompt = f"""Write a detailed assignment answer for the topic: {question_topic}
                CRITICAL FORMATTING RULES:
                - Use ONLY plain text - absolutely NO markdown syntax
                - NO asterisks (*), NO hashtags (#), NO underscores (_), NO backticks (`)
                - NO special formatting characters whatsoever
                - Write exactly as if you are writing with a pen on paper
                - Use /LINE_BREAK only when you need to force a specific line break
                - Separate paragraphs naturally with double line breaks
                - Write in simple, clear sentences
                - Do NOT start with "Answer:" or any prefix - just begin writing the content
                - Do NOT include any header information like name, roll numbers, subject details

                Write a comprehensive university-level assignment answer for "{subject_name}" that includes:
                - A clear introduction to the topic
                - Main body with relevant points and examples  
                - A proper conclusion
                - Approximately 400-600 words
                - Academic but student-friendly tone
                - Demonstrate good understanding of the subject

                Start writing the assignment content immediately without any prefixes or headers.

                Topic: {question_topic}"""
        
        try:
            response = self.model.generate_content(prompt)
            generated_content = response.text
            
            # we are only interested in plain text
            generated_content = self._clean_markdown(generated_content)
            
            return generated_content
            
        except Exception as e:
            raise Exception(f"Error generating content with Gemini: {str(e)}")
    
    def generate_complete_assignment(
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
        Generate complete assignment with header and content
        """
        header_section = self.generate_header_section(
            name, class_roll, university_roll, subject_name, subject_code, question_topic, other_details
        )
        
        content = self.generate_assignment_content(subject_name, question_topic)
        
        # Combine header and content
        full_text = header_section + content
        
        return full_text
    
    def _clean_markdown(self, text: str) -> str:
        """
        Remove common markdown syntax from text - enhanced version
        """
        import re
        
        # Remove markdown headers (# ## ### etc.)
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        
        # Remove bold/italic markers (* ** _ __)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # *italic*
        text = re.sub(r'__(.*?)__', r'\1', text)      # __bold__
        text = re.sub(r'_(.*?)_', r'\1', text)        # _italic_
        
        # Remove code blocks and inline code
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # ```code```
        text = re.sub(r'`(.*?)`', r'\1', text)                  # `code`
        
        # Remove bullet points and list markers
        text = re.sub(r'^[-*+]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
        
        # Remove blockquotes
        text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
        
        # Remove any remaining asterisks used for emphasis
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        
        # Clean up multiple spaces but preserve intentional line breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Only clean horizontal whitespace
        
        return text.strip()