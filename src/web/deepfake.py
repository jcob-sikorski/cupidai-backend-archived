from fastapi import APIRouter, Depends

from auth import VerifyToken

from model.deepfake import Deepfake

from service import deepfake as service

router = APIRouter(prefix = "/deepfake")

auth = VerifyToken()

@router.post("/generate", status_code=201)  # Generates a new resource
async def generate(deepfake: Deepfake, user_id: str = Depends(auth.verify)) -> None:
    return service.generate(deepfake, user_id)

@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user_id: str = Depends(auth.verify)) -> None:
    return service.get_history(user_id)