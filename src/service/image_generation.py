from typing import Dict, List, Optional

import re

import httpx

from error import NotAuthorized

from comfyui.ModelInterface import generate_workflow

import data.image_generation as data

from model.image_generation import Settings, Message

import service.billing as billing_service
import service.history as history_service

def webhook(message: Message) -> None:
    data.update_message(user_id=message.user_id, message_id=None, status=message.status, s3_uris=message.s3_uris)

    history_service.update('image_generation', message.user_id)

def check_settings(settings: Settings):
    # TODO: here we must verify all the setting's fields
    pass

def save_settings(settings: Settings):
    return data.save_settings(settings)

def update_message(user_id: str, message_id: Optional[str] = None, status: Optional[str] = None, uploadcare_uris: Optional[Dict[str, str]] = None, settings_id: Optional[str] = None, s3_uris: Optional[List[str]] = None):
    return data.update_message(user_id, message_id, status, uploadcare_uris, settings_id, s3_uris)

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None

async def generate(settings: Settings, uploadcare_uris: Dict[str, str], user_id: str) -> None:
    if billing_service.has_permissions('image_generation', user_id):
        image_ids = {key: extract_id_from_uri(uri) for key, uri in uploadcare_uris.items()}

        settings_id = save_settings(settings)

        message_id = update_message(user_id, None, "started", uploadcare_uris, settings_id, None)

        workflow_json = generate_workflow(settings, image_ids)

        if workflow_json is None:
            update_message(user_id, message_id, "failed")
            return None

        # Define the URL of the server
        url = "https://native-goat-saved.ngrok-free.app/"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # Define the payload for the request
        payload = {
            'workflow': workflow_json,
            'uploadcare_uris': uploadcare_uris,
            'image_ids': image_ids,
            'settings_id': settings_id,
            'user_id': user_id
        }

        # Send the POST request
        async with httpx.AsyncClient() as client:
            await client.post(url, headers=headers, json=payload)
    else:
        raise NotAuthorized(msg=f"Invalid permissions")