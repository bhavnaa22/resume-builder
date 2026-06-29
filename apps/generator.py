from google import genai
from google.genai import types
import os
import subprocess

class ResumeGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.latex_available = self._check_latex()
    
    def _check_latex(self):
        try:
            subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def generate_latex(self, processed_data):
        prompt = f"""Create a professional LaTeX resume.
        
Job Keywords: {', '.join(processed_data.get('keywords', []))}
Content: {processed_data.get('raw_text', '')[:2000]}

Requirements:
- Use article or moderncv class
- Include keywords naturally
- 1-2 pages max
- ATS-friendly format

Return ONLY LaTeX code, no markdown."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            latex_code = response.text
            
            # Clean markdown if present
            if '```latex' in latex_code:
                latex_code = latex_code.split('```latex')[1].split('```')[0]
            elif '```' in latex_code:
                latex_code = latex_code.split('```')[1].split('```')[0]
            
            return latex_code.strip()
            
        except Exception as e:
            print(f"API Error: {e}")
            return self._fallback_template()
    
    def _fallback_template(self):
        return r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\begin{document}
\centerline{\LARGE\textbf{Resume}}
\vspace{1em}
\noindent API Error - Please retry.
\end{document}"""