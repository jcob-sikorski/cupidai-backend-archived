from bson.objectid import ObjectId

from model.account import Account, Invite

from service.account import get_password_hash

from pymongo import ReturnDocument
from .init import account_col, invite_col

def signup(username: str, password: str) -> None:
    # Check if account with the given user_id already exists
    existing_account = account_col.find_one({"username": username})
    if existing_account:
        # Account already exists, return an error
        raise ValueError("Account already exists for this user ID")

    # Create a new account
    account = Account(user_id=str(ObjectId()), username=username, password=get_password_hash(password))
    account_col.insert_one(account.dict())

    # Optionally, return the newly created account
    return account


def signup_ref(ref: str) -> None:
    # TODO: make this work the same as team invite
    # although we need the email of the user signing up

    pass


def create_invite(invite: Invite):
    result = invite_col.insert_one(invite.dict())


def change_email(email: str, user: Account) -> None:
    result = account_col.find_one_and_update(
        {"user_id": user.user_id},
        {"$set": {"email": email}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )


def get_user(username: str) -> None:
    print("GETTING USER DETAILS")
    result = account_col.find_one({"username": username})

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


def change_profile_picture(profile_uri: str, user: Account) -> None:
    result = account_col.find_one_and_update(
        {"user_id": user.user.user_id},
        {"$set": {"profile_uri": profile_uri}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def delete(user: Account) -> None:
    # Find and delete the account with the given user_id
    result = account_col.delete_one({"user_id": user.user_id})

    # Check if an account was actually deleted
    if result.deleted_count == 0:
        raise ValueError("No account found with this user ID")

    return {"message": "Account deleted successfully"}


def get_invite(invite_id: str) -> None:
    print("GETTING INVITE DETAILS")
    result = invite_col.find_one({"_id": invite_id})

    if result is not None:
        invite = Invite(**result)
        return invite
    return None