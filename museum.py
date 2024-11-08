import requests
import random
import string

ROOT_URL = "https://collectionapi.metmuseum.org"
N_DEPARTMENTS = 21

def get_art_object(objectID=45734):
    """
    takes a unique object ID as input 
    returns an art object in json format
    returns None if object ID is invalid
    """
    
    url = ROOT_URL + f"/public/collection/v1/objects/{objectID}"

    art_object = requests.get(url)

    # if the art object is found
    if art_object.status_code == 200:
        return art_object.json()

    # else return None object
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


def get_random_object_with_image_ID():
    """
    returns the ID of a random object with an image
    """

    objects_with_images = get_objects_with_images()
    # get the total number of objects
    n_objects = objects_with_images["total"]

    # choose a random art piece within range
    n = random.randint(0, n_objects - 1)
    objectID = objects_with_images["objectIDs"][n]

    return objectID


if __name__ == "__main__":
    print("\n*** Welcome to the Hyperlink Metropolitan Museum ***\n")

