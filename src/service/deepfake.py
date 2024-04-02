import data.deepfake as data

from uuid import UUID

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
                "source": "https://ucarecdn.com/7277eac7-216d-4a87-8767-61294eb97374/-/preview/712x1000/",
                "target": "https://ucarecdn.com/dde666f2-2704-413f-9945-13a8fdfb8039/-/preview/701x1000/",
                "keep_fps": False,
                "enhance_face": True
            }
        )

        # The okaris/facefusion model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        for item in output:
            # https://replicate.com/okaris/facefusion/api#output-schema
            print(item)
        # TODO on the successful call of API:
        #       - update deepfake usage
        #       - return generation id to track deepfake status
    else:
        raise NotAutorized(msg=f"Invalid permissions")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
