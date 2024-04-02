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
def get_status(generation_id: UUID4, _: User = Depends(get_current_user)) -> DeepfakeStatus:
    return service.get_status(generation_id)

    
@router.get("/")
def get_usage(user: User = Depends(get_current_user)) -> DeepfakeUsage:
    return service.get_usage(user)


@router.post("/", status_code=201)
def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> UUID4:
    return service.generate(deepfake, user)


@router.post("/", status_code=201)
def webhook(deepfake_status: DeepfakeStatus) -> None:
    return service.webhook(deepfake_status) 