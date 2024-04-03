from fastapi import APIRouter, Depends

from model.user import User
from model.deepfake import Deepfake
from web.user import get_current_user

from service import deepfake as service

router = APIRouter(prefix = "/deepfake")

@router.get("/get-status/{deepfake_id}")
async def get_status(deepfake_id: str, _: User = Depends(get_current_user)) -> Deepfake:
    return service.get_status(deepfake_id)


@router.post("/generate", status_code=201)
async def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> str:
    return service.generate(deepfake, user)