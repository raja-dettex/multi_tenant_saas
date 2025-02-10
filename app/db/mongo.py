from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:secret@localhost:27017')


def get_audit_logs_collection():
    try:
        client = MongoClient(MONGO_URI)
        mongo_db = client['audit-logs-db']
        mongo_collection = mongo_db['audit-logs-collection']
        return mongo_collection
    except Exception as e:
        print(e)
