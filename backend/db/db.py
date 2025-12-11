from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

print("MONGO_URI loaded:", bool(mongo_uri))
print("DB_NAME loaded:", db_name)

try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    print("Connected to MongoDB successfully!")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("Error connecting to MongoDB:", e)
