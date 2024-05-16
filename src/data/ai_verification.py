from typing import List, Optional

from uuid import uuid4

from model.ai_verification import Prompt

from pymongo import ReturnDocument
from .init import midjourney_prompt_col


def create_prompt(prompt: Prompt,
                  user_id: str) -> Optional[Prompt]:
    prompt = prompt.dict()

    prompt['user_id'] = user_id

    result = midjourney_prompt_col.insert_one(prompt)

    if not result:
        raise ValueError("Failed to create midjourney prompt.")

    print("MIDJOURNEY PROMPT CREATED: ", prompt)
    return prompt


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