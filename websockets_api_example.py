import websocket
import uuid
import json
import urllib.request
import urllib.parse
import io
import requests
import uvicorn

from datetime import datetime

from typing import List, Dict, Any

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from uploadcare.api import FilesApi
from uploadcare.uploader import Uploader

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
    image_uris: List[str]
    user_id: str

class Message(BaseModel):
    message_id: str
    user_id: str
    status: str
    image_uris: List[str]
    created_at: str
    settings_id: str

def upload_image_to_uploadcare(image_data):
    uploader = Uploader(public_key='e6daeb69aa105a823395', secret_key='b230fca6ccfea3cccfa2')
    file_handle = io.BytesIO(image_data)
    file_handle.name = 'image.png'  # You can set a custom name if needed
    file_info = uploader.upload(file_handle)
    return file_info['uuid']

# Define a POST endpoint to receive the JSON payload
@app.post("/")
async def create_item(json_payload: WorkflowRequest):
    try:
        # Access the workflow and user_id from the JSON payload
        workflow = json_payload.workflow
        image_uris = json_payload.image_uris
        user_id = json_payload.user_id
        
        # Process the workflow data or perform any desired actions
        print("Received workflow:", workflow)
        print("Image URIs:", image_uris)
        print("User ID:", user_id)
        
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

        # Create a Message object
        message = Message(
            message_id=uuid4(),
            user_id=user_id,
            status="completed",
            image_uris=image_uris,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            settings_id=uuid4()
        )

        # Now you have a list of Uploadcare UUIDs which you can use in your webhook
        # Send these UUIDs and the Message object to your webhook endpoint
        webhook_data = {'message': message.dict(), 'uuids': uploadcare_uuids}
        response = requests.post('https://garfish-cute-typically.ngrok-free.app/image-generation/webhook', json=webhook_data)

        # Print the response
        print(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)