from fastapi import Depends

import httpx

from error import NotAuthorized

from comfyui.ModelInterface import generate_workflow

import data.image_generation as data

from model.image_generation import Settings, Message

import service.billing as billing_service

# TODO: set up the comfyui on the rented PC and install entire server + git to simulate interacting with a fastapi server
# TODO: maybe it's good idea to set the stauts (in progress) on runpod server?
# TODO: set up the webhook which gets and saves the uris of generated images to the db
def webhook(message: Message) -> None:
    data.update(message)

def save_settings(settings: Settings):
    data.save_settings(settings)

async def generate(settings: Settings, user_id: str) -> None:
    if billing_service.has_permissions('image_generation', user_id):
        save_settings(settings)

        workflow_json = generate_workflow(settings)

        # Define the URL of the server
        url = "http://imaginaryserver.com/api/runpod"

        # Define the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # Define the payload for the request
        payload = {
            'workflow': workflow_json,
            'user_id': user_id
        }

        # Send the POST request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # TODO: use the functions to update statuses, usage etc.
            # like in the deepfake and image verification

            pass
        else:
            print(f"Request failed with status code {response.status_code}")
    else:
        raise NotAuthorized(msg=f"Invalid permissions")
    pass
    

# we set up the fastapi server listening on some port and waiting for the generation request
# then it forwards the request to the fastapi and then uploads the generated images to the uploadcare and makes the post request to the
# previous fastapi server with the images uris which that server saves to a collection which is monitored by frontend by polling