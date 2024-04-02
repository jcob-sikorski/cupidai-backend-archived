from uuid import UUID

from fastapi import APIRouter, Depends

from model.user import User
from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake
from web.user import get_current_user

from service import deepfake as service
from error import NotAutorized

router = APIRouter(prefix = "/deepfake")

@router.get("/{generation_id}")
def get_status(generation_id: UUID, _: User = Depends(get_current_user)) -> DeepfakeStatus:
    return service.get_status(generation_id)

    
@router.get("/")
def get_usage(user: User = Depends(get_current_user)) -> DeepfakeUsage:
    return service.get_usage(user)


@router.post("/", status_code=201)
def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> UUID:
    return service.generate(deepfake, user)


@router.post("/", status_code=201)
def webhook(deepfake_status: DeepfakeStatus) -> None:
    return service.webhook(deepfake_status) 