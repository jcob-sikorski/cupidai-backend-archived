import data.deepfake as data

from pydantic import UUID4

from fastapi import Depends

from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake

from model.user import User

from error import NotAutorized

def get_status(generation_id: UUID4) -> DeepfakeStatus:
    return data.get_status(generation_id)
    

def get_usage(user: User) -> DeepfakeUsage:
    return data.get_usage(user)


def generate(deepfake: Deepfake, user: User) -> UUID4:
    if data.has_permissions(user):
        # TODO call here the runpod API
        pass
    else:
        raise NotAutorized(msg=f"Invalid permissions")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
