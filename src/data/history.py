from model.history import History

from pymongo import ReturnDocument

from .init import history_col

domain_to_index = {
    "": "images_generated" ,
    "deepfake": "deepfakes_generated" ,
    "ai_verification": "ai_verification_generated" ,
    "content_utilities": "content_utilities_uses" ,
    "referral": "people_referred" 
}

# TESTING DONE ✅
def update(domain: str, user_id: str) -> None:
    print("UPDATING USAGE HISTORY")
    history_col.find_one_and_update(
        {"user_id": user_id},
        {"$inc": {domain_to_index[domain]: 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

# TESTING DONE ✅
def get(user_id: str) -> None:
    result = history_col.find_one({"user_id": user_id})
    if result is not None:
        return History(**result)
    else:
        return None