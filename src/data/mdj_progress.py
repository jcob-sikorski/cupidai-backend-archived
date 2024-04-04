from model.mdj_progress import Progress

from pymongo import ReturnDocument
from .init import progress_col

def update(progress: Progress) -> None:
    progress_col.find_one_and_update(
        {"message_id": progress.message_id},
        {"$set": progress.dict()},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )