import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

__MONGO_URI__ = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER_ADDRESS')}.mongodb.net/?retryWrites=true&w=majority"

def test_db_conntection():
    client = MongoClient(__MONGO_URI__, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print('Pinged success!')
    except Exception as exception:
        print('AN ERROR OCCURRED: ')
        print(exception)

test_db_conntection()