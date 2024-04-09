from fastapi import Depends

from error import NotAuthorized

from comfyui.ModelInterface import generate_workflow

from model.image_generation import Settings

import service.billing as billing_service

def generate(settings: Settings, user_id: str) -> None:
    if billing_service.has_permissions('image_generation', user_id):
        workflow_json = generate_workflow(settings)

        # TODO: update statuses of the image generation in the db
        #       when the request got sent

        # TODO: update the usage after a successful run
    else:
        raise NotAuthorized(msg=f"Invalid permissions")

    # TODO: send the post request to the runpod server
    #       and use the functions to update statuses, usage etc.
    #       like in the deepfake and image verification
    pass