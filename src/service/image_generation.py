from typing import Dict

import re

import httpx

from error import NotAuthorized

from comfyui.ModelInterface import generate_workflow

import data.image_generation as data

from model.image_generation import Settings, Message

import service.billing as billing_service
import service.history as history_service

def webhook(message: Message) -> None:
    data.update(message)

    history_service.update('image_generation', message.user_id)

def save_settings(settings: Settings):
    return data.save_settings(settings)

def update_message(user_id: str, status: str, image_uris: Dict[str, str], settings_id: str):
    return data.update_message(user_id, status, image_uris, settings_id)

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None

async def generate(settings: Settings, image_uris: Dict[str, str], user_id: str) -> None:
    if billing_service.has_permissions('image_generation', user_id):
        image_ids = {key: extract_id_from_uri(uri) for key, uri in image_uris.items()}

        settings_id = save_settings(settings)

        message_id = update_message(user_id, "started", image_uris, settings_id)

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
            'image_uris': image_uris,
            'image_ids': image_ids,
            'user_id': user_id
        }

        # Send the POST request
        async with httpx.AsyncClient() as client:
            client.post(url, headers=headers, json=payload)
    else:
        raise NotAuthorized(msg=f"Invalid permissions")
    

# we set up the fastapi server listening on some port and waiting for the generation request
# then it forwards the request to the fastapi and then uploads the generated images to the uploadcare and makes the post request to the
# previous fastapi server with the images uris which that server saves to a collection which is monitored by frontend by polling