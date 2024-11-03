from flask import Flask, render_template, request, redirect
from waitress import serve
from museum import *
from artObject import *

app = Flask(__name__)

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

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)