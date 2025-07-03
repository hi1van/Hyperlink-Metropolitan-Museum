from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate

# create global SQLAlchemy object
db = SQLAlchemy()

def create_app():
    """ 
    factory function which creates and returns a new Flask instance
    """

    app = Flask(__name__)

    # load application configurations
    app.config.from_object(Config) 

    # bind the SQLAlchemy db object to the Flask app
    db.init_app(app)
    
    from .models import User
    from .models import Art
    migrate = Migrate(app, db)
    
    # register the blueprint to make routes part of the app
    from .routes import main
    app.register_blueprint(main)

    return app