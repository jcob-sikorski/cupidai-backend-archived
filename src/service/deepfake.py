import data.deepfake as data

import replicate

from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake

from model.user import User

from error import NotAutorized

def get_status(generation_id: str) -> DeepfakeStatus:
    return data.get_status(generation_id)
    

def get_usage(user: User) -> DeepfakeUsage:
    return data.get_usage(user)


def generate(deepfake: Deepfake, user: User) -> str:
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

        # The predict method returns an iterator, and you can iterate over that output.
        output_uri = None
        for item in output:
            output_uri = item

        if output_uri:
            data.update_usage(user)

            deepfake_id = data.add_deepfake(deepfake)

            # TODO we should probably here create a detached process which monitors 
            #      and updates the db when it comes to the status of the replicate run
            #      specifically if it's possible to download the generated image
            #      if it's possible it should mark it in the db by calling the webhook

            return deepfake_id
    else:
        raise NotAutorized(msg=f"Invalid permissions")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
