import requests
import json

from model.account import Account, Invite

from pymongo import ReturnDocument
from .init import account_col, invite_col

def create(email: str, user_id: str) -> None:
    # Check if account with the given user_id already exists
    existing_account = account_col.find_one({"user_id": user_id})
    if existing_account:
        # Account already exists, return an error
        raise ValueError("Account already exists for this user ID")

    # Create a new account
    account = Account(email=email, user_id=user_id)
    account_col.insert_one(account.dict())

    # Optionally, return the newly created account
    return account

def create_invite(invite: Invite):
    result = invite_col.insert_one(invite.dict())

def change_email(email: str, user_id: str) -> None:
    result = account_col.find_one_and_update(
        {"user_id": user_id},
        {"$set": {"email": email}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    # TODO:
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = json.dumps({
    #   "email": email,
    #   "connection": "passwordless"
    # })

    # headers = {
    #   'Content-Type': 'application/json',
    #   'Accept': 'application/json'
    # }

    # response = requests.request("PATCH", url, headers=headers, data=payload)

# TESTING DONE ✅
def get(user_id: str) -> None:
    print("GETTING USER DETAILS")
    result = account_col.find_one({"user_id": user_id})

    if result is not None:
        account = Account(**result)
        return account
    return None

def get_by_email(email: str) -> None:
    print("GETTING USER DETAILS BY EMAIL")
    result = account_col.find_one({"email": email})

    if result is not None:
        account = Account(**result)
        return account
    return None

# def get(user_id: str) -> None:
    # TODO:
    # return 200

    # TODO: is this really a user_id?
    # TODO: how to get access token which has the user_id?
    # TODO: is this user authenticated?
    # TODO: how to authenticate a user?
    # TODO: what is the setuo to use my fastapi endpoint as a usser and
    #       manage this user?

    # TODO: how to interact with this api? what is the user_id? what is the bearer token?
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = {}

    # headers = {
    #   'Accept': 'application/json',
    #   'Authorization': f'Bearer '
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

def change_profile_picture(profile_uri: str, user_id: str) -> None:
    # TODO:
    return 200
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = json.dumps({
    #   "picture": profile_uri
    # })

    # headers = {
    #   'Content-Type': 'application/json',
    #   'Accept': 'application/json'
    # }

    # response = requests.request("PATCH", url, headers=headers, data=payload)

def delete(user_id: str) -> None:
    # TODO:
    return 200
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = {}

    # headers = {}

    # response = requests.request("DELETE", url, headers=headers, data=payload)

def get_invite(invite_id: str) -> None:
    print("GETTING INVITE DETAILS")
    result = invite_col.find_one({"_id": invite_id})

    if result is not None:
        invite = Invite(**result)
        return invite
    return None