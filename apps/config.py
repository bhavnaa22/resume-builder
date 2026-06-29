import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.join(basedir, '..')
load_dotenv(os.path.join(parent_dir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or "xxxxxx"
    
    BASE_DIR = basedir
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    PDF_FOLDER = os.path.join(STATIC_FOLDER, 'pdfs')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'tex'}
    
    # CHANGE THIS - Use 127.0.0.1 instead of 0.0.0.0
    HOST = os.environ.get('HOST') or '127.0.0.1'
    PORT = int(os.environ.get('PORT') or 5001)
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}