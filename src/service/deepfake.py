import multiprocessing

import replicate
from replicate.exceptions import ReplicateError

from error import NotAuthorized

import os

from model.deepfake import Deepfake

import data.deepfake as data

import service.billing as billing_service
import service.history as history_service

# TODO: after buying a plan test this function
def run_inference(deepfake, deepfake_id: str, user_id: str) -> None:
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

        # TODO: track the usage for the team and user himself
        history_service.update('deepfake', user_id)
    else:
        data.update(deepfake_id, status="failed")

# TESTING DONE ✅
def generate(deepfake: Deepfake, user_id: str) -> None:
    if billing_service.has_permissions('deepfake', user_id):
        data.create(deepfake)

        print("CREATING A DETACHED PROCESS WHICH MONITORS AND UPDATES THE DB")
        p = multiprocessing.Process(target=run_inference, args=(deepfake, deepfake.deepfake_id, user_id))
        print("STARTING A PROCESS")
        p.start()
        
        return deepfake.deepfake_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

# TESTING DONE ✅
def get_history(user_id: str) -> None:
    return data.get_history(user_id)