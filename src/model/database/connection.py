from functools import lru_cache

import settings

from pymongo import MongoClient
from pymongo.database import Database


@lru_cache(maxsize=None)
def get_client() -> MongoClient:
    mongo_client = MongoClient(settings.CONNECTION_STR)
    mongo_client.server_info()  # raises exception in case connection string is not valid
    return mongo_client


@lru_cache(maxsize=None)
def get_database() -> Database:
    return get_client().get_database(settings.DATABASE)
