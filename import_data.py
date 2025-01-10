import ssl
import certifi
import aiohttp
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Art
from app.config import Config


HAS_IMAGES_QUERY_ROOT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isHighlight=true&q="
OBJECT_ID_ROOT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
ssl_context = ssl.create_default_context(cafile=certifi.where())

async def fetch_art_data(session, objectID):
    """ returns the art data for a given objectID """
    async with session.get(OBJECT_ID_ROOT_URL + str(objectID)) as art_object:
        if art_object.status == 200:
            return await art_object.json()
        else:
            print(f"Failed to retrieve art details for objectID {objectID}: {art_object.status}")
        return None

async def import_data(batch_size=1000):

    query_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    batch = []
    batch_counter = 0

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    db_session = Session()

    # for non-blocking http requests
    async with aiohttp.ClientSession() as session_requests:
    
        # only import art with images going through each char for query results
        for char in query_chars:
            print(f"Now importing art for query {char}")

            # retrieve all objectIDs for a given query
            response = await session_requests.get(HAS_IMAGES_QUERY_ROOT_URL + char, ssl=ssl_context)
            
            if response.status == 200:
                objects = await response.json()
                
                tasks = []
                # objectIDs retrieved, add to tasks to add to the db_session
                for objectID in objects["objectIDs"]:
                    tasks.append(fetch_art_data(session_requests, objectID))

                # gather the art data for each objectID
                results = await asyncio.gather(*tasks)

                for art_object in results:
                    if art_object:
                        art_instance = Art(objectID=art_object["objectID"], primaryImage=art_object["primaryImageSmall"], \
                                            artist=art_object["artistDisplayName"], artist_bio=art_object["artistDisplayBio"], \
                                            artwork_date=art_object["objectDate"], medium=art_object["medium"], \
                                            dimensions=art_object["dimensions"], department=art_object["department"], \
                                            object_name=art_object["objectName"], title=art_object["title"], \
                                            period=art_object["period"])
                        
                    batch.append(art_instance)

                    if len(batch) >= batch_size:
                        db_session.add_all(batch)
                        db_session.commit()
                        batch = []

                        batch_counter += 1
                        print(f"Batch number {batch_counter} complete")
                
            else:
                print(f"Failed to retrieve data: {response.status}")

        if batch:
            db_session.add_all(batch)
            db_session.commit()

    db_session.close()
    print("Import complete")

    return


if __name__ == "__main__":
    asyncio.run(import_data())
