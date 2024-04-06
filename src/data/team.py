from typing import List

from model.team import Team, Member

from pymongo import ReturnDocument
from .init import team_col, member_col

def accept(member_id: str, user_id: str) -> None:
    # Check if the user is already in another team
    existing_team = team_col.find_one({"members": user_id})
    
    if existing_team:
        print(f"User {user_id} is already in another team.")
        return

    # Add the user id to the member list
    team = team_col.find_one({"owner": member_id})
    if team:
        team["members"].append(user_id)
        team_col.find_one_and_update(
            {"_id": team["_id"]},
            {"$set": {"members": team["members"]}}
        )

    # Create the member model
    member = Member(user_id=user_id, permissions=[])
    member_col.insert_one(member.dict())


def update_permissions(permissions: List[str], member_id: str, user_id: str) -> None:
    member_col.find_one_and_update(
        {"user_id": member_id},
        {"$set": {"permissions": permissions}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def delete(member_id: str, user_id: str) -> None:
    # Fetch the team that the member belongs to
    team = team_col.find_one({"members": member_id})
    
    if team:
        # Remove the member_id from the team's members list
        team["members"].remove(member_id)
        
        # Update the team document in the database
        team_col.find_one_and_update(
            {"_id": team["_id"]},
            {"$set": {"members": team["members"]}}
        )
    
    # Delete the member model
    member_col.delete_one({"user_id": member_id})


def transfer_ownership(member_id: str, user_id: str) -> None:
    # Fetch the team that the member belongs to
    team = team_col.find_one({"members": member_id})
    
    if team:
        # Update the owner of the team
        team_col.find_one_and_update(
            {"_id": team["_id"]},
            {"$set": {"owner": user_id}}
        )


def get_members(user_id: str) -> None:
    # Fetch the team that the user belongs to
    team = team_col.find_one({"owner": user_id})
    
    if team:
        # Return the members of the team
        return team["members"]


def get_activity(user_id: str) -> None:
    # TODO: to be implemented
    pass

def get_team_name(user_id: str) -> None:
    result = team_col.find_one({"members": user_id})
    if result is not None:
        team = Team(**result)
        return team.name
    return None

def disband(user_id: str) -> None:
    # Fetch the team that the user owns
    team = team_col.find_one({"owner": user_id})
    
    if team:
        # Remove the team document from the database
        team_col.delete_one({"_id": team["_id"]})
        
        # Remove the member models of the team
        for member_id in team["members"]:
            member_col.delete_one({"user_id": member_id})

def leave(user_id: str) -> None:
    # Fetch the team that the user is a member of
    team = team_col.find_one({"members": user_id})
    
    if team:
        # Remove the user_id from the team's members list
        team["members"].remove(user_id)
        
        # Update the team document in the database
        team_col.find_one_and_update(
            {"_id": team["_id"]},
            {"$set": {"members": team["members"]}}
        )
        
        # Remove the member model
        member_col.delete_one({"user_id": user_id})

def owner(user_id: str) -> None:
    # Fetch the team that the user is a member of
    team = team_col.find_one({"members": user_id})
    
    if team:
        # Return the owner of the team
        return team["owner"]