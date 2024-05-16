from typing import List, Optional

from uuid import uuid4

from model.social_account import SocialAccount

from pymongo import ReturnDocument
from .init import social_account_col


def create(social_account: SocialAccount, user_id: str) -> Optional[SocialAccount]:
    # Convert social_account to dictionary
    social_account = social_account.dict()

    # Generate a UUID for the account_id
    account_id = str(uuid4())

    # Add user_id and account_id to the social_account dictionary
    social_account['user_id'] = user_id
    social_account['account_id'] = account_id

    # Insert the social_account into the collection
    result = social_account_col.insert_one(social_account)

    # Check if insertion was successful
    if not result:
        raise ValueError("Failed to create social account.")

    # Print the created account and return it
    print("ACCOUNT CREATED: ", social_account)
    return social_account


def update(social_account: SocialAccount) -> None:
    update_query = {}
    # Iterate through the fields of the SocialAccount object
    for field, value in social_account.dict().items():
        # Check if the field value is not None
        if value is not None:
            # Add the field and value to the update query
            update_query[field] = value

    # Update the document in the collection
    result = social_account_col.find_one_and_update(
        {"account_id": social_account.account_id},
        {"$set": update_query},
        upsert=False,
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise ValueError("Failed to update social account.")


def get(user_id: str) -> Optional[List[SocialAccount]]:
    results = social_account_col.find({"user_id": user_id})

    social_accounts = [SocialAccount(**result) for result in results]

    print("SOCIAL ACCOUNTS: ", social_accounts)

    return social_accounts[::-1]