import websocket
import uuid
import json
import urllib.request
import urllib.parse
import io
import os
import requests
import uvicorn

from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pyuploadcare import Uploadcare, File

import httpx

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

app = FastAPI()

class WorkflowRequest(BaseModel):
    workflow: Dict[str, Any]
    image_uris: Dict[str, str]
    image_ids: Dict[str, str]
    message_id_id: str
    user_id: str

class Message(BaseModel):
    user_id: Optional[str]
    status: Optional[str]
    image_uris: Optional[Dict[str, str]]
    created_at: Optional[str]
    settings_id: Optional[str]
    uploadcare_uuids: Optional[List[str]]

def download_and_save_images(image_uris: Dict[str, str], image_ids: Dict[str, str], predefined_path: str) -> None:
    """
    Downloads and saves images based on image URIs and image IDs.
    Args:
        image_uris (Dict[str, str]): Dictionary of image URIs.
        image_ids (Dict[str, str]): Dictionary of image IDs.
        predefined_path (str): Predefined path to save the images.
    """
    for key, uri in image_uris.items():
        image_id = image_ids.get(key)
        if image_id:
            image_path = os.path.join(predefined_path, f"{image_id}.jpg")
            response = requests.get(uri)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"Image saved at {image_path}")
            else:
                print(f"Failed to download image from {uri}")
        else:
            print(f"No image ID found for key: {key}")

def remove_images(image_ids: Dict[str, str], predefined_path: str) -> None:
    """
    Removes images based on image IDs.
    Args:
        image_ids (Dict[str, str]): Dictionary of image IDs.
        predefined_path (str): Predefined path where the images are stored.
    """
    for key, image_id in image_ids.items():
        image_path = os.path.join(predefined_path, f"{image_id}.jpg")
        try:
            os.remove(image_path)
            print(f"Image removed: {image_path}")
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

def upload_image_to_uploadcare(image_data):
    uploadcare = Uploadcare(public_key='e6daeb69aa105a823395', secret_key='b230fca6ccfea3cccfa2')
    file_handle = io.BytesIO(image_data)
    file_handle.name = 'image.png'  # You can set a custom name if needed
    ucare_file = uploadcare.upload(file_handle)
    return ucare_file.uuid

async def send_webhook_acknowledgment(user_id: str, message_id: str, status: str, webhook_url: str, uploadcare_uuids: Optional[List[str]] = None) -> None:
    """
    Sends an acknowledgment message via webhook.

    Args:
        message_id (str): The unique identifier for the message.
        webhook_url (str): The URL of the webhook endpoint.

    Returns:
        None
    """
    try:
        # Create a dictionary to store the fields
        message_fields = {
            'user_id': user_id,
            'message_id': message_id,
            'status': status
        }

        # Only include the 'uploadcare_uuid' field if it is not None
        if uploadcare_uuids is not None:
            message_fields['uploadcare_uuids'] = uploadcare_uuids

        # Create the Message object
        message = Message(**message_fields)

        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=message.__dict__)
            if response.status_code == 200:
                print("Webhook request successful!")
            else:
                print(f"Webhook request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error sending acknowledgment: {str(e)}")

# Define a POST endpoint to receive the JSON payload
@app.post("/")
async def create_item(json_payload: WorkflowRequest):
    try:
        # Access the workflow and user_id from the JSON payload
        workflow = json_payload.workflow
        image_uris = json_payload.image_uris
        image_ids = json_payload.image_ids
        message_id = json_payload.message_id
        user_id = json_payload.user_id

        webhook_url = 'https://garfish-cute-typically.ngrok-free.app/image-generation/webhook'

        send_webhook_acknowledgment(user_id, message_id, 'in progress', webhook_url)
        
        # Process the workflow data or perform any desired actions
        print("Received workflow:", workflow)
        print("Image URIs:", image_uris)
        print("Image IDs:", image_ids)
        print("User ID:", user_id)

        predefined_path = 'C:\\Users\\Shadow\\Desktop'

        download_and_save_images(image_uris, image_ids, predefined_path)
        
        ws = websocket.WebSocket()
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
        images = get_images(ws, workflow)

        # List to store Uploadcare UUIDs
        uploadcare_uuids = []

        for node_id in images:
            for image_data in images[node_id]:
                # Upload image to Uploadcare
                uploadcare_uuid = upload_image_to_uploadcare(image_data)
                uploadcare_uuids.append(uploadcare_uuid)

        send_webhook_acknowledgment(user_id, message_id, 'completed', webhook_url, uploadcare_uuids)

        remove_images(image_ids, predefined_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)