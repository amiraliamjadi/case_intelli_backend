from flask import Flask
from .extensions import db
from .routes import main
from .routes import register_routes
from flask_migrate import Migrate


def create_app():

    app = Flask(__name__, template_folder="templates")

    # Configuration for SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///m_sqlite.db'
    # Optional: Suppress warnings about SQLAlchemy's track modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions like database
    db.init_app(app)

    # Initialize Migrate
    migrate = Migrate(app, db)

    # Register routes
    register_routes(app)


    # Register Blueprints for routes
    app.register_blueprint(main)

    return app