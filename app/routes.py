from flask import render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from . import db
from .models import User
from .museum import *
from .artObject import *

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    """
    Landing page
    """
    return render_template("index.html")

@main.route('/hyperMuseum')
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

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)
        db.session.add(new_user)

        try:
            db.session.commit()
        except SQLAlchemy.exc.IntegrityError as e:
            if 'unique constraint' in str(e):
                return "Username already exists. Please choose a different one.", 400

        return f"User {username} added successfully!"
    
    return '''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            <input type="submit" value="Add User">
        </form>
    '''