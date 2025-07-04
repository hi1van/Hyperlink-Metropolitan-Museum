from flask import render_template, request, Blueprint, jsonify, session
import google.generativeai as genai
import requests
from flask_sqlalchemy import SQLAlchemy
from . import db
from .models import User
from .museum import *
from math import ceil
from .config import Config
from io import BytesIO
from PIL import Image

main = Blueprint('main', __name__)
genai.configure(api_key=Config.GEMINI_API_KEY)

@main.route('/')
@main.route('/index')
def index():
    """
    renders the landing page
    """
    return render_template("index.html")

@main.route('/hyperMuseum')
def hyperMuseum():
    """
    renders an art display page with a random art object
    """

    # get the art object to be displayed
    art_object = get_art_object()

    # invalid return object
    if art_object is None:
        return jsonify({"error": "Object not found"}), 404
    
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
    """
    renders a page to browse available departments of the MET
    """

    # gather all available distinct departments from the db
    departments = [row[0] for row in Art.query.with_entities(Art.department).distinct().all()]

    return render_template(
        "browse_departments.html",
        departments=departments
    )

@main.route('/api/departments/<department>/artworks')
def get_department_artworks(department):
    """
    returns all artworks in a given department in json form
    """

    # parameters for pagination
    page = int(request.args.get('page', 1))
    PER_PAGE = 15

    # query artworks for the specified department
    total_artworks = Art.query.filter_by(department=department).distinct(Art.objectID).count()
    artworks = Art.query.filter_by(department=department) \
                        .distinct(Art.objectID) \
                        .offset((page - 1) * PER_PAGE) \
                        .limit(PER_PAGE) \
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

    total_pages = ceil(total_artworks / PER_PAGE)

    return jsonify({
        "artworks": artwork_data,
        "total_pages": total_pages,
        "current_page": page
    })

@main.route('/artwork/<objectID>')
def get_artwork(objectID):
    """
    renders an artwork page for the specified ID
    """

    artwork = Art.query.filter_by(objectID=objectID).first()

    # invalid return object
    if artwork is None:
        return jsonify({"error": "Object not found"}), 404
    
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

@main.route('/browse/popular_artists')
def browse_popular_artists():
    """
    renders a page to browse select popular artists featured at the MET
    """

    # gather all available distinct departments
    POPULAR_ARTISTS = ["Vincent van Gogh", "Leonardo da Vinci", "Rembrandt (Rembrandt van Rijn)", "Johannes Vermeer", 
                       "Caravaggio (Michelangelo Merisi)", "Joseph Mallord William Turner", "Auguste Renoir",
                       "Camille Pissarro"]
    
    # FOR TESTING:
    # all_artists = [row[0] for row in Art.query.with_entities(Art.artist).distinct().all()]

    return render_template(
        "browse_popular_artists.html",
        artists=POPULAR_ARTISTS
    )

@main.route('/api/chat', methods=['POST'])
def artwork_chat():
    """
    accepts json input from the frontend
    feeds in user input and returns model's response
    """
    
    # extract user input and context info from the request body
    user_message = request.json.get("message")
    artwork_title = request.json.get("artwork_title") 
    artist_name = request.json.get("artist_name")
    medium = request.json.get("medium")
    image_url = request.json.get("image_url") 

    # reply in case of empty message
    if not user_message:
        return jsonify({"response": "Please ask a question!"})

    # track and add to chat history in the FLask session
    chat_history = session.get("chat_history", [])
    chat_history.append({"role": "user", "parts": user_message})
    session["chat_history"] = chat_history

    try:
        # open image for Gemini
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # set up Gemini model
        # TODO refine the model's prompt for better structured responses
        model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=f"""You are an AI chatbot named August, acting as a guide at the Hyperlink Metropolitan Museum which
                                        features artworks from the Metropolitan Museum in New York City. Answer questions as an expert art
                                        historian, staying relevant to this artwork or the MET museum.
                                        Avoid speculation and stick to factual information.
                                        Aim for concise answers, which don't involve language which is too complex for the
                                        average art-enjoyer unless thorough discussion is desired."""
                )

        chat = model.start_chat(history=session["chat_history"])

        # add to the model's metadata for better responses
        context = f"""The user is viewing the artwork '{artwork_title}' by {artist_name}. The medium used is {medium}."""
        prompt = f"""The user's message is: {user_message}
                    Context: {context} The image is of the artwork."""

        # generate response
        response = chat.send_message([prompt, image])

        # add response to chat history
        chat_history.append({"role": "model", "parts": response.text})
        session["chat_history"] = chat_history

        # return the model's response
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "Sorry! There was an error processing your message. Please ask me again!"})
    

@main.route('/api/popular_artists/<artist>/artworks')
def get_popular_artist_artworks(artist):
    """
    returns all artworks of a given artist in json form
    """

    # parameters for pagination
    page = int(request.args.get('page', 1))
    per_page = 15

    # query artworks for the specified artist
    total_artworks = Art.query.filter_by(artist=artist).distinct(Art.objectID).count()
    artworks = Art.query.filter_by(artist=artist) \
                        .distinct(Art.objectID) \
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
