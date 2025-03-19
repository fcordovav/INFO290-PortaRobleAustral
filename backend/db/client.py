from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")


db_client = MongoClient(DB_CONNECTION_STRING, server_api=ServerApi('1'))
db = [DB_NAME]


try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)