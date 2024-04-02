import os
from pydantic import UUID4

from fastapi import APIRouter, HTTPException, Depends

from model.user import User
from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake
from web.user import get_current_user

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import deepfake as service
else:
    from service import deepfake as service
from error import NotAutorized

router = APIRouter(prefix = "/deepfake")

@router.get("/{generation_id}")
def get_status(generation_id: UUID4, user: User = Depends(get_current_user)) -> DeepfakeStatus:
    try:
        return service.get_status(generation_id, user)
    except NotAutorized as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

    
@router.get("/")
def get_usage(user: User = Depends(get_current_user)) -> DeepfakeUsage:
    try:
        return service.get_usage(user)
    except NotAutorized as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> UUID4:
    try:
        return service.generate(deepfake, user)
    except NotAutorized as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.post("/", status_code=201)
def webhook(deepfake_status: DeepfakeStatus) -> None:
    try:
        return service.webhook(deepfake_status) 
    except NotAutorized as exc:
        raise HTTPException(status_code=409, detail=exc.msg)