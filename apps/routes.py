import os
import json
import subprocess
import time
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from apps.generator import ResumeGenerator
from apps.input.input_main import InputHandler
from apps.processing.process_main import ProcessHandler

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# ============ PAGE ROUTES ============

@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@main_bp.route('/upload')
def upload_page():
    """Upload resume and job description"""
    return render_template('upload.html')

@main_bp.route('/preview/<job_id>')
def preview_page(job_id):
    """Preview generated LaTeX/PDF"""
    return render_template('preview.html', job_id=job_id)

@main_bp.route('/download/<job_id>')
def download_page(job_id):
    """Download final files"""
    return render_template('download.html', job_id=job_id)

@main_bp.route('/history')
def history_page():
    """View generation history"""
    return render_template('history.html')

# ============ API ROUTES ============

@main_bp.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file upload and start processing"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '').strip()
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique job ID
            timestamp = str(int(time.time()))
            original_name = secure_filename(file.filename)
            job_id = f"{original_name.rsplit('.', 1)[0]}_{timestamp}"
            
            # Save uploaded file
            filename = f"{job_id}.{original_name.rsplit('.', 1)[1]}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process with AI
            if not current_app.config['GEMINI_API_KEY']:
                return jsonify({'error': 'Gemini API key not configured'}), 500
            
            # Extract and process
            processor = ProcessHandler(current_app.config['GEMINI_API_KEY'])
            result = processor.process_resume_and_jd(filepath, job_description)
            
            # Generate LaTeX
            generator = ResumeGenerator(current_app.config['GEMINI_API_KEY'])
            latex_code = generator.generate_latex(result)
            
            # Save LaTeX
            latex_path = os.path.join(current_app.config['PDF_FOLDER'], f'resume_{job_id}.tex')
            with open(latex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            # Try to generate PDF immediately
            pdf_generated = compile_latex_to_pdf(latex_path, job_id)
            
            return jsonify({
                'success': True,
                'job_id': job_id,
                'filename': original_name,
                'latex_preview': latex_code[:500] + '...' if len(latex_code) > 500 else latex_code,
                'pdf_generated': pdf_generated,
                'keywords_matched': len(result.get('keywords', [])),
                'message': 'Resume processed successfully'
            })
            
        except Exception as e:
            current_app.logger.error(f"Processing error: {str(e)}")
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT, TEX'}), 400

@main_bp.route('/api/latex/<job_id>', methods=['GET'])
def get_latex(job_id):
    """Get LaTeX source code"""
    try:
        # Try exact match first
        latex_path = os.path.join(current_app.config['PDF_FOLDER'], f'resume_{job_id}.tex')
        
        # If not found, search for partial match
        if not os.path.exists(latex_path):
            files = os.listdir(current_app.config['PDF_FOLDER'])
            matching = [f for f in files if job_id in f and f.endswith('.tex')]
            if matching:
                latex_path = os.path.join(current_app.config['PDF_FOLDER'], matching[0])
        
        if os.path.exists(latex_path):
            with open(latex_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'success': True,
                'latex': content,
                'job_id': job_id
            })
        else:
            return jsonify({'error': 'LaTeX file not found', 'job_id': job_id}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/generate-pdf/<job_id>', methods=['POST'])
def generate_pdf(job_id):
    """Compile LaTeX to PDF"""
    try:
        latex_path = os.path.join(current_app.config['PDF_FOLDER'], f'resume_{job_id}.tex')
        
        if not os.path.exists(latex_path):
            # Search for file
            files = os.listdir(current_app.config['PDF_FOLDER'])
            matching = [f for f in files if job_id in f and f.endswith('.tex')]
            if matching:
                latex_path = os.path.join(current_app.config['PDF_FOLDER'], matching[0])
            else:
                return jsonify({'error': 'LaTeX source not found'}), 404
        
        success = compile_latex_to_pdf(latex_path, job_id)
        
        if success:
            pdf_filename = f'resume_{job_id}.pdf'
            return jsonify({
                'success': True,
                'pdf_url': f'/static/pdfs/{pdf_filename}',
                'message': 'PDF generated successfully'
            })
        else:
            return jsonify({
                'error': 'PDF compilation failed',
                'message': 'Ensure pdflatex is installed on the server'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/files/<job_id>', methods=['GET'])
def check_files(job_id):
    """Check which files exist for a job"""
    pdf_folder = current_app.config['PDF_FOLDER']
    
    files = {
        'tex': False,
        'pdf': False,
        'cover_tex': False,
        'cover_pdf': False
    }
    
    # Check for resume files
    tex_files = [f for f in os.listdir(pdf_folder) if f.endswith('.tex')]
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    for f in tex_files:
        if job_id in f:
            if f.startswith('resume_'):
                files['tex'] = True
            elif f.startswith('cover_'):
                files['cover_tex'] = True
    
    for f in pdf_files:
        if job_id in f:
            if f.startswith('resume_'):
                files['pdf'] = True
            elif f.startswith('cover_'):
                files['cover_pdf'] = True
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'files': files
    })

@main_bp.route('/api/download/<job_id>', methods=['GET'])
def download_file(job_id):
    """Download generated file"""
    file_type = request.args.get('type', 'pdf')
    
    # Map file types to extensions and prefixes
    type_map = {
        'tex': ('resume_', '.tex'),
        'pdf': ('resume_', '.pdf'),
        'cover_tex': ('cover_', '.tex'),
        'cover_pdf': ('cover_', '.pdf'),
        'cover': ('cover_', '.pdf')
    }
    
    prefix, ext = type_map.get(file_type, ('resume_', '.pdf'))
    filename = f'{prefix}{job_id}{ext}'
    filepath = os.path.join(current_app.config['PDF_FOLDER'], filename)
    
    # If exact match not found, search
    if not os.path.exists(filepath):
        files = os.listdir(current_app.config['PDF_FOLDER'])
        matching = [f for f in files if job_id in f and f.endswith(ext) and f.startswith(prefix)]
        if matching:
            filepath = os.path.join(current_app.config['PDF_FOLDER'], matching[0])
            filename = matching[0]
    
    if os.path.exists(filepath):
        mimetype = 'application/pdf' if ext == '.pdf' else 'text/plain'
        return send_file(
            filepath,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    return jsonify({'error': 'File not found', 'filename': filename}), 404

@main_bp.route('/api/history', methods=['GET'])
def get_history():
    """Get generation history"""
    try:
        pdf_folder = current_app.config['PDF_FOLDER']
        files = []
        
        if os.path.exists(pdf_folder):
            for filename in os.listdir(pdf_folder):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(pdf_folder, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'filename': filename,
                        'job_id': filename.replace('resume_', '').replace('.pdf', '').replace('cover_', ''),
                        'created': stat.st_mtime,
                        'created_formatted': time.strftime('%Y-%m-%d %H:%M', time.localtime(stat.st_mtime)),
                        'size': stat.st_size,
                        'size_kb': round(stat.st_size / 1024, 1)
                    })
        
        # Sort by creation time, newest first
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'count': len(files),
            'files': files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/delete/<job_id>', methods=['DELETE'])
def delete_files(job_id):
    """Delete all files for a job"""
    try:
        pdf_folder = current_app.config['PDF_FOLDER']
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        deleted = []
        extensions = ['.tex', '.pdf', '.aux', '.log', '.out', '.synctex.gz']
        
        # Delete generated files
        for filename in os.listdir(pdf_folder):
            if job_id in filename:
                filepath = os.path.join(pdf_folder, filename)
                try:
                    os.remove(filepath)
                    deleted.append(filename)
                except Exception as e:
                    current_app.logger.error(f"Error deleting {filename}: {e}")
        
        # Delete uploaded source files
        for filename in os.listdir(upload_folder):
            if job_id in filename:
                filepath = os.path.join(upload_folder, filename)
                try:
                    os.remove(filepath)
                    deleted.append(filename)
                except Exception as e:
                    current_app.logger.error(f"Error deleting {filename}: {e}")
        
        return jsonify({
            'success': True,
            'deleted_count': len(deleted),
            'deleted_files': deleted,
            'job_id': job_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'gemini_configured': bool(current_app.config['GEMINI_API_KEY']),
        'upload_folder_exists': os.path.exists(current_app.config['UPLOAD_FOLDER']),
        'pdf_folder_exists': os.path.exists(current_app.config['PDF_FOLDER'])
    })

# ============ HELPER FUNCTIONS ============

def compile_latex_to_pdf(latex_path, job_id):
    """Compile LaTeX file to PDF"""
    try:
        pdf_folder = current_app.config['PDF_FOLDER']
        
        # Run pdflatex
        result = subprocess.run(
            [
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory', pdf_folder,
                latex_path
            ],
            capture_output=True,
            text=True,
            timeout=current_app.config.get('LATEX_TIMEOUT', 30)
        )
        
        # Check if PDF was created
        pdf_path = os.path.join(pdf_folder, f'resume_{job_id}.pdf')
        
        # Try alternative naming if not found
        if not os.path.exists(pdf_path):
            base_name = os.path.basename(latex_path).replace('.tex', '.pdf')
            alt_path = os.path.join(pdf_folder, base_name)
            if os.path.exists(alt_path):
                # Rename to standard format
                os.rename(alt_path, pdf_path)
        
        return os.path.exists(pdf_path)
        
    except subprocess.TimeoutExpired:
        current_app.logger.error("LaTeX compilation timed out")
        return False
    except FileNotFoundError:
        current_app.logger.error("pdflatex not found. Please install LaTeX.")
        return False
    except Exception as e:
        current_app.logger.error(f"LaTeX compilation error: {e}")
        return False