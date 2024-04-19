from fastapi import APIRouter, Depends, BackgroundTasks

from typing import Annotated

from model.account import Account
from model.deepfake import Deepfake

from service import account as account_service
from service import deepfake as service

router = APIRouter(prefix="/deepfake")

# Protected endpoint
@router.post("/generate", status_code=201)  # Generates a new resource
async def generate(deepfake: Deepfake, user: Annotated[Account, Depends(account_service.get_current_active_user)], background_tasks: BackgroundTasks) -> None:
    return service.generate(deepfake, user, background_tasks)

# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_history(user)
