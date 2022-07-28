import collections
from pymongo import MongoClient
from NotesParse import parseNotes

def pushToAtlas(notesList,atlasuri):
    client = MongoClient(atlasuri)
    db = client.get_database("BooksNotes")
    for x in notesList:
        if db.get_collection(x["from"]) == None:
            tmp = db.create_collection(x["from"])
            tmp.create_index("content")
        collections = db.get_collection(x["from"])
        collections.insert_one(x)
