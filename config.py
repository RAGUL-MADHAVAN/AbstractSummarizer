import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///summarizer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN', '')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv'}
    
    @staticmethod
    def init_app(app):
        # Ensure upload folder exists
        os.makedirs(os.path.join(app.root_path, 'static', Config.UPLOAD_FOLDER), exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
