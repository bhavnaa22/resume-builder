import os

class OutputHandler:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def save_latex(self, job_id, latex_code):
        """Save LaTeX code to file"""
        filepath = os.path.join(self.output_dir, f'resume_{job_id}.tex')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        return filepath
    
    def save_cover_letter(self, job_id, latex_code):
        """Save cover letter LaTeX"""
        filepath = os.path.join(self.output_dir, f'cover_{job_id}.tex')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        return filepath