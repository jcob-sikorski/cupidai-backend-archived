from fastapi import APIRouter, Depends, BackgroundTasks

from typing import Annotated

from model.account import Account
from model.deepfake import Message

from service import account as account_service
from service import deepfake as service

router = APIRouter(prefix="/deepfake")

# TODO: add two webhooks: one for facefusion and second for higher plans' API


# TODO: we should probably somehow make difference between endpoint for higher plans API and our custom one - facefusion

# Protected endpoint
@router.post("/generate", status_code=201)  # Generates a new resource
async def generate(message: Message, user: Annotated[Account, Depends(account_service.get_current_active_user)], background_tasks: BackgroundTasks) -> None:
    return service.generate(message, user, background_tasks)

# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_history(user)
