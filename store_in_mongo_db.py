from pymongo import MongoClient

class MongoDB:
    
    def __init__(self):
        self.client = client = MongoClient('localhost', 27017)
        self.db = client.rag_project
        self.collection = self.db['raw_data']
    
    def insert(self, doc):
        result = self.collection.insert_one(doc)
        return result
    
    def delete(self, field, value):
        result = self.collection.delete_one({field: value})
        return result
    
    def get_all_docs(self):
        documents = self.collection.find()
        return documents

    def get_all_doc_of_a_source(self, source):
        # documents = self.collection.find()
        documents = self.collection.find({'source': source})
        return documents

