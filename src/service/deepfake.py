from fastapi import BackgroundTasks

import replicate
from replicate.exceptions import ReplicateError

from error import NotAuthorized

import os

import data.deepfake as data

from model.account import Account
from model.deepfake import Deepfake

import service.billing as billing_service
import service.history as history_service


def run_inference(deepfake, deepfake_id: str, user: Account) -> None:
    replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    print("RUNNING INFERENCE")
    try:
        output = replicate.run(
            "okaris/facefusion:963e964879a44c24b0b5b9cc612a5c64c60dc2e27e0ace0173b1c3c47ef3a188",
            input={
                "source": deepfake.source_uri,
                "target": deepfake.target_uri,
                "keep_fps": deepfake.keep_fps,
                "enhance_face": deepfake.enhance_face
            }
        )
        
    except ReplicateError as e:
        print(f"Error running inference: {e}")
        data.update(deepfake_id, status="failed")
        return

    # The predict method returns an iterator, and you can iterate over that output.
    output_uri = None
    for item in output:
        output_uri = item

    if output_uri:
        print(f"GOT THE OUTPUT URI: {output_uri}")

        data.update(deepfake_id, output_uri=output_uri)
        
        data.update(deepfake_id, status="completed")

        history_service.update('deepfake', user.user_id)
    else:
        data.update(deepfake_id, status="failed")


def generate(deepfake: Deepfake, user: Account, background_tasks: BackgroundTasks) -> None:
    if billing_service.has_permissions('deepfake', user.user_id):
        data.create(deepfake)

        print("CREATING A BACKGROUND TASK WHICH MONITORS AND UPDATES THE DB")
        background_tasks.add_task(run_inference, deepfake, deepfake.deepfake_id, user.user_id)
        
        return deepfake.deepfake_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

# TESTING DONE ✅
def get_history(user: Account) -> None:
    return data.get_history(user.user_id)