import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import logging
# logging.getLogger('pymongo').setLevel(logging.WARNING)
class MongoAPI:
    def __init__(self, collection_name):
        load_dotenv()
        self.server = os.getenv('MONGO_SERVER')
        self.port = os.getenv('MONGO_PORT')
        self.username = os.getenv('MONGO_APP_USER')
        self.password = os.getenv('MONGO_APP_PASS')
        self.db = os.getenv('MONGO_DB')
        self.client = self.getDB()
        cursor = self.client[self.db]
        self.collection = cursor[collection_name]

    def getDB(self):
        mongoClient = MongoClient("mongodb://" + str(self.username) + ":" + str(self.password) + "@" + str(self.server) + ":" + str(self.port) + "/?authMechanism=DEFAULT&authSource=" + str(self.db), serverSelectionTimeoutMS=500)
        try:
            if mongoClient.admin.command('ismaster')['ismaster']:
                logging.info("Connected to the MongoDB Server!")
                return mongoClient
        except OperationFailure:
            logging.error("Database not found.")
            return None
        except ServerSelectionTimeoutError:
            logging.error("MongoDB Server is down.")
            return None

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def save(self, data):
        response = self.collection.insert_one(data)
        return response.inserted_id

    def update(self, data, db_id):
        filter_criteria = {'_id': db_id}
        updated_data = {"$set": data}
        response = self.collection.update_one(filter_criteria, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        logging.error(f'Update status: {output}, db_id: {db_id}, data: {data}')
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
