from flask import Flask
from flask_cors import CORS
import os

def create_app(config_name='default'):
    # Get the absolute path to the apps directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static'),
        static_url_path='/static'
    )
    
    # Load configuration
    from apps.config import config
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Create directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from apps.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app