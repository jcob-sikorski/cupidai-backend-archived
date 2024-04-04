import multiprocessing

import replicate

from model.deepfake import Deepfake
from model.user import User

import data.deepfake as data

import service.billing as billing_service
import service.history as history_service

from error import NotAutorized

from bson import ObjectId

def run_inference(deepfake, deepfake_id: str, user: User) -> None:
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
        # TODO: Implement usage update
    
        # TODO: Implement progress update

        pass

def generate(deepfake: Deepfake, user: User) -> None:
    if billing_service.has_permissions(user):
        deepfake_id = str(ObjectId())
        history_service.update('deepfake')

        # Create a detached process which monitors and updates the db
        p = multiprocessing.Process(target=run_inference, args=(deepfake, deepfake_id, user))
        p.start()
        
        return deepfake_id
    else:
        raise NotAutorized(msg=f"Invalid permissions")

def get_history(user: User) -> None:
    return data.get_history(user)