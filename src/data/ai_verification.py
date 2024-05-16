from typing import Optional, List, Tuple

from uuid import uuid4

from model.ai_verification import Prompt, SocialAccount

from pymongo import ReturnDocument, MongoClient, WriteConcern
from pymongo.errors import OperationFailure
from .init import midjourney_prompt_col, social_account_col

from init import mongoClient

def add_account(social_account: SocialAccount, 
                prompt: Prompt, 
                user_id: str) -> Optional[Tuple[SocialAccount, Prompt]]:
    session = mongoClient.start_session()
    try:
        with session.start_transaction(write_concern=WriteConcern("majority")):
            # Convert social_account and prompt to dictionaries
            social_account_dict = social_account.dict()
            prompt_dict = prompt.dict()

            # Generate a UUID for the account_id and prompt_id
            account_id = str(uuid4())

            # Add user_id, account_id, and prompt_id to the dictionaries
            social_account_dict['user_id'] = user_id
            social_account_dict['account_id'] = account_id

            prompt_dict['user_id'] = user_id
            prompt_dict['account_id'] = account_id

            # Insert the social_account and prompt documents into the collections
            social_account_col.insert_one(social_account_dict, session=session)
            midjourney_prompt_col.insert_one(prompt_dict, session=session)

            # Commit the transaction
            session.commit_transaction()

            # Print the created documents and return the social account
            print("SOCIAL ACCOUNT CREATED: ", social_account_dict)
            print("MIDJOURNEY PROMPT CREATED: ", prompt_dict)

            return social_account
    except OperationFailure as exc:
        # An error occurred, abort the transaction
        print("Transaction aborted:", exc)
        session.abort_transaction()
        return None
    finally:
        # End the session
        session.end_session()


def update_account(social_account: SocialAccount) -> None:
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


def get_accounts(user_id: str) -> Optional[List[SocialAccount]]:
    results = social_account_col.find({"user_id": user_id})

    social_accounts = [SocialAccount(**result) for result in results]

    print("SOCIAL ACCOUNTS: ", social_accounts)

    return social_accounts[::-1]


def update_prompt(prompt: Prompt) -> None:
    update_query = {}

    for field, value in prompt.dict().items():
        if value is not None:
            update_query[field] = value

    result = midjourney_prompt_col.find_one_and_update(
        {"account_id": prompt.account_id},
        {"$set": update_query},
        upsert=False,
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise ValueError("Failed to update prompt.")


def get_prompts(user_id: str) -> Optional[List[Prompt]]:
    results = midjourney_prompt_col.find({"user_id": user_id})

    prompts = [Prompt(**result) for result in results]

    print("PROMPTS: ", prompts)

    return prompts[::-1]