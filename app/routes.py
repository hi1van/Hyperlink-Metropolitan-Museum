from flask import render_template, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import db
from .models import User
from .museum import *
from math import ceil

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

    art_object = get_art_object()

    # invalid return object
    if art_object is None:
        return "Object not found", 404  
    
    return render_template(
        "hyperMuseum.html",
        image = art_object.primaryImage,
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

@main.route('/browse/departments')
def browse_departments():

    # gather all available distinct departments
    departments = [row[0] for row in Art.query.with_entities(Art.department).distinct().all()]

    return render_template(
        "browse_departments.html",
        departments=departments
    )

@main.route('/api/departments/<department>/artworks')
def get_department_artworks(department):

    # parameters for pagination
    page = int(request.args.get('page', 1))
    per_page = 15

    # query artworks for the specified department
    total_artworks = Art.query.filter_by(department=department).count()
    artworks = Art.query.filter_by(department=department) \
                        .offset((page - 1) * per_page) \
                        .limit(per_page) \
                        .all()
    
    # prepare data to return
    artwork_data = [
        {
            "id": artwork.objectID,
            "title": artwork.title,
            "image": artwork.primaryImage,
            "artist": artwork.artist
        } for artwork in artworks
    ]

    total_pages = ceil(total_artworks / per_page)

    return jsonify({
        "artworks": artwork_data,
        "total_pages": total_pages,
        "current_page": page
    })

@main.route('/artwork/<objectID>')
def get_artwork(objectID):

    artwork = Art.query.filter_by(objectID=objectID).first()

    # invalid return object
    if artwork is None:
        return "Object not found", 404  
    
    return render_template(
        "artwork.html",
        image = artwork.primaryImage,
        artist = artwork.artist,
        artist_bio = artwork.artist_bio,
        artwork_date = artwork.artwork_date,
        medium = artwork.medium,
        dimensions = artwork.dimensions,
        department = artwork.department,
        object_name = artwork.object_name,
        title = artwork.title,
        period = artwork.period,
    )


# @main.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     if request.method == 'POST':
#         username = request.form['username']
#         new_user = User(username=username)
#         db.session.add(new_user)

#         try:
#             db.session.commit()
#         except SQLAlchemy.exc.IntegrityError as e:
#             if 'unique constraint' in str(e):
#                 return "Username already exists. Please choose a different one.", 400

#         return f"User {username} added successfully!"
    
#     return '''
#         <form method="POST">
#             Username: <input type="text" name="username"><br>
#             <input type="submit" value="Add User">
#         </form>
#     '''