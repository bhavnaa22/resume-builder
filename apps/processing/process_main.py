import re
from apps.input.input_main import InputHandler

class ProcessHandler:
    def __init__(self, gemini_api_key):
        self.input_handler = InputHandler()
        self.api_key = gemini_api_key
    
    def process_resume_and_jd(self, resume_path, job_description):
        """Process resume and job description using Gemini"""
        import google.generativeai as genai
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Extract resume text
        resume_text = self.input_handler.extract_text(resume_path)
        
        # Extract keywords from JD
        keywords = self._extract_keywords(model, job_description)
        
        # Structure the data
        processed = {
            'raw_text': resume_text,
            'job_description': job_description,
            'keywords': keywords,
            'structured': self._structure_resume(model, resume_text)
        }
        
        return processed
    
    def _extract_keywords(self, model, job_description):
        """Extract important keywords from job description"""
        prompt = f"""
        Extract the top 10-15 most important keywords/skills from this job description.
        Return as a comma-separated list.
        
        Job Description:
        {job_description}
        """
        
        response = model.generate_content(prompt)
        keywords = [k.strip() for k in response.text.split(',')]
        return keywords
    
    def _structure_resume(self, model, resume_text):
        """Structure resume into sections"""
        prompt = f"""
        Parse this resume text into structured sections.
        Return JSON format with keys: personal_info, summary, experience (list), education (list), skills (list).
        
        Resume:
        {resume_text}
        """
        
        response = model.generate_content(prompt)
        # Parse JSON response
        try:
            import json
            return json.loads(response.text)
        except:
            return {'raw': resume_text}