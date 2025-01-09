from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from waitress import serve
from museum import *
from artObject import *

app = Flask(__name__)
load_dotenv()

# configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
@app.route('/index')
def index():
    """
    Landing page
    """
    return render_template("index.html")

@app.route('/hyperMuseum')
def hyperMuseum():
    """
    Renders an art display page
    """

    objectID = get_random_object_with_image_ID()
    art_object = get_art_object(objectID)

    # invalid return object
    if not art_object or "primaryImageSmall" not in art_object:
        return "Image not found", 404
    
    art_object = artObject(art_object)
    
    return render_template(
        "hyperMuseum.html",
        image = art_object.image,
        artist = art_object.artist,
        artist_bio = art_object.artist_bio,
        artwork_date = art_object.artwork_date,
        medium = art_object.medium,
        dimensions = art_object.dimensions,
        department = art_object.department,
        object_name = art_object.object_name,
        title = art_object.title,
        period = art_object.period,
    )

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)
        db.session.add(new_user)

        try:
            db.session.commit()
            return f"User {username} added successfully!"
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return "Username already exists. Please choose a different one.", 400
            else:
                return f"An unexpected error occurred: {e}", 500
    
    return '''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            <input type="submit" value="Add User">
        </form>
    '''

# create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)