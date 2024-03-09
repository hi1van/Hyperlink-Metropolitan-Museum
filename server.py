from flask import Flask, render_template, request, redirect
from waitress import serve
from museum import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    
    return render_template("index.html")

@app.route('/hyperMuseum')
def hypermuseum():
    art_object = get_art_object(45734)

    if not art_object or "primaryImage" not in art_object:
        return "Image not found", 404

    image = art_object["primaryImage"]
    
    return redirect(image)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)