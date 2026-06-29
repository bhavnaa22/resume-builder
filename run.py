#!/usr/bin/env python3
"""
Taylrd - AI Resume Generator
Flask Backend Entry Point
"""

import os
import sys

# Ensure apps module is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps import create_app

def setup_directories(app):
    """Ensure all required directories exist"""
    directories = [
        app.config['UPLOAD_FOLDER'],
        app.config['PDF_FOLDER'],
        os.path.join(app.config['STATIC_FOLDER'], 'css'),
        os.path.join(app.config['STATIC_FOLDER'], 'js'),
        os.path.join(app.config['STATIC_FOLDER'], 'images')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Ensured directory exists: {directory}")

def check_dependencies():
    """Check if required external dependencies are available"""
    import subprocess
    
    dependencies = {
        'pdflatex': 'LaTeX compiler (required for PDF generation)'
    }
    
    missing = []
    for cmd, description in dependencies.items():
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print(f"✓ Found: {cmd}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(f"{cmd} ({description})")
            print(f"✗ Missing: {cmd} - {description}")
    
    if missing:
        print("\n⚠️  Warning: Some dependencies are missing:")
        for m in missing:
            print(f"   - {m}")
        print("\nTo install LaTeX:")
        print("  Ubuntu/Debian: sudo apt-get install texlive-full")
        print("  MacOS: brew install --cask mactex")
        print("  Windows: Install MiKTeX or TeX Live")

def main():
    """Main entry point"""
    print("=" * 50)
    print("Taylrd - AI Resume Generator")
    print("=" * 50)
    
    # Create app
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    print(f"\nConfiguration: {config_name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    
    # Setup
    setup_directories(app)
    check_dependencies()
    
    # Check API key
    if not app.config['GEMINI_API_KEY']:
        print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
        print("   AI features will not work.")
        print("   Set it in your .env file: GEMINI_API_KEY=your_key_here")
    else:
        print("\n✓ Gemini API key configured")
    
    # Run
    print("\n" + "=" * 50)
    print(f"Starting server on http://{app.config['HOST']}:{app.config['PORT']}")
    print("=" * 50 + "\n")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

if __name__ == '__main__':
    main()