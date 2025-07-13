from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL= os.getenv("BASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
TOKEN = os.getenv("TOKEN")


USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

DB_URL = os.getenv("DB_URL")

AUTH_URL = os.getenv("AUTH_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_SECRET = os.getenv("AUTH_SECRET")
