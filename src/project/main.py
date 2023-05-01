from pymongo import MongoClient
import datetime as dt


client = MongoClient()
db = client["test_database"]
collection = db["test_collection"]


post = dict(
    author="Mike",
    text="My first blog post!",
    tags=["mongodb", "python", "pymongo"],
    date=dt.datetime.utcnow(),
)
