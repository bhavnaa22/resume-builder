import PyPDF2
import docx
import os

class InputHandler:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.tex']
    
    def extract_text(self, filepath):
        """Extract text from various file formats"""
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            return self._extract_pdf(filepath)
        elif ext == '.docx':
            return self._extract_docx(filepath)
        elif ext in ['.txt', '.tex']:
            return self._extract_text(filepath)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def _extract_pdf(self, filepath):
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_docx(self, filepath):
        doc = docx.Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def _extract_text(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()