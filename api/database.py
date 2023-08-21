import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

__MONGO_URI__ = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER_ADDRESS')}.mongodb.net/?retryWrites=true&w=majority"

class MongoConnection: 
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
        
    def get_collection_from_db(collection, db = 'testDb'):
        """
        Read data from the db collection specified

        Args: 
            collection(str) : Database collection name
            db(str) : Database name (default - testDb)

        Returns: 
            list: data from collection
        """
        print(f'Writing data to {db} - {collection}')

        try:
            data = []
            client = MongoClient(__MONGO_URI__, server_api=ServerApi('1'))
            cursor = client[db][collection].find()

            for doc in cursor:
                data.append(doc)

            return data
        except Exception as exception:
            print(exception)
            raise Exception(f'An error occurred while reading {collection} to database. Error: {exception}')

    def write_to_db(data, collection, db = 'testDb'):
        """
        Write provided data to MongoDB database

        Args:
            data(list) : Data in list format to be written to db
            collection(str) : Database collection
            db(str) : Database name (default - testDb)
        """
        print(f'Writing data to {db} - {collection}')
        try:
            client = MongoClient(__MONGO_URI__, server_api=ServerApi('1'))
            insert_to = client[db][collection]

            # print(f'data => {data}')

            for x in data:
                x.update({'_id': x[collection]['id']})
                print(f'\nthis is x => {x}')
                insert_to.update_one(
                    { '_id': x[collection]['id']},
                    { '$set': x},
                    upsert = True
                )
        except Exception as exception:
            print(exception)
            raise Exception(f'An error occurred while writing {collection} to database. Error: {exception}')
            
