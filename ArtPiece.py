ROOT_URL = "https://collectionapi.metmuseum.org"

def get_object(objectID):
    
    url = ROOT_URL + f"/public/collection/v1/objects/{objectID}"

    return url

# takes departments as an array of integers, if no department is specified, return all
def get_objects(departments):

    url = ROOT_URL + "/public/collection/v1/objects"

    if not departments:
        return url
    
    for i in range(len(departments)):
        if i == 0:
            url = url + f"?departmentIds={departments[i]}"

        else:
            url = url + f"|{departments[i]}"

    return url


print(get_objects([3,4, 5]))



