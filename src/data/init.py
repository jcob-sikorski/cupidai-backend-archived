from pymongo import MongoClient

from dotenv import load_dotenv

import os

load_dotenv()

def get_db():
    """Connect to MongoDB database instance"""

    mongoClient = MongoClient(
        f"mongodb+srv://{os.getenv('MONGODB_CREDENTIALS')}@atlascluster.2zt2wrb.mongodb.net/",
        uuidRepresentation="standard"
    )

    db = mongoClient[f"{os.getenv('MONGODB_DB')}"]
    account_col = db['Account']
    invite_col = db['Invite']
    password_reset_col = db['PasswordReset']
    stripe_account_col = db['StripeAccount']
    # team_col = db['Team']
    tos_col = db['TermsOfService']
    plan_col = db['Plan']
    usage_history_col = db['UsageHistory']
    comfyui_col = db['ComfyUI']
    settings_col = db['Settings']
    midjourney_col = db['Midjourney']
    midjourney_prompt_col = db['MidjourneyPrompt']
    referral_col = db['Referral']
    payout_request_col = db['PayoutRequest']
    payout_history_col = db['PayoutHistory']
    earnings_col = db['Earnings']
    statistics_col = db['Statistics']
    bug_col = db['Bug']
    deepfake_col = db['Deepfake']
    social_account_col = db['SocialAccount']
    # member_col = db['Member']

    return account_col, invite_col, password_reset_col, stripe_account_col, tos_col, plan_col, usage_history_col, comfyui_col, settings_col, midjourney_col, midjourney_prompt_col, referral_col, payout_request_col, payout_history_col, earnings_col, statistics_col, bug_col, deepfake_col, social_account_col

account_col, invite_col, password_reset_col, stripe_account_col, tos_col, plan_col, usage_history_col, comfyui_col, settings_col, midjourney_col, midjourney_prompt_col, referral_col, payout_request_col, payout_history_col, earnings_col, statistics_col, bug_col, deepfake_col, social_account_col = get_db()