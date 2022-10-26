from hashlib import md5

import pymongo
from pymongo import MongoClient


def push_to_atlas(notes_list, atlas_uri):
    client = MongoClient(atlas_uri)
    db = client.get_database("BooksNotes")
    if db.get_collection(notes_list[0]["from"]) is None:
        pass
    collections = db.get_collection(notes_list[0]["from"])
    for x in notes_list:
        x['contenthash'] = md5(x["content"].encode('utf-8')).hexdigest()
        collections.find_one_and_update({"contenthash": x["contenthash"]}, {"$set": x}, upsert=True)
    collections.create_index([("contenthash", pymongo.ASCENDING)], unique=True, name="contenthash")


def push_to_atlas_my_favorite(notes_list, atlas_uri):
    client = MongoClient(atlas_uri)
    db = client.get_database("FavoriteNotes")
    collations = db.get_collection("FavoriteNotes")
    for x in notes_list:
        x["contenthash"] = md5(x["content"].encode('utf-8')).hexdigest()
        collations.find_one_and_update({"contenthash": x["contenthash"]}, {"$set": x}, upsert=True)
    collations.create_index([("contenthash", pymongo.ASCENDING)], unique=True, name="contenthash")
