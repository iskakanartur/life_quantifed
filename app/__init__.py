from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

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

    # Register blueprint
    from app.views import bp as main_bp
    app.register_blueprint(main_bp)

    # Import models to create database tables
    from app import models

    with app.app_context():
        db.create_all()

    return app
