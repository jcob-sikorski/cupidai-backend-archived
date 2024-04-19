from fastapi import BackgroundTasks

from typing import Dict, List, Optional

from error import NotAuthorized

import httpx

import re

import data.deepfake as data

from model.account import Account
from model.deepfake import DeepfakeMessage

import service.billing as billing_service
import service.history as history_service

def webhook(deepfake: Deepfake) -> None:
    print(deepfake)
    update_deepfake(user_id=deepfake_message.user_id, deepfake_id=deepfake_message.deepfake_id, status=deepfake_message.status, s3_uri=deepfake_message.s3_uri)

    if deepfake_message.status == 'in progress':
        history_service.update('deepfake', deepfake_message.user_id)

def update_deepfake(user_id: str, status: Optional[str] = None, source_uris: Optional[Dict[str, str]] = None, target_uri: Optional[str] = None, deepfake_id: Optional[str] = None, reference_face_distance: Optional[str] = None, face_enhancer_model: Optional[float] = None, frame_enhancer_blend: Optional[float] = None, s3_uri: Optional[str] = None):
    return data.update_deepfake(user_id, status, source_uris, target_uri, deepfake_id, reference_face_distance, face_enhancer_model, frame_enhancer_blend, s3_uri)

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

# TODO: same with deepfake: this should probably be named similar to message (deepfake_message?) and (image_gen_message)?

def generate(deepfake_message: DeepfakeMessage, user: Account, background_tasks: BackgroundTasks) -> None:
    if billing_service.has_permissions('deepfake', user.user_id):
        # TODO: if above or equal to business plan call the api
        #       else call our runpod server + set up webhook probably for both?        

        image_ids = [extract_id_from_uri(uri) for uri in deepfake_message.uploadcare_uris]


        deepfake_id = update_deepfake(user.user_id, "started", deepfake_message.uploadcare_uris, None, deepfake_message.reference_face_distance, deepfake_message.face_enhancer_model, deepfake_message.frame_enhancer_blend, None)


        # Define the URL of the server
        url = "https://native-goat-saved.ngrok-free.app/"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }
    
        # Define the payload for the request
        payload = {
            'uploadcare_uris': deepfake_message.uploadcare_uris,
            'image_ids': image_ids,
            'deepfake_id': deepfake_id,
            'user_id': user.user_id
        }

        background_tasks.add_task(send_post_request, url, headers, payload)
        
        return deepfake_message.deepfake_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

# TESTING DONE ✅
def get_history(user: Account) -> None:
    return data.get_history(user.user_id)