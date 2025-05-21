import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # If MongoDB URI is not set, use a default local connection
           
            mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
            db_name = os.environ.get('MONGODB_DB', 'taskscentral')
            
            self.client = MongoClient(mongo_uri)
            # Check connection
            self.client.admin.command('ping')
            logger.info("MongoDB connection successful")
            
            # Connect to the database
            self.db = self.client[db_name]
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False

    def get_collection(self, collection_name):
        """Get a MongoDB collection"""
        if not self.db:
            if not self.connect():
                logger.error(f"Cannot get collection {collection_name}: No database connection")
                return None
        return self.db[collection_name]

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("MongoDB connection closed")

# Create a singleton instance
mongodb_client = MongoDBClient()

def get_db():
    """Get the MongoDB database instance"""
    return mongodb_client.db

def get_collection(collection_name):
    """Get a collection from MongoDB"""
    return mongodb_client.get_collection(collection_name)