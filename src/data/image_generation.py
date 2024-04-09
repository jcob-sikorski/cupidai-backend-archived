from model.image_generation import Settings, Message

from pymongo import ReturnDocument
from .init import comfyui_col, settings_col

def update(message: Message) -> None:
    comfyui_col.find_one_and_update(
        {"message_id": message.message_id},
        {"$set": message.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

def save_settings(settings: Settings) -> None:
    settings_col.find_one_and_update(
        {"settings_id": settings.settings_id},
        {"$set": settings.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )