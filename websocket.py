#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import os
import httpx

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
import uvicorn

import boto3

from pydantic import BaseModel

from typing import List, Dict, Any, Optional

load_dotenv()

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

app = FastAPI()

# Load AWS S3 Access keys from environment variables
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')

boto3.setup_default_session(aws_access_key_id=S3_ACCESS_KEY,
                            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                            region_name='us-east-1')

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

def upload_images_to_s3(images):
    s3_client = boto3.client('s3')

    image_uris = []

    for node_id in images:
        for image_data in images[node_id]:
            image_key = str(uuid.uuid4())

            
            s3_client.put_object(
                Body=image_data,
                Bucket='magicalcurie',
                Key=image_key
            )

            image_uris.append(f's3://magicalcurie/{image_key}')

    return image_uris

class Message(BaseModel):
    user_id: Optional[str]
    status: Optional[str]
    image_uris: Optional[Dict[str, str]]
    created_at: Optional[str]
    settings_id: Optional[str]
    s3_uris: Optional[List[str]]

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

        if s3_uris is not None:
            print("ADDING UPLOADCARE_UUIDS FIELD TO MESSAGE MODEL")
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


@app.post("/")
async def create_item(request: Request):
    payload = await request.json() 
    workflow = payload.get('workflow', {})
    message_id = payload.get('message_id', {})
    user_id = payload.get('user_id', {})

    webhook_url = 'https://garfish-cute-typically.ngrok-free.app/image-generation/webhook'

    await send_webhook_acknowledgment(user_id, message_id, 'in progress', webhook_url)

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, workflow)

    s3_uris = upload_images_to_s3(images)

    await send_webhook_acknowledgment(user_id, message_id, 'completed', webhook_url, s3_uris)

    return s3_uris

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)