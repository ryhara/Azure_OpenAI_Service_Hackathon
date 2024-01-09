import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")