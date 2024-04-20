from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException

from pydantic import BaseModel

from typing import Annotated

from model.account import Account

from service import account as account_service
from service import deepfake as service

import requests

router = APIRouter(prefix="/deepfake")

@router.post("/webhook", status_code=200)
async def webhook(response: dict) -> None:
    print("WEBHOOK ACTIVATED")
    print(response)
    status_code = service.webhook(response)

    if status_code == 200:
        return
    else:
        raise HTTPException(status_code=400, detail="Invalid signature")

class GenerateRequest(BaseModel):
    source_uri: str
    target_uri: str
    modify_video: str

# Protected endpoint
@router.post("/generate", status_code=201)
async def generate(req: GenerateRequest,
                   user: Annotated[Account, Depends(account_service.get_current_active_user)], 
                   background_tasks: BackgroundTasks) -> None:

    return service.generate(req.source_uri, 
                            req.target_uri, 
                            req.modify_video, 
                            user, 
                            background_tasks)


# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.get_history(user)
