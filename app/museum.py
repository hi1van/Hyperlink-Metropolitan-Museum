import requests
import random
import string
from .config import Config
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from .models import Art

ROOT_URL = "https://collectionapi.metmuseum.org" # MET API
N_DEPARTMENTS = 21
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

def get_art_object():
    """
    returns a random Art object with an image in json format
    returns None if unsuccessful
    """

    # only retrieve objects with images for display
    # CHANGE: store this data in db to reduce computation
    objects_with_images = get_objects_with_images()

    # first search for an art object stored in the database
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # set a search limit to avoid time out
    loop_limit = 10
    loop_counter = 0

    # retrieve objects until one with an image is found
    # (some objects in the API described as hasImage don't have a primary image oddly)
    while loop_counter < loop_limit:
        loop_counter += 1

        # select an object randomly
        objectID = get_random_object_with_image_ID(objects_with_images)
        
        # query to fetch the art object with given objectID
        art_object = session.query(Art).filter(Art.objectID == objectID).first()

        if art_object:
            # doesn't have a link, try again
            if len(art_object.primaryImage) == 0:
                continue

            session.close()
            print("Object retrieved via the database")
            return art_object
        else:
            # fall back - query the API and add to the database
            url = ROOT_URL + f"/public/collection/v1/objects/{objectID}"

            art_object = requests.get(url)

            # if the art object is found add to database and return
            if art_object.status_code == 200:
                art_object = art_object.json()

                # doesn't have a link, try again
                if len(art_object["primaryImageSmall"]) == 0:
                    continue
                
                # create new art instance to add to the db and return
                art_instance = Art(objectID=art_object["objectID"], primaryImage=art_object["primaryImageSmall"], \
                                artist=art_object["artistDisplayName"], artist_bio=art_object["artistDisplayBio"], \
                                artwork_date=art_object["objectDate"], medium=art_object["medium"], \
                                dimensions=art_object["dimensions"], department=art_object["department"], \
                                object_name=art_object["objectName"], title=art_object["title"], \
                                period=art_object["period"])
                
                session.add(art_instance)
                session.commit()
                session.close()

                return art_instance

    session.close()

    # return None object if unsuccessful
    return None


def get_objects(departments=None):
    """
    takes an array of departmentID(s) as input
    returns all objects in the specified departments
    returns all objects if no department/no valid department is given
    """

    url = ROOT_URL + "/public/collection/v1/objects"

    # if no department is specified then just return all
    if not departments:
        objects = requests.get(url)
        return objects.json()
    
    first = True
    i = 0
    while i < len(departments):
        # not a valid departmentId
        if departments[i] <= 0 or departments[i] > N_DEPARTMENTS:
            i += 1
            continue

        if first:
            url = url + f"?departmentIds={departments[i]}"
            first = False
        
        else:
            url = url + f"|{departments[i]}"

        i += 1

    objects = requests.get(url)

    return objects.json()


def get_objects_with_images():
    """
    returns objects with images in json format using a random query letter
    """

    url = ROOT_URL + "/public/collection/v1/search?hasImages=true&isHighlight=true&q="

    # url must inlude a query to be able to go through, so choose any random letter to add as the query
    letter = random.choice(string.ascii_lowercase)
    url = url + letter

    objects = requests.get(url)
    return objects.json()


def get_random_object_with_image_ID(objects_with_images):
    """
    returns the ID of a random object with an image
    """

    # get the total number of objects
    n_objects = objects_with_images["total"]

    # choose a random art piece within range
    n = random.randint(0, n_objects - 1)
    objectID = objects_with_images["objectIDs"][n]

    return objectID


if __name__ == "__main__":
    print("\n*** Welcome to the Hyperlink Metropolitan Museum ***\n")

