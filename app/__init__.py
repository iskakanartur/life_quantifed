from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Load configuration based on environment
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    elif os.getenv('FLASK_ENV') == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        # Default configuration for development
        app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprint
    from .views import bp as main_bp  # Adjusted to relative import
    app.register_blueprint(main_bp)

    # Import models to create database tables
    from . import models  # Adjusted to relative import

    with app.app_context():
        db.create_all()

    return app
