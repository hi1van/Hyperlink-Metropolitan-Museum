class artObject:

    def __init__(self, art_object):
        self.image = art_object["primaryImageSmall"]
        self.artist = art_object["artistDisplayName"]
        self.artist_bio = art_object["artistDisplayBio"]
        self.artwork_date = art_object["objectDate"]
        self.medium = art_object["medium"]
        self.dimensions = art_object["dimensions"]
        self.department = art_object["department"]
        self.object_name = art_object["objectName"]
        self.title = art_object["title"]
        self.period = art_object["period"]