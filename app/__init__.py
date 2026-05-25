from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint)
    
    return app
