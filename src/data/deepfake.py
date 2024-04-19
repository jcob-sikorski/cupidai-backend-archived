from typing import List, Optional

from bson.objectid import ObjectId

from model.deepfake import Message

from pymongo import ReturnDocument
from .init import deepfake_col


def create(message: Message) -> bool:
    print("ADDING DEEPFAKE MESSAGE TO THE COLLECTION")
    result = deepfake_col.insert_one(message.dict())
    return result.inserted_id is not None



def update_message(user_id: str, 
                   status: Optional[str] = None, 
                   uploadcare_uris: Optional[List[str]] = None, 
                   message_id: Optional[str] = None, 
                   reference_face_distance: Optional[str] = None, 
                   face_enhancer_model: Optional[float] = None, 
                   frame_enhancer_blend: Optional[float] = None, 
                   s3_uri: Optional[str] = None):
    
    message = Message(
        user_id=user_id,
        status=status,
        uploadcare_uris=uploadcare_uris,
        message_id=message_id,
        reference_face_distance=reference_face_distance,
        face_enhancer_mode=face_enhancer_model,
        frame_enhancer_blend=frame_enhancer_blend,
        s3_uri=s3_uri
    )

    update_fields = {key: value for key, value in message.dict().items() if value is not None}

    if message_id:
        print("UPDATING MESSAGE (message_id not null)")
        deepfake_col.find_one_and_update(
            {"_id": ObjectId(message_id)},  # Convert message_id to ObjectId
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER
        )
    else:
        print("CREATING NEW MESSAGE (message_id is null)")
        message_id = deepfake_col.insert_one(update_fields)
        message_id = str(message_id.inserted_id)
    
    return message_id



def get_history(user_id: str) -> List[Message]:
    print("GETTING DEEPFAKE HISTORY")
    results = deepfake_col.find({"user_id": user_id})

    messages = [Message(**result) for result in results]

    return messages