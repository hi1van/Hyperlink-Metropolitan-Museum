from flask import Flask, render_template, request, redirect
from waitress import serve
from museum import *
import random

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    
    return render_template("index.html")

@app.route('/hyperMuseum')
def hyperMuseum():

    objects = get_objects_with_images()
    n_objects = objects["total"]

    n = random.randint(0, n_objects - 1)
    objectID = objects["objectIDs"][n]

    art_object = get_art_object(objectID)

    if not art_object or "primaryImageSmall" not in art_object:
        return "Image not found", 404

    image = art_object["primaryImageSmall"]
    
    return render_template(
        "hyperMuseum.html",
        image = image
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)