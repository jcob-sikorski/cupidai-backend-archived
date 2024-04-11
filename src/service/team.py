from typing import List

import requests

import data.team as data

from model.team import Team

import service.account as account_service

def accept(member_id: str, user_id: str) -> None:
    return data.accept(member_id, user_id)

def invite(guest_email: str, host_id: str) -> None:
    host_as_member = get_member(host_id)

    if host_as_member and ('invite' in host_as_member.permissions):
        guest_account = account_service.get_by_email(guest_email)

        # Get the team name based on the user_id
        team_name = data.get_team_name(host_id)

        # TODO: what we pass for guest_id? we can't pass it because it might be null
        #       email probably too we cant pass becuase the email might contain special characters
        invite_link = f"https://cupidai.tech/team/accept/{guest_id}/{host_id}?signup={str(guest_account is None).lower()}"

        response = requests.request(
            "POST", 
            "https://app.loops.so/api/v1/transactional", 
            json={
                "transactionalId": "cltertje200k7zf04tzzdhmgx",
                "email": guest_email,
                "dataVariables": {
                    # TODO: based on the development/prodcution update all the links
                    "invite_link": invite_link,
                    "team_name": team_name,
                }
            },
            headers={
                "Authorization": "Bearer 1dd67db210159eeff8910667b5db9b91",
                "Content-Type": "application/json"
            }
        )

        # TODO: billing permission and team permission are not the same thing
        #       the billing permissions are the max the team can have
        #       the team permissions start from zero and can increase 
        #       into the billing permissions
    else:
        return # TODO: return some error here

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

def get_member(user_id: str):
    return data.get_member(user_id)