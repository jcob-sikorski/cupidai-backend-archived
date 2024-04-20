from fastapi import BackgroundTasks

from typing import Dict, List, Optional

from error import NotAuthorized

import httpx

import re

import json

import requests

from pyuploadcare import Uploadcare

import hashlib

from Crypto.Cipher import AES

from Crypto.Util.Padding import unpad

import base64

import data.deepfake as data

from model.account import Account
from model.deepfake import Message

import service.billing as billing_service
import service.history as history_service

# Generate signature
def generate_msg_signature(client_id, timestamp, nonce, msg_encrypt):
    sorted_str = ''.join(sorted([client_id, str(timestamp), str(nonce), msg_encrypt]))

    hash_obj = hashlib.sha1(sorted_str.encode())
    
    return hash_obj.hexdigest()

# Decryption algorithm
def generate_aes_decrypt(data_encrypt, client_id, client_secret):
    aes_key = client_secret.encode()

    iv = client_id.encode()
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    decrypted = unpad(cipher.decrypt(base64.b64decode(data_encrypt)), AES.block_size)

    return decrypted.decode()

def status_message(status_code: int) -> str:
    if status_code == 1 or status_code == 2:
        return "in progress"
    elif status_code == 3:
        return "completed"
    elif status_code == 4:
        return "failed"
    else:
        return "unknown"

def webhook(response: dict) -> None:
    clientId = "AKDt8rWEczpYPzCGur2xE="
    clientSecret = "nmwUjMAK0PJpl0MOiXLOOOwZADm0gkLo"

    signature = response["signature"]
    msg_encrypt = response["dataEncrypt"]
    timestamp = response["timestamp"]
    nonce = response["nonce"]

    new_signature = generate_msg_signature(clientId, timestamp, nonce, msg_encrypt)
    if signature == new_signature:
        result = generate_aes_decrypt(msg_encrypt, clientId, clientSecret)
        decrypted_result = json.loads(result)
        
        # Extracting status code and generating status message
        status_code = decrypted_result.get("status", 0)
        status_msg = status_message(status_code)
        
        # Print the status message
        print("Status:", status_msg)
        print("_id:", decrypted_result.get("_id", ""))
        print("type:", decrypted_result.get("type", ""))
        print("url:", decrypted_result.get("url", ""))

        job_id = decrypted_result.get("_id", "")

        data.update_message(job_id=job_id,
                            status=status_msg)

        # Return success http status code 200
    else:
        # Return error http status code 400
        pass

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None
    
async def send_post_request(url: str, headers: dict, payload: dict, user_id: str) -> None:
    print("SENDING POST REQUEST")
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

        response_data = response.json()

        code = response_data.get("code")

        data = response_data.get("data", {})
        job_id = data.get("_id")
        output_url = data.get("url")

        data.update_message(user_id=user_id,
                            status='in progress' if code == 1000 else 'failed',
                            job_id=job_id,
                            output_url=output_url)
        
        if code == 1000:
            history_service.update('deepfake', user_id)


def get_file_format(file_id: str):
    print("INITIALIZING UPLOADCARE CLIENT")
    uploadcare = Uploadcare(public_key='e6daeb69aa105a823395', secret_key='9a1b92e275b8fc7855a9')

    print("GETTING FILE FORMAT")
    file_info = uploadcare.file(file_id).info

    return file_info['mime_type'].split('/')[1]

