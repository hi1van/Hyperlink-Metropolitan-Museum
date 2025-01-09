from waitress import serve
from app import create_app, db

app = create_app()

# create database tables if they don't exist
with app.app_context():
    db.create_all

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)