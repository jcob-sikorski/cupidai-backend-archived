import multiprocessing

import replicate

from error import NotAuthorized

from bson import ObjectId

from model.deepfake import Deepfake

import data.deepfake as data

import service.billing as billing_service
import service.history as history_service

def run_inference(deepfake, deepfake_id: str, user_id: str) -> None:
    output = replicate.run(
        "okaris/facefusion:963e964879a44c24b0b5b9cc612a5c64c60dc2e27e0ace0173b1c3c47ef3a188",
        input={
            "source": deepfake.source_uri,
            "target": deepfake.target_uri,
            "keep_fps": deepfake.keep_fps,
            "enhance_face": deepfake.enhance_face
        }
    )

    # The predict method returns an iterator, and you can iterate over that output.
    output_uri = None
    for item in output:
        output_uri = item

    if output_uri:
        history_service.update('deepfake', user_id)

        data.update_status(deepfake_id)

def generate(deepfake: Deepfake, user_id: str) -> None:
    if billing_service.has_permissions('deepfake', user_id):
        deepfake_id = str(ObjectId())
        history_service.update('deepfake')

        # Create a detached process which monitors and updates the db
        p = multiprocessing.Process(target=run_inference, args=(deepfake, deepfake_id, user_id))
        p.start()
        
        return deepfake_id
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

def get_history(user_id: str) -> None:
    return data.get_history(user_id)