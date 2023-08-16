"""
adbm

Interface with MongoDB, loads JSON files,
and inserts them into a database.

Noah Stieler, 2023
"""

import pymongo
import os
import json

client = None
db_name = ''

serverSelectionTimeoutMS = 1000


def db_operation(func):
    def wrapped(*args, **kwargs):
        return_val = None
        try:
            return_val = func(*args, **kwargs)
        except pymongo.errors.ConnectionFailure as e:
            print(e)
            exit()

        return return_val

    return wrapped


def connect(uri: str) -> None:
    global client
    client = pymongo.MongoClient(uri,
                                 serverSelectionTimeoutMS=serverSelectionTimeoutMS)


def insert_recursive(path: str, collection_name: str) -> list:
    """Recursively searches all sub-folders and inserts all found
    JSON files."""
    doc_ids = []

    for item in os.scandir(path):
        if item.is_dir():
            doc_ids += insert_recursive(os.path.join(path, item), collection_name)

    # Insert all JSON files in this directory
    doc_ids += insert_doc(path, collection_name)

    return doc_ids


@db_operation
def insert_doc(path: str, collection_name: str) -> list:
    """Inserts all json documents at path."""
    doc = _parse_json(path)

    db = client[db_name]
    collection = db[collection_name]

    doc_ids = []
    for key in doc:
        new_id = str(collection.insert_one(doc[key]).inserted_id)
        doc_ids.append(new_id)

    return doc_ids


def _parse_json(path: str) -> dict:
    """Takes a directory of JSON files and returns them as a dict."""
    out_list = {}

    for item in os.scandir(path):
        if os.path.isfile(item) and item.path.endswith('.json'):
            with open(item.path, 'r') as file:
                json_dict = json.load(file)
                out_list[json_dict['meta']['s_parameter']] = json_dict

    return out_list
