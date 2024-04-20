from fastapi import BackgroundTasks

from typing import Dict, List, Optional

from error import NotAuthorized

import httpx

import re

import json

import requests

from pyuploadcare import Uploadcare

import data.deepfake as data

from model.account import Account
from model.deepfake import Message

import service.billing as billing_service
import service.history as history_service

def update_message(user_id: str, 
                   status: Optional[str] = None, 
                   source_uri: Optional[str] = None,
                   target_uri: Optional[str] = None,
                   message_id: Optional[str] = None, 
                   s3_uri: Optional[str] = None):
    
    print("UPDATING MESSAGE")
    return data.update_message(user_id,
                                status,
                                source_uri,
                                target_uri,
                                message_id,
                                s3_uri)

def extract_id_from_uri(uri):
    # Use regex to extract the UUID from the URI
    match = re.search(r"/([a-f0-9-]+)/-/", uri)
    if match:
        return match.group(1)
    else:
        return None
    
async def send_post_request(url: str, headers: dict, payload: dict) -> None:
    print("SENDING POST REQUEST")
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)

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
      "modifyVideo": target_uri, # TODO: this should be target video link not target image link
      "webhookUrl": "https://garfish-cute-typically.ngrok-free.app/deepfake/a-webhook"
    })
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MjEwYzUzZDkxZGZiNzg5ZjUxNDg1MyIsInVpZCI6MTkzMzU0NywiZW1haWwiOiJqbS5zaWVraWVyYUBnbWFpbC5jb20iLCJjcmVkZW50aWFsSWQiOiI2NjIyNGM1YWQ5MWRmYjc4OWY1NmJiOGMiLCJmaXJzdE5hbWUiOiJKYWt1YiIsImZyb20iOiJ0b08iLCJ0eXBlIjoidXNlciIsImlhdCI6MTcxMzUyMzk1MCwiZXhwIjoyMDI0NTYzOTUwfQ.K0DvoRu5mTloYdWfF4zAEAf3oSl3o1zWmioGdHB06Kk',
      'Content-Type': 'application/json'
    }

    print("ADDING BACKGROUND TASK")
    background_tasks.add_task(send_post_request, url, headers, payload)

def generate(
        message: Message, 
        user: Account, 
        background_tasks: BackgroundTasks) -> None:
    
    if billing_service.has_permissions('deepfake', user):
        source_id = extract_id_from_uri(message.source_uri)
        source_format = get_file_format(source_id)

        if source_format not in ['jpeg', 'png', 'heic']:
            return 500 # TODO we must also raise exceptions

        target_id = extract_id_from_uri(message.target_uri)
        target_format = get_file_format(target_id)

        message_id = update_message(user.user_id,
                                    "started",
                                    message.source_uri,
                                    message.target_uri,
                                    None,
                                    None)
        
        source_opts = run_face_detection(message.source_uri)
        target_opts = run_face_detection(message.target_uri)

        if target_format in ['mov', 'mp4']:
            run_video(message.source_uri,
                      message.target_uri,
                      source_opts,
                      target_opts,
                      background_tasks)
        else:
            run_photo(message.source_uri,
                      message.target_uri,
                      source_opts,
                      target_opts,
                      background_tasks)
        
        return message_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")


def get_history(user: Account) -> None:
    return data.get_history(user.user_id)