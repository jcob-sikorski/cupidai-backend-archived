from typing import Optional

from model.history import History

from pymongo import ReturnDocument

from .init import history_col

domain_to_index = {
    "image_generation": "images_generated",
    "deepfake": "deepfakes_generated",
    "ai_verification": "ai_verification_generated",
    "content_utilities": "content_utilities_uses",
    "referral": "people_referred" 
}


def update(domain: str, user_id: str) -> None:
    print("UPDATING USAGE HISTORY")
    # Update history for the user
    result = history_col.find_one_and_update(
        {"user_id": user_id},
        {"$inc": {domain_to_index[domain]: 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    if result is None:
        raise ValueError("Failed to update the usage history.")

    # # Update history for the team if the user is in a team
    # team = team_service.get_team(user_id)
    # if team:
    #     history_col.find_one_and_update(
    #         {"owner": team.owner},
    #         {"$inc": {domain_to_index[domain]: 1}},
    #         upsert=True,
    #         return_document=ReturnDocument.AFTER
    #     )



def get(user_id: str) -> History:
    # team = team_service.get_team(user_id)

    # if team and user_id in team.members:
    #     result = history_col.find_one({"team_id": team.team_id})
    # else:
        # result = history_col.find_one({"user_id": user_id})
    result = history_col.find_one({"user_id": user_id})

    if result is not None:
        return History(**result)
    else:
        return History(user_id=user_id,
                       images_generated=0,
                       deepfakes_generated=0,
                       ai_verification_generated=0,
                       content_utilities_uses=0,
                       people_referred=0)