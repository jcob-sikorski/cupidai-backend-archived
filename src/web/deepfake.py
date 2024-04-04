from fastapi import APIRouter, Depends

from model.deepfake import Deepfake
from model.user import User

from service import deepfake as service

from web.user import get_current_user

router = APIRouter(prefix = "/deepfake")

@router.post("/generate", status_code=201)  # Generates a new resource
async def generate(deepfake: Deepfake, user: User = Depends(get_current_user)) -> None:
    return service.generate(deepfake, user)

@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user: User = Depends(get_current_user)) -> None:
    return service.get_history(user)