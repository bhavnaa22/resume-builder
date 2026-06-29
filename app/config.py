import os
from dotenv import load_dotenv

# Get the base directory (apps folder)
basedir = os.path.abspath(os.path.dirname(__file__))

# Load .env from parent directory (root)
parent_dir = os.path.join(basedir, '..')
load_dotenv(os.path.join(parent_dir, '.env'))

class Config:
    """Base configuration"""
    
    # 🔑 YOUR GEMINI API KEY - Option 1: From .env file
    # Option 2: Replace directly here: GEMINI_API_KEY = "xxxxxx"
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or "xxxxxx"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Paths
    BASE_DIR = basedir
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    PDF_FOLDER = os.path.join(STATIC_FOLDER, 'pdfs')
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'tex'}
    
    # Server settings
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}