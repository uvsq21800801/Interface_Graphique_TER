import os
from dotenv import load_dotenv
import pymongo as pm
from Inputs.Db_schemas import (
    Structures,
    Configurations,
    Colorations,
    Motifs,
    Occurrences,
    Similarities,
)

## Variables
load_dotenv()
client_uri = os.getenv("CLIENT_URI")
maxSevSelDelay = 30000
color0 = {"name": "interfaceH2O", "elements": ["OW", "OS", "Si"], "haveH": False}

## Connection à la Base de Donnée MongoDb
def connect_mongodb():
    try:
        client = pm.MongoClient(client_uri, serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
        return client
    except pm.errors.ConnectionFailure or pm.errors.ServerSelectionTimeoutError as err:
        print("Failed to connect to server " + str(client_uri) + " : \n" + str(err))
        return None


# Création des collections
def create_collections(db):
    lst_collection = db.list_collection_names()
    dict_schema = {
        "structures": Structures.schema,
        "configurations": Configurations.schema,
        "colorations": Colorations.schema,
        "motifs": Motifs.schema,
        "occurrences": Occurrences.schema,
        "similarities": Similarities.schema,
    }
    dict_coll = {}
    for name in dict_schema:
        if name not in lst_collection:
            dict_coll[name[:3]] = db.create_collection(
                name, validator={"$jsonSchema": dict_schema[name]}
            )
        else:
            dict_coll[name[:3]] = db[name]
    if db.colorations.count_documents({"name": "interfaceH2O"}) == 0:
        db.colorations.insert_one(color0)
    return dict_coll
