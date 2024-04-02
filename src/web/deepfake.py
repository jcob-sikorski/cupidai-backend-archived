import os
from pydantic import UUID4

from fastapi import APIRouter, HTTPException, Depends

from model.deepfake import Deepfake
from web.user import oauth2_dep

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import deepfake as service
else:
    from service import deepfake as service
from error import NotAutorized # TODO come up with good names for this one

router = APIRouter(prefix = "/deepfake")

@router.get("/{generation_id}")
def get_status(generation_id: UUID4, token: str = Depends(oauth2_dep)) -> DeepfakeStatus:
    try:
        return service.get_status(generation_id, token)
    except NotAutorized as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

    
@router.get("/")
def get_usage(token: str = Depends(oauth2_dep)) -> DeepfakeUsage:
    try:
        return service.get_usage(token)
    except NotAutorized as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def generate(deepfake: Deepfake, token: str = Depends(oauth2_dep)) -> UUID4:
    # TODO we should modify this because user can either get UUID or he can get the message that he doesn't have priviliges to generate new image
    try:
        # TODO few layers below we should check if the user with the token has permissions to generate new image return the status
        return service.generate(deepfake, token)
    except NotAutorized as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.post("/", status_code=201)
def webhook(deepfake_status: DeepfakeStatus) -> None:
    # TODO we should modify this because user can either get UUID or he can get the message that he doesn't have priviliges to generate new image
    try:
        # TODO few layers below we should check if the user with the token has permissions to generate new image return the status
        return service.webhook(deepfake_status) 
    except NotAutorized as exc:
        raise HTTPException(status_code=409, detail=exc.msg)