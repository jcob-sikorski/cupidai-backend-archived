import data.deepfake as data

import replicate

import multiprocessing

from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake

from model.user import User

from bson import ObjectId

from error import NotAutorized

def get_status(deepfake_id: str) -> DeepfakeStatus:
    return data.get_status(deepfake_id)
    

def get_usage(user: User) -> DeepfakeUsage:
    return data.get_usage(user)


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
        data.update_usage(user)
        data.update_status(deepfake_id, output_uri)

def generate(deepfake: Deepfake, user: User) -> str:
    if data.has_permissions(user):
        deepfake_id = str(ObjectId())
        data.create_status(deepfake_id)

        # Create a detached process which monitors and updates the db
        p = multiprocessing.Process(target=run_inference, args=(deepfake, deepfake_id, user))
        p.start()
        
        return deepfake_id
    else:
        raise NotAutorized(msg=f"Invalid permissions")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
