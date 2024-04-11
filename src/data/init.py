"""Initialize MongoDB database"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.binary import UuidRepresentation

load_dotenv()

def get_db():
    """Connect to MongoDB database instance"""

    mongoCredentials = os.getenv("MONGODB_CREDENTIALS")
    mongoClient = MongoClient(
        f"mongodb+srv://{mongoCredentials}@atlascluster.2zt2wrb.mongodb.net/",
        uuidRepresentation="standard"
    )

    db = mongoClient['cupidai']

    account_col = db['Account']
    stripe_account_col = db['StripeAccount']
    team_col = db['Team']
    tos_col = db['TermsOfService']
    plan_col = db['Plan']
    history_col = db['History']
    comfyui_col = db['ComfyUI']
    settings_col = db['Settings']
    midjourney_col = db['Midjourney']
    bug_col = db['Bug']
    deepfake_col = db['Deepfake']
    social_account_col = db['SocialAccount']
    member_col = db['Member']

    return account_col, stripe_account_col, team_col, tos_col, plan_col, history_col, comfyui_col, settings_col, midjourney_col, bug_col, deepfake_col, social_account_col, member_col

account_col, stripe_account_col, team_col, tos_col, plan_col, history_col, comfyui_col, settings_col, midjourney_col, bug_col, deepfake_col, social_account_col, member_col = get_db()