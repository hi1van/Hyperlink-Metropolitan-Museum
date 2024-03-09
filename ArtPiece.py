import requests

ROOT_URL = "https://collectionapi.metmuseum.org"

# returns object
def get_object(objectID):
    
    url = ROOT_URL + f"/public/collection/v1/objects/{objectID}"

    object = requests.get(url)

    if object.status_code == 200:
        return object
    else:
        return None

# returns all objects in specified departments
# takes departments as an array of integers, if no department is specified, return all
def get_objects(departments=None):

    url = ROOT_URL + "/public/collection/v1/objects"

    if not departments:
        objects = requests.get(url)
        return objects
    
    first = 1
    i = 0
    while i < len(departments):
        # not a valid departmentId
        if departments[i] < 1 or departments[i] > 21:
            i += 1
            continue

        if first:
            url = url + f"?departmentIds={departments[i]}"
            first = 0
        
        else:
            url = url + f"|{departments[i]}"

        i += 1

    objects = requests.get(url)
    return objects



