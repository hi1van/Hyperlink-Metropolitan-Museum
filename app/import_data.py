import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Art
from .config import Config

HAS_IMAGES_QUERY_ROOT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isHighlight=true&q="
OBJECT_ID_ROOT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"


def import_data(batch_size=1000):

    query_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    batch = []

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # only import art with images
    for char in query_chars:
        print(f"Now importing art for query {char}")
        
        response = requests.get(HAS_IMAGES_QUERY_ROOT_URL + char)
        
        if response.status_code == 200:
            objects = response.json()

            # objects retrieved, add to session
            for objectID in objects["objectIDs"]:
                art_object = requests.get(OBJECT_ID_ROOT_URL + objectID)
                if art_object.status_code == 200:

                    art_instance = Art(objectID=art_object["objectID"], primaryImage=art_object["primaryImageSmall"], \
                                        artist=art_object["artistDisplayName"], artist_bio=art_object["artistDisplayBio"], \
                                        artwork_date=art_object["objectDate"], medium=art_object["medium"], \
                                        dimensions=art_object["dimensions"], department=art_object["department"], \
                                        object_name=art_object["objectName"], title=art_object["title"], \
                                        period=art_object["period"])
                    
                    batch.append(art_instance)

                    if len(batch) >= batch_size:
                        session.add_all(batch)
                        session.commit()
                        batch = []

                else:
                    print(f"Failed to retrieve art details for objectID {objectID}: {art_object.status_code}")
            
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    if batch:
        session.add_all(batch)
        session.commit()

    session.close()

    return


if __name__ == "__main__":
    import_data()
