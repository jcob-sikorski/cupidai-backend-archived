"""Initialize MongoDB database"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.binary import UuidRepresentation

load_dotenv()

def get_db():
    """Connect to MongoDB database instance"""

    # mongoCredentials = os.getenv("MONGODB_CREDENTIALS")
    # mongoClient = MongoClient(
    #     f"mongodb+srv://{mongoCredentials}@atlascluster.2zt2wrb.mongodb.net/",
    #     uuidRepresentation="standard"
    # )

    # db = mongoClient['cupidai']

    # user_col = db['User']
    # stripe_account_col = db['StripeAccount']
    # team_col = db['Team']
    # tos_col = db['TermsOfService']
    # history_col = db['History']
    # midjourney_col = db['Midjourney']
    # bug_col = db['Bug']
    # deepfake_col = db['Deepfake']
    # social_account_col = db['SocialAccount']
    # member_col = db['Member']

    user_col = None
    stripe_account_col = None
    team_col = None
    tos_col = None
    history_col = None
    midjourney_col = None
    bug_col = None
    deepfake_col = None
    social_account_col = None
    member_col = None

    return user_col, stripe_account_col, team_col, tos_col, history_col, midjourney_col, bug_col, deepfake_col, social_account_col, member_col

user_col, stripe_account_col, team_col, tos_col, history_col, midjourney_col, bug_col, deepfake_col, social_account_col, member_col = get_db()