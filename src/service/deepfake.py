from fastapi import BackgroundTasks

from typing import Dict, List, Optional

from error import NotAuthorized

import httpx

import re

import data.deepfake as data

from model.account import Account
from model.deepfake import Message

import service.billing as billing_service
import service.history as history_service

def webhook(deepfake: Deepfake) -> None:
    print(deepfake)
    update_deepfake(user_id=deepfake_message.user_id, deepfake_id=deepfake_message.deepfake_id, status=deepfake_message.status, s3_uri=deepfake_message.s3_uri)

    if deepfake_message.status == 'in progress':
        history_service.update('deepfake', deepfake_message.user_id)

def update_message(user_id: str, status: Optional[str] = None, uploadcare_uris: Optional[List[str]] = None, message_id: Optional[str] = None, reference_face_distance: Optional[str] = None, face_enhancer_model: Optional[float] = None, frame_enhancer_blend: Optional[float] = None, s3_uri: Optional[str] = None):
    return data.update_deepfake(user_id, status, uploadcare_uris, deepfake_id, reference_face_distance, face_enhancer_model, frame_enhancer_blend, s3_uri)

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None
    
async def send_post_request(url: str, headers: dict, payload: dict) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)

def generate(message: Message, user: Account, background_tasks: BackgroundTasks) -> None:
    if billing_service.has_permissions('deepfake', user.user_id):
        # TODO: if above or equal to business plan call the api
        #       else call our runpod server + set up webhook probably for both?        

        image_ids = [extract_id_from_uri(uri) for uri in message.uploadcare_uris]

        # TODO: we can add here kwargs of message instead to make this more compact + search for all other similar function in codebase
        message_id = update_message(user.user_id, "started", message.uploadcare_uris, None, message.reference_face_distance, message.face_enhancer_model, message.frame_enhancer_blend, None)


        # Define the URL of the server
        url = "https://native-goat-saved.ngrok-free.app/"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # TODO: pass here other facefusion paramters
        # Define the payload for the request
        payload = {
            'uploadcare_uris': message.uploadcare_uris,
            'image_ids': image_ids,
            'message_id': message_id,
            'user_id': user.user_id
        }

        background_tasks.add_task(send_post_request, url, headers, payload)
        
        return message_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

# TESTING DONE ✅
def get_history(user: Account) -> None:
    return data.get_history(user.user_id)