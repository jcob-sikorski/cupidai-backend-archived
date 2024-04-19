#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint

import uuid
import os
import httpx
import requests
import cv2
import numpy as np

import subprocess

from datetime import datetime

from dotenv import load_dotenv

from fastapi import FastAPI, Request
import uvicorn

import boto3

from pydantic import BaseModel

from typing import List, Field, Optional

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

def upload_image_to_s3(output_path):
    s3_client = boto3.client('s3')

    # Read the image file in binary mode
    with open(output_path, 'rb') as f:
        image_data = f.read()

    # Convert the binary data to a numpy array
    image_array = np.frombuffer(image_data, np.uint8)

    # Decode the image data
    image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

    # Save the decoded image as a PNG file
    cv2.imwrite(output_path, image)

    with open(output_path, 'rb') as data:
        s3_client.upload_fileobj(data, 'magicalcurie', output_path)

    s3_uri = f's3://magicalcurie/{output_path}'

    # Remove the local image file
    os.remove(output_path)

    return s3_uri

def download_and_save_images(
        uploadcare_uris: List[str], 
        image_ids: List[str], 
        predefined_path: str) -> None:
    """
    Downloads and saves images based on image URIs and image IDs.
    Args:
        uploadcare_uris (List[str]): List of image URIs.
        image_ids (List[str]): List of image IDs.
        predefined_path (str): Predefined path to save the images.
    """
    print(f"DOWNLOADING AND SAVING IMAGES")
    for image_uri, image_id in zip(uploadcare_uris, image_ids):        
        if image_id:
            print(f"SETTING THE UNIQUE FILEPATH OF THE IMAGE")
            image_path = os.path.join(predefined_path, f"{image_id}.jpg")
            print(f"DOWNLOADING IMAGE")
            response = requests.get(image_uri)
            if response.status_code == 200:
                print(f"WRITING IMAGE TO THE UNIQUE PATH")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"Image saved at {image_path}")
            else:
                print(f"Failed to download image from {image_uri}")
        else:
            print(f"Zip of uploadcare_uris and image_ids is fucked.")

def remove_images(
        image_ids: List[str], 
        predefined_path: str) -> None:
    """
    Removes images based on image IDs.
    Args:
        image_ids (List[str]): List of image IDs.
        predefined_path (str): Predefined path where the images are stored.
    """
    print(f"REMOVING IMAGES")
    for image_id in image_ids:
        print(f"SETTING THE UNIQUE FILEPATH OF THE IMAGE")
        image_path = os.path.join(predefined_path, f"{image_id}.jpg")
        try:
            print(f"REMOVING AN IMAGE")
            os.remove(image_path)
            print(f"Image removed: {image_path}")
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

class Message(BaseModel):
    user_id: str
    status: Optional[str] = None
    uploadcare_uris: Optional[List[str]] = None # the last one is the target uri
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message_id: Optional[str] = None
    reference_face_distance: Optional[float] = None
    face_enhancer_model: Optional[str] = None
    frame_enhancer_blend: Optional[int] = None
    s3_uris: Optional[List[str]] = None

async def send_webhook_acknowledgment(
        user_id: str, 
        message_id: str, 
        status: str, 
        webhook_url: str, 
        s3_uri: str = None) -> None:
    """
    Sends an acknowledgment message via webhook.

    Args:
        user_id (str): The unique identifier for the user.
        message_id (str): The unique identifier for the message.
        status (str): The status of the message.
        webhook_url (str): The URL of the webhook endpoint.
        s3_uri (str): The S3 URI associated with the message.

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

        if s3_uri is not None:
            print("ADDING S3_URI FIELD TO MESSAGE MODEL")
            message_fields['s3_uri'] = s3_uri

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
    user_id = payload.get('user_id', {})
    uploadcare_uris = payload.get('uploadcare_uris', {})
    image_ids = payload.get('image_ids', {})
    message_id = payload.get('message_id', {})
    reference_face_distance = payload.get('reference_face_distance', {})
    face_enhancer_model = payload.get('face_enhancer_model', {})
    frame_enhancer_blend = payload.get('frame_enhancer_blend', {})

    webhook_url = 'https://garfish-cute-typically.ngrok-free.app/deepfake/webhook'

    await send_webhook_acknowledgment(user_id, message_id, 'in progress', webhook_url)

    try:
        predefined_path = 'C:\\Users\\Shadow\\Desktop'

        download_and_save_images(uploadcare_uris, image_ids, predefined_path)

        command = ["python", "run.py", 
                   "--headless", 
                   "--reference-face-distance", reference_face_distance, 
                   "--face-enhancer-model", face_enhancer_model, 
                   "--frame-enhancer-blend", frame_enhancer_blend]

        # Add a '-s' flag for each image
        for source_id in image_ids[:-1]:
            source_path = os.path.join(predefined_path, f"{source_id}.jpg")
            command.extend(["-s", source_path])

        target_path = predefined_path + f"{image_ids[-1]}.png"

        output_id = uuid.uuid4()
        output_path = os.path.join(predefined_path, f"{output_id}.png")

        command.extend([["-t", target_path, "-o", output_path]])
        
        # Run the command
        subprocess.run(command, check=True)

        s3_uri = upload_image_to_s3(output_path)
    except Exception as e:
        await send_webhook_acknowledgment(user_id, message_id, 'failed', webhook_url)

    await send_webhook_acknowledgment(user_id, message_id, 'completed', webhook_url, s3_uri)

    remove_images(image_ids, predefined_path)

    return s3_uri

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)