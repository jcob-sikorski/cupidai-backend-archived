from collections import Counter, defaultdict
import data.deepfake as data

from pydantic import UUID4

from fastapi import Depends

from web.user import oauth2_dep

from error import NotAutorized

def get_status(generation_id: UUID4, token: str = Depends(oauth2_dep)) -> DeepfakeStatus:
    if authed(token):
        return data.get_status(generation_id)
    else:
        raise NotAutorized(msg=f"Token expired")
    

def get_usage(deepfake: Deepfake, token: str = Depends(oauth2_dep)) -> DeepfakeUsage:
    if authed(token):
        return data.get_usage(deepfake)
    else:
        raise NotAutorized(msg=f"Token expired")


def generate(deepfake: Deepfake, token: str = Depends(oauth2_dep)) -> UUID4:
    if authed(token):
        if data.has_permissions(token):
            # TODO call here the runpod API
        
            return service.generate(deepfake, token)
        else:
            raise NotAutorized(msg=f"Invalid permissions")
    else:
        raise NotAutorized(msg=f"Token expired")
   
   
def webhook(deepfake_status: DeepfakeStatus) -> None:
    data.webhook(deepfake_status)
