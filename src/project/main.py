from pymongo import MongoClient
from loguru import logger
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


posts = db["posts"]
post_id = posts.insert_one(post).inserted_id
print(post_id)
