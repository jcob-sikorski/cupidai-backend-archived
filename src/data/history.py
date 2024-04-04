from model.user import User

from pymongo import ReturnDocument
from .init import history_col

domain_to_index = {
    "": "images_generated" ,
    "deepfake": "deepfakes_generated" ,
    "ai_verification": "ai_verification_generated" ,
    "content_utilities": "content_utilities_uses" ,
    "referral": "people_referred" 
}


def update(domain: str, user: User) -> None:
    # TODO: find a team_id of this user
    team_id = None

    history_col.find_one_and_update(
        {"team_id": team_id},
        {"$inc": {domain_to_index[domain]: 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def get(user: User) -> None:
    result = history_col.find_one({"account_id": user.id})
    if result is not None:
        return User(**result)
    else:
        return None