from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from model.deepfake import Deepfake

from service import deepfake as service

router = APIRouter(prefix = "/deepfake")

@router.post("/generate", dependencies=[Depends(validate_token)], status_code=201)  # Generates a new resource
async def generate(deepfake: Deepfake) -> None:
    return service.generate(deepfake, user_id)

@router.get("/history", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves history
async def get_history() -> None:
    return service.get_history(user_id)