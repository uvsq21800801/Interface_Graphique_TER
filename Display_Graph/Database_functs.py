import os
import pymongo as pm
from dotenv import load_dotenv

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