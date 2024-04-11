from typing import List

import requests

import data.team as data

from model.team import Team

def accept(member_id: str, user_id: str) -> None:
    return data.accept(member_id, user_id)

# TODO: how do we handle the case when we want to invite a new user to the team?
# TODO: in accept function we must map the email to the user_id for the exisitng user
# TODO: for not existing user we must somehow indicate to the frontend that he needs 
#       to signup and his user_id was created + added to the team
def invite(email: str, user_id: str) -> None:
    # Get the team name based on the user_id
    team_name = data.get_team_name(user_id)

    if team_name is not None:
        response = requests.request(
            "POST", 
            "https://app.loops.so/api/v1/transactional", 
            json={
                "transactionalId": "cltertje200k7zf04tzzdhmgx",
                "email": email,
                "dataVariables": {
                    "link": f"https:/cupidai.tech/team/accept/{member_id}/{user_id}",
                    "team_name": team_name
                }
            },
            headers={
                "Authorization": "Bearer 1dd67db210159eeff8910667b5db9b91",
                "Content-Type": "application/json"
            }
        )
    else:
        print("User ID not found in Team collection.")

# TESTING DONE ✅
def update_permissions(permissions: List[str], member_id: str, user_id: str) -> None:
    return data.update_permissions(permissions, member_id, user_id)

# TESTING DONE ✅
def delete(member_id: str, user_id: str) -> None:
    return data.delete(member_id, user_id)

# TESTING DONE ✅
def transfer_ownership(member_id: str, user_id: str) -> None:
    return data.transfer_ownership(member_id, user_id)

# TESTING DONE ✅
def get_members(user_id: str) -> None:
    return data.get_members(user_id)

def get_activity(user_id: str) -> None:
    return data.get_activity(user_id)

# TESTING DONE ✅
def disband(user_id: str) -> None:
    return data.disband(user_id)

# TESTING DONE ✅
def create(team: Team, user_id: str) -> None:
    return data.create(team, user_id)

# TESTING DONE ✅
def leave(user_id: str) -> None:
    try:
        return data.leave(user_id)
    except Exception as e:
        raise e

# TESTING DONE ✅
def owner(user_id: str) -> None:
    return data.owner(user_id)

# TESTING DONE ✅
def get_team(user_id: str):
    return data.get_team(user_id)