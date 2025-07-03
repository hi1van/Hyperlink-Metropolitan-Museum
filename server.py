from app import create_app, db
from flask_migrate import Migrate
from datetime import timedelta
import os

# create Flask application instance
app = create_app()
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # user session time limit

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)