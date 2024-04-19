from fastapi import BackgroundTasks

from typing import Dict, List, Optional

from error import NotAuthorized

import httpx

import re

from pyuploadcare import Uploadcare

import data.deepfake as data

from model.account import Account
from model.deepfake import Message

import service.billing as billing_service
import service.history as history_service

def facefusion_webhook(message: Message) -> None:
    print(message)
    update_message(user_id=message.user_id, 
                   message_id=message.message_id, 
                   status=message.status, 
                   s3_uri=message.s3_uri)

    if message.status == 'in progress':
        history_service.update('deepfake', message.user_id)

def check_parameters(message: Message):
    face_enhancer_models = [
        "codeformer",
        "gfpgan_1.2",
        "gfpgan_1.3",
        "gfpgan_1.4",
        "gpen_bfr_256",
        "gpen_bfr_512",
        "gpen_bfr_1024",
        "gpen_bfr_2048",
        "restoreformer_plus_plus"
    ]
    
    if message.reference_face_distance is None:
        return "Error: reference_face_distance is None"
    elif not (0.0 <= message.reference_face_distance <= 1.5 and
              message.reference_face_distance % 0.05 == 0):
        return "Error: reference_face_distance must be between 0.0 and 1.5 and a multiple of 0.05"

    if message.face_enhancer_model is None:
        return "Error: face_enhancer_model is None"
    elif message.face_enhancer_model not in face_enhancer_models:
        return f"Error: face_enhancer_model must be one of {face_enhancer_models}"

    if message.frame_enhancer_blend is None:
        return "Error: frame_enhancer_blend is None"
    elif not (0 <= message.frame_enhancer_blend <= 100):
        return "Error: frame_enhancer_blend must be between 0 and 100"

    return True


def update_message(user_id: str, 
                   status: Optional[str] = None, 
                   uploadcare_uris: Optional[List[str]] = None, 
                   message_id: Optional[str] = None, 
                   reference_face_distance: Optional[str] = None, 
                   face_enhancer_model: Optional[float] = None, 
                   frame_enhancer_blend: Optional[float] = None, 
                   s3_uri: Optional[str] = None):
    
    return data.update_deepfake(user_id, 
                                status, 
                                uploadcare_uris, 
                                message_id, 
                                reference_face_distance, 
                                face_enhancer_model, 
                                frame_enhancer_blend, 
                                s3_uri)

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

def generate(
        message: Message, 
        user: Account, 
        background_tasks: BackgroundTasks) -> None:
    
    if billing_service.has_permissions('deepfake', user.user_id):
        check = check_parameters(message)
        if check is not True:
            return check
        
        # TODO: if above or equal to business plan call the api
        #       else call our runpod server + set up webhook probably for both?     

        file_ids = [extract_id_from_uri(uri) for uri in message.uploadcare_uris]

        uploadcare = Uploadcare(public_key='e6daeb69aa105a823395', secret_key='9a1b92e275b8fc7855a9')

        file_formats = []

        for file_id in file_ids:
            file_info = uploadcare.file(file_id).info()
            file_formats.append(file_info['mime_type'].split('/')[1])

        print("FILE FORMATS")
        print(file_formats)

        message_id = update_message(user.user_id, 
                                    "started", 
                                    message.uploadcare_uris,
                                    None,
                                    message.reference_face_distance, 
                                    message.face_enhancer_model, 
                                    message.frame_enhancer_blend, 
                                    None)


        # Define the URL of the server
        url = "https://native-goat-saved.ngrok-free.app/"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # Define the payload for the request
        payload = {
            'user_id': user.user_id,
            'uploadcare_uris': message.uploadcare_uris,
            'file_ids': file_ids,
            'file_formats': file_formats,
            'message_id': message_id,
            'reference_face_distance': message.reference_face_distance,
            'face_enhancer_model': message.face_enhancer_model,
            'frame_enhancer_blend': message.frame_enhancer_blend
        }

        background_tasks.add_task(send_post_request, url, headers, payload)
        
        return message_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

# TESTING DONE ✅
def get_history(user: Account) -> None:
    return data.get_history(user.user_id)