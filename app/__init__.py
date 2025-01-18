from flask import Flask
from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.DevelopmentConfig")

    # Initialize extensions like database
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app