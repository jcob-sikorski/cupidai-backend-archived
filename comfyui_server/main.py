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

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from pyuploadcare import Uploadcare, File

import httpx

server_address = "127.0.0.1:8188"
client_id = None

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
    print("QUEUEING THE PROMPT")
    prompt_id = queue_prompt(prompt)['prompt_id']
    print(f"PROMPT QUEUED: {prompt_id}")
    output_images = {}
    while True:
        print("RECEIVING DATA")
        out = ws.recv()
        if isinstance(out, str):
            print("DATA RECEIVED IS STRING")
            message = json.loads(out)
            if message['type'] == 'executing':
                print("EXECUTING")
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print("EXECUTION DONE")
                    break #Execution is done
        else:
            print("DATA RECEIVED IS NOT STRING")
            continue #previews are binary data

    print("GETTING HISTORY")
    history = get_history(prompt_id)[prompt_id]
    print("HISTORY RETRIEVED")
    for o in history['outputs']:
        for node_id in history['outputs']:
            print(f"PROCESSING NODE: {node_id}")
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                print("IMAGES FOUND IN NODE OUTPUT")
                images_output = []
                for image in node_output['images']:
                    print(f"GETTING IMAGE: {image['filename']}")
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output
            print(f"IMAGES PROCESSED FOR NODE: {node_id}")

    print("RETURNING OUTPUT IMAGES")
    return output_images


app = FastAPI()

class Message(BaseModel):
    user_id: Optional[str]
    status: Optional[str]
    image_uris: Optional[Dict[str, str]]
    created_at: Optional[str]
    settings_id: Optional[str]
    s3_uris: Optional[List[str]]

def download_and_save_images(image_uris: Dict[str, str], image_ids: Dict[str, str], predefined_path: str) -> None:
    """
    Downloads and saves images based on image URIs and image IDs.
    Args:
        image_uris (Dict[str, str]): Dictionary of image URIs.
        image_ids (Dict[str, str]): Dictionary of image IDs.
        predefined_path (str): Predefined path to save the images.
    """
    print(f"DOWNLOADING AND SAVING IMAGES")
    for key, uri in image_uris.items():
        print(f"GETTING IMAGE ID")
        image_id = image_ids.get(key)
        
        if image_id:
            print(f"SETTING THE UNIQUE FILEPATH OF THE IMAGE")
            image_path = os.path.join(predefined_path, f"{image_id}.jpg")
            print(f"DOWNLOADING IMAGE")
            response = requests.get(uri)
            if response.status_code == 200:
                print(f"WRITING IMAGE TO THE UNIQUE PATH")
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
    print(f"REMOVING IMAGES")
    for key, image_id in image_ids.items():
        print(f"SETTING THE UNIQUE FILEPATH OF THE IMAGE")
        image_path = os.path.join(predefined_path, f"{image_id}.jpg")
        try:
            print(f"REMOVING AN IMAGE")
            os.remove(image_path)
            print(f"Image removed: {image_path}")
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

def upload_image_to_uploadcare(image_data, image_name):
    print(f"INITIALIZING UPLOADCARE CLIENT")
    uploadcare = Uploadcare(public_key='e6daeb69aa105a823395', secret_key='b230fca6ccfea3cccfa2')

    print(f"DECODING IMAGE TO BYTES")
    file_handle = io.BytesIO(image_data)

    print(f"UPLOADING AN IMAGE TO UPLOADCARE")
    ucare_file = uploadcare.upload(file_handle)

    print(f"RETURNING AN IMAGE UUID")
    return ucare_file.uuid

async def send_webhook_acknowledgment(user_id: str, message_id: str, status: str, webhook_url: str, s3_uris: Optional[List[str]] = None) -> None:
    """
    Sends an acknowledgment message via webhook.

    Args:
        message_id (str): The unique identifier for the message.
        webhook_url (str): The URL of the webhook endpoint.

    Returns:
        None
    """
    print("SENDING WEBHOOK ACKNOWLEDGMENT")
    try:
        print("CREATING DICTIONARY TO STORE THE FIELDS")
        # Create a dictionary to store the fields
        message_fields = {
            'user_id': user_id,
            'message_id': message_id,
            'status': status
        }

        # Only include the 'uploadcare_uuid' field if it is not None
        if s3_uris is not None:
            print("ADDING s3_uris FIELD TO MESSAGE MODEL")
            message_fields['s3_uris'] = s3_uris

        print("CREATING MESSAGE MODEL")
        # Create the Message object
        message = Message(**message_fields)

        print(f"MAKING POST REQUEST TO THE WEBHHOK {webhook_url}")
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=message.__dict__)
            if response.status_code == 200:
                print("Webhook request successful!")
            else:
                print(f"Webhook request failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error sending acknowledgment: {str(e)}")



# Define a POST endpoint to receive the JSON payload
# async def create_item(json_payload: WorkflowRequest):
@app.post("/")
async def create_item(request: Request):
    try:
        print(f"MAKING REQUEST TO JSON CONVERSION")
        body = await request.body()
        body_str = body.decode()
        json_payload = json.loads(body_str)

        print(f"GOT THE REQUEST: {json_payload}")
        # Access the workflow and user_id from the JSON payload
        workflow = f"""{json_payload['workflow']}"""

        image_uris = json_payload['image_uris']
        image_ids = json_payload['image_ids']
        message_id = json_payload['message_id']
        user_id = json_payload['user_id']

        webhook_url = 'https://garfish-cute-typically.ngrok-free.app/image-generation/webhook'

        send_webhook_acknowledgment(user_id, message_id, 'in progress', webhook_url)
        
        # Process the workflow data or perform any desired actions
        print("Received workflow:", workflow)
        print("Image URIs:", image_uris)
        print("Image IDs:", image_ids)
        print("User ID:", user_id)

        predefined_path = 'C:\\Users\\Shadow\\Desktop'

        download_and_save_images(image_uris, image_ids, predefined_path)

        print(f"CONNECTING TO WEBSOCKET")
        client_id = user_id
        ws = websocket.WebSocket()
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")


        images = get_images(ws, workflow)

        # List to store Uploadcare UUIDs
        s3_uris = []

        for node_id in images:
            for image_data in images[node_id]:
                # Upload image to Uploadcare
                uploadcare_uuid = upload_image_to_uploadcare(image_data)
                print("APPENDING UPLOADCARE UUID TO THE ARRAY")
                s3_uris.append(uploadcare_uuid)

        send_webhook_acknowledgment(user_id, message_id, 'completed', webhook_url, s3_uris)

        remove_images(image_ids, predefined_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)