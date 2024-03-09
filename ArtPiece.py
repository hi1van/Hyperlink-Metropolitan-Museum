ROOT_URL = "https://collectionapi.metmuseum.org"

def get_object(objectID):
    
    url = ROOT_URL + f"/public/collection/v1/objects/{objectID}"

    return url

# takes departments as an array of integers, if no department is specified, return all
def get_objects(departments=None):

    url = ROOT_URL + "/public/collection/v1/objects"

    if not departments:
        return url
    
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

    return url

print(get_objects())


