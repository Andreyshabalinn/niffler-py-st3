from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL= os.getenv("BASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
TOKEN = os.getenv("TOKEN")


USERNAME = os.getenv("TEST_LOGIN")
PASSWORD = os.getenv("TEST_PASSWORD")

DB_URL = os.getenv("DB_URL")
USER_DB_URL = os.getenv("USER_DB_URL")

AUTH_URL = os.getenv("BASE_AUTH_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_SECRET = os.getenv("AUTH_SECRET")

KAFKA_SERVER = os.getenv("SERVER_NAME")

SOAP_ADDRESS = os.getenv("SOAP_ADDRESS")

WIREMOCK_HOST = "localhost:8094"
CURRENCY_HOST = "localhost:8092"
 