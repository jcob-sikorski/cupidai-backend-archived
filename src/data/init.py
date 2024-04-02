"""Initialize MongoDB database"""

import os
from pymongo import MongoClient

def get_db():
    """Connect to MongoDB database instance"""

    mongoCredentials = os.getenv("MONGODB_CREDENTIALS")
    mongoClient = MongoClient(f"mongodb+srv://{mongoCredentials}@atlascluster.2zt2wrb.mongodb.net/")

    db = mongoClient['cupidai']

    user_col = db['User']
    deepfake_col = db['Deepfake']
    deepfake_status_col = db['DeepfakeStatus']
    deepfake_usage_col = db['DeepfakeUsage']

    return user_col, deepfake_col, deepfake_status_col, deepfake_usage_col

user_col, deepfake_col, deepfake_status_col, deepfake_usage_col = get_db()