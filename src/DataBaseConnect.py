from webbrowser import BackgroundBrowser
from pymongo import IndexModel, MongoClient,collation
import pymongo
from NotesParse import parseNotes
from hashlib import md5

def pushToAtlas(notesList,atlasuri):
    client = MongoClient(atlasuri)
    db = client.get_database("BooksNotes")
    if db.get_collection(notesList[0]["from"]) == None:
        tmp = db.create_collection(notesList[0]["from"])
    collections = db.get_collection(notesList[0]["from"])
    for x in notesList:
        x["contenthash"] = md5(x["content"].encode('utf-8')).hexdigest()
        collections.find_one_and_update({"contenthash":x["contenthash"]},{"$set":x},upsert=True)
    collections.create_index([("contenthash",pymongo.ASCENDING)],unique=True,name="contenthash")
    
def pushToAtlasMyFavorite(notesList,atlasuri):
    client = MongoClient(atlasuri)
    db = client.get_database("FavoriteNotes")
    collations = db.get_collection("FavoriteNotes")
    for x in notesList:
        x["contenthash"] = md5(x["content"].encode('utf-8')).hexdigest()
        collations.find_one_and_update({"contenthash":x["contenthash"]},{"$set":x},upsert=True)
    collations.create_index([("contenthash",pymongo.ASCENDING)],unique=True,name="contenthash")