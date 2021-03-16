from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app():
    """Construct the core application."""
    app = Flask( __name__ )
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    app.config.from_object('config.Config')

    with app.app_context():
        # Imports
        from . import serve
        # Initialize Global db
        db.create_all()

        return app


