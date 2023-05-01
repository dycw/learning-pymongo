from pymongo import ASCENDING, MongoClient
from itertools import islice
from typing import Any
from sys import stdout
from bson.objectid import ObjectId
from loguru import logger
import datetime as dt


# https://pymongo.readthedocs.io/en/stable/tutorial.html


logger.remove(0)
logger.add(stdout)


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
logger.info(f"{post_id=}")
logger.info(f"{db.list_collection_names()=}")
logger.info(f"{posts.find_one()=}")
logger.info(f"{posts.find_one(dict(author='Mike'))=}")
logger.info(f"{posts.find_one(dict(author='Eliot'))=}")
logger.info(f"{posts.find_one(dict(_id=post_id))=}")


def get(post_id: str, /) -> Any:
    return client["db"]["collection"].find_one(dict(_id=ObjectId(post_id)))


new_posts = [
    dict(
        author="Mike",
        text="Another post!",
        tags=["bulk", "insert"],
        date=dt.datetime(2009, 11, 12, 11, 14),
    ),
    dict(
        author="Eliot",
        title="MongoDB is fun",
        text="and pretty easy too",
        tags=["bulk", "insert"],
        date=dt.datetime(2009, 11, 10, 10, 45),
    ),
]
result = posts.insert_many(new_posts)
logger.info(f"{result.inserted_ids=}")


for post in islice(posts.find(), 5):
    logger.info(f"Querying for more than 1 document >>> {post=}")


for post in islice(posts.find(dict(author="Mike")), 5):
    logger.info(f"Querying for more than 1 document (Mike) >>> {post=}")


logger.info(f"{posts.count_documents({})=}")
logger.info(f"{posts.count_documents(dict(author='Mike'))=}")


d = dt.datetime(2009, 11, 12, 12)
for post in islice(posts.find(dict(date={"$lt": d})).sort("author"), 5):
    logger.info(f"Range queries: {post=}")


result = db["profiles"].create_index([("user_id", ASCENDING)], unique=True)
logger.info(f"{sorted(list(db['profiles'].index_information()))=}")


user_profiles = [dict(user_id=211, name="Luke"), dict(user_id=212, name="Ziltoid")]
result = db["profiles"].insert_many(user_profiles)
new_profile = dict(user_id=213, name="Drew")
duplicate_profile = dict(user_id=212, name="Tommy")
result = db["profiles"].insert_one(new_profile)
result = db["profiles"].insert_one(duplicate_profile)
