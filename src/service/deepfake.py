import data.deepfake as data

from uuid import uuid4, UUID

import replicate

from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake

from model.user import User

from error import NotAutorized

def get_status(generation_id: UUID) -> DeepfakeStatus:
    return data.get_status(generation_id)
    

def get_usage(user: User) -> DeepfakeUsage:
    return data.get_usage(user)


def generate(deepfake: Deepfake, user: User) -> UUID:
    if data.has_permissions(user):
        output = replicate.run(
            "okaris/facefusion:963e964879a44c24b0b5b9cc612a5c64c60dc2e27e0ace0173b1c3c47ef3a188",
            input={
                "source": deepfake.source_uri,
                "target": deepfake.target_uri,
                "keep_fps": deepfake.keep_fps,
                "enhance_face": deepfake.enhance_face
            }
        )
        
        # The okaris/facefusion model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        output_uri = None
        for item in output:
            output_uri = item

        if output_uri:
            data.update_usage(user)

            deepfake_id = data.add_deepfake(deepfake)

            return deepfake_id
    else:
        raise NotAutorized(msg=f"Invalid permissions")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
