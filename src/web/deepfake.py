from uuid import UUID

from fastapi import APIRouter, Depends

from model.user import User
from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake
from web.user import get_current_user

from service import deepfake as service

router = APIRouter(prefix = "/deepfake")

@router.get("/get-status/{generation_id}")
async def get_status(generation_id: UUID, _: User = Depends(get_current_user)) -> DeepfakeStatus:
    return service.get_status(generation_id)

    
@router.get("/get-usage")
async def get_usage(user: User = Depends(get_current_user)) -> DeepfakeUsage:
    return service.get_usage(user)


@router.post("/generate", status_code=201)
async def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> UUID:
    return service.generate(deepfake, user)


@router.post("/webhook", status_code=201)
async def webhook(deepfake_status: DeepfakeStatus) -> None:
    return service.webhook(deepfake_status)