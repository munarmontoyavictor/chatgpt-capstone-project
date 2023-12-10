import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import errors
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

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
        mongo_uri = (
            f"mongodb://{self.username}:{self.password}@"
            f"{self.server}:{self.port}/?authMechanism=DEFAULT&authSource={self.db}"
        )
        mongoClient = MongoClient(mongo_uri, serverSelectionTimeoutMS=500)
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

    def get_all(self):
        documents = list(self.collection.find({"transcription": {"$exists": True}}))
        for document in documents:
            document["job_id"] = str(document.pop("_id"))

        return documents

    def get_by_id(self, job_id):
        result = {"message": "Item not found"}
        try:
            object_id = ObjectId(job_id)
            document = self.collection.find_one({"_id": object_id})
            if document:
                if "transcription" in document:
                    document["message"] = 'ok'
                    document["job_id"] = str(document.pop("_id"))
                    result = document
                else:
                    result = {"message": "Transcription in process"}
            return result
        except errors.InvalidId:
            return {"message": "Invalid ObjectId"}


    def save(self, data):
        response = self.collection.insert_one(data)
        return response.inserted_id

    def update(self, data, db_id):
        filter_criteria = {'_id': db_id}
        updated_data = {"$set": data}
        response = self.collection.update_one(filter_criteria, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

