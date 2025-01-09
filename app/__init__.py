from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    from .models import User
    from .models import Art
    migrate = Migrate(app, db)
    
    from .routes import main
    app.register_blueprint(main)

    return app