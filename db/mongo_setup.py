# db/mongo_setup.py
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# database name
db = client["gi_marketplace"]

def get_db():
    return db
