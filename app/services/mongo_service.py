from pymongo import MongoClient
from ..models.document_model import Document
from ..configs.settings import settings

client = MongoClient(settings.MONGODB_URI)
collection = client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]

def store_in_mongodb(document: Document):
    doc_dict = document.dict()
    collection.insert_one(doc_dict)