from typing import List, Dict, Optional

from datetime import datetime

from model.image_generation import Settings, Message

from pymongo import ReturnDocument
from .init import comfyui_col, settings_col

def update_message(user_id: str, message_id: Optional[str] = None, status: Optional[str] = None, image_uris: Optional[Dict[str, str]] = None, settings_id: Optional[str] = None, uploadcare_uuids: Optional[List[str]] = None) -> None:
    message = Message(
        user_id=user_id,
        status=status,
        image_uris=image_uris,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        settings_id=settings_id
        uploadcare_uuids=uploadcare_uuids
    )

    update_fields = {key: value for key, value in message.dict().items() if value is not None}

    if message_id:
        comfyui_col.find_one_and_update(
            {"_id": message_id},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER
        )
    else:
        message_id = comfyui_col.insert_one(update_fields)
    
    return message_id

def save_settings(settings: Settings) -> None:
    result = settings_col.insert_one(settings.dict())
    inserted_id = str(result.inserted_id)
    return inserted_id