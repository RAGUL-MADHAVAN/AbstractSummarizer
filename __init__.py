import os
from datetime import datetime, timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .config import config
from transformers import pipeline

# Import extensions from models (which includes the user_loader)
from .models import db, login_manager, csrf

# Configure login manager (this is the same instance from models.py)
login_manager.login_view = 'auth.login'


def _register_jinja_filters(app: Flask):
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%Y-%m-%d %H:%M'):
        if not value:
            return ''
        return value.strftime(format)

    @app.template_filter('timesince')
    def timesince(value):
        if not value:
            return ''
        now = datetime.utcnow()
        diff = now - value
        if diff < timedelta(minutes=1):
            return 'just now'
        elif diff < timedelta(hours=1):
            mins = diff.seconds // 60
            return f"{mins} min ago"
        elif diff < timedelta(days=1):
            hrs = diff.seconds // 3600
            return f"{hrs} hr ago"
        else:
            days = diff.days
            return f"{days} day{'s' if days != 1 else ''} ago"


def create_app(config_name='default'):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Init extensions (these are already created in models.py)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Ensure folders
    os.makedirs(os.path.join(app.root_path, 'static', 'downloads'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'img'), exist_ok=True)

    # Register filters
    _register_jinja_filters(app)

    # Import models to register user_loader
    from .models import User, Summary

    # Register blueprints
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .summarizer import summarizer as summarizer_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(summarizer_blueprint, url_prefix='/summarizer')

    # Global context variables for all templates
    @app.context_processor
    def inject_globals():
        return {
            'now': datetime.utcnow(),
        }

    # Create tables
    with app.app_context():
        db.create_all()

    # Initialize summarization pipeline once
    try:
        if not hasattr(app, 'summarizer'):
            app.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        # Defer model loading errors until first use; log minimal info
        app.logger.warning(f"Summarizer pipeline init deferred: {e}")

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return app.send_static_file('errors/404.html') if os.path.exists(os.path.join(app.static_folder, 'errors/404.html')) else ("404 Not Found", 404)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return app.send_static_file('errors/500.html') if os.path.exists(os.path.join(app.static_folder, 'errors/500.html')) else ("500 Internal Server Error", 500)

    return app
