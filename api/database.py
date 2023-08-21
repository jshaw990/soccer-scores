import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

__MONGO_URI__ = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER_ADDRESS')}.mongodb.net/?retryWrites=true&w=majority"

class DatabaseConnection: 
    def test_db_conntection():
        """
        Test the connection to MongoDB

        Returns: 
            str : Prints success to console
        Raises:
            Exception: Error connecting to DB

        """

        client = MongoClient(__MONGO_URI__, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            print('Pinged success!')
        except Exception as exception:
            raise Exception(f'An error occurred: {exception}')

    def write_to_db(data, db = 'testDb', collection = 'testCollection1'):
        """
        Write provided data to MongoDB database

        Args:
            data(list) : Data in list format to be written to db
            db(str) : Database name (default - testDb)
            collection(str) : Database collection (default - testCollection1)
        """
        print(f'Writing data to {db} - {collection}')
        try:
            client = MongoClient(__MONGO_URI__, server_api=ServerApi('1'))
            insert_to = client[db][collection]

            for x in data:
                x.update({'_id': x['fixture']['id']})
                insert_to.update_one(
                    { '_id': x['fixture']['id']},
                    { '$set': x},
                    upsert = True
                )
        except Exception as exception:
            raise Exception(f'An error occurred while writing to database. Error: {exception}')
            
