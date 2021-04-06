from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
mail = Mail()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    # Run the configurations to setup the URIs 
    # before initializing the db and other variables
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    mail.init_app(app)

    with app.app_context():
        # Imports
        from . import serve
        # Initialize Global db
        db.create_all()

        return app

