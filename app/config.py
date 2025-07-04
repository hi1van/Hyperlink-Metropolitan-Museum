import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class Config:
    # for PostgreSQL
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getenv('SQLITE_DB_PATH')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')