def run_face_detection(uploadcare_uri: str):
    url = "https://sg3.akool.com/detect"

    payload = json.dumps({
      "single_face": True,
      "image_url": uploadcare_uri
    })
    headers = {
      'Authorization': 'Bearer token',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    landmarks_str = response_data.get("landmarks_str", "")

    return landmarks_str

def run_photo(source_uri: str, 
              target_uri: str, 
              source_opts: str, 
              target_opts: str, 
              background_tasks: BackgroundTasks):
    url = "https://openapi.akool.com/api/open/v3/faceswap/highquality/specifyimage"

    payload = json.dumps({
      "sourceImage": {
            "path": source_uri,
            "opts": source_opts
        },
      "targetImage": {
            "path": target_uri,
            "opts": target_opts
        },
      "face_enhance": 1,
      "modifyImage": target_uri,
      "webhookUrl": "https://garfish-cute-typically.ngrok-free.app/deepfake/a-webhook"
    })
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MjEwYzUzZDkxZGZiNzg5ZjUxNDg1MyIsInVpZCI6MTkzMzU0NywiZW1haWwiOiJqbS5zaWVraWVyYUBnbWFpbC5jb20iLCJjcmVkZW50aWFsSWQiOiI2NjIyNGM1YWQ5MWRmYjc4OWY1NmJiOGMiLCJmaXJzdE5hbWUiOiJKYWt1YiIsImZyb20iOiJ0b08iLCJ0eXBlIjoidXNlciIsImlhdCI6MTcxMzUyMzk1MCwiZXhwIjoyMDI0NTYzOTUwfQ.K0DvoRu5mTloYdWfF4zAEAf3oSl3o1zWmioGdHB06Kk',
      'Content-Type': 'application/json'
    }

    print("ADDING BACKGROUND TASK")
    background_tasks.add_task(send_post_request, url, headers, payload)

def run_video(source_uri: str,
              target_uri: str,
              source_opts: str,
              modify_video: str,
              target_opts: str,
              background_tasks: BackgroundTasks):
    url = "https://openapi.akool.com/api/open/v3/faceswap/highquality/specifyimage"

    payload = json.dumps({
      "sourceImage": {
            "path": source_uri,
            "opts": source_opts
        },
      "targetImage": {
            "path": target_uri,
            "opts": target_opts
        },
      "modifyVideo": modify_video,
      "webhookUrl": "https://garfish-cute-typically.ngrok-free.app/deepfake/a-webhook"
    })
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MjEwYzUzZDkxZGZiNzg5ZjUxNDg1MyIsInVpZCI6MTkzMzU0NywiZW1haWwiOiJqbS5zaWVraWVyYUBnbWFpbC5jb20iLCJjcmVkZW50aWFsSWQiOiI2NjIyNGM1YWQ5MWRmYjc4OWY1NmJiOGMiLCJmaXJzdE5hbWUiOiJKYWt1YiIsImZyb20iOiJ0b08iLCJ0eXBlIjoidXNlciIsImlhdCI6MTcxMzUyMzk1MCwiZXhwIjoyMDI0NTYzOTUwfQ.K0DvoRu5mTloYdWfF4zAEAf3oSl3o1zWmioGdHB06Kk',
      'Content-Type': 'application/json'
    }

    print("ADDING BACKGROUND TASK")
    background_tasks.add_task(send_post_request, url, headers, payload)

# TODO: if the uploaded file is a video there must be toggle button
# if the video is running then there are three areas to drag and drop:
# first is for source image, second is for target image and third is for video

def generate(
        message: Message, 
        user: Account, 
        background_tasks: BackgroundTasks) -> None:
    
    if billing_service.has_permissions('deepfake', user):
        source_id = extract_id_from_uri(message.source_uri)
        source_format = get_file_format(source_id)

        target_id = extract_id_from_uri(message.target_uri)
        target_format = get_file_format(target_id)

        if source_format not in ['jpeg', 'png', 'heic'] or \
           target_format not in ['jpeg', 'png', 'heic']:
                
            return 500 # TODO we must also raise exceptions
            
        if message.modify_video:            
            video_id = extract_id_from_uri(message.modify_video)
            video_format = get_file_format(video_id)

            if video_format not in ['mov', 'mp4']:
                return 500 # TODO we must also raise exceptions
            
            source_opts = run_face_detection(message.source_uri)
            target_opts = run_face_detection(message.target_uri)
        
            run_video(message.source_uri,
                      message.target_uri,
                      message.modify_video,
                      source_opts,
                      target_opts,
                      background_tasks)
        else:            
            source_opts = run_face_detection(message.source_uri)
            target_opts = run_face_detection(message.target_uri)
        
            run_photo(message.source_uri,
                      message.target_uri,
                      source_opts,
                      target_opts,
                      background_tasks)
    else:
        raise NotAuthorized(msg=f"Invalid permissions")


def get_history(user: Account) -> None:
    return data.get_history(user.user_id)