from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from model.account import Account
from model.ai_verification import Prompt
from model.midjourney import Message

from service import account as account_service
from service import ai_verification as service

router = APIRouter(prefix="/ai-verification")

# TODO: we should test this out once we buy a plan
# Protected endpoint
@router.post("/faceswap", status_code=201)  # Initiates a face swap
async def faceswap(source_uri: str, target_uri: str, user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.faceswap(source_uri, target_uri, user)

# TODO: we should test this out once we buy a plan
# Protected endpoint
@router.post("/imagine", status_code=201)  # Initiates an imagination process
async def imagine(prompt: Prompt, user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.imagine(prompt, user)

# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves job history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> List[Message]:
    history = service.get_history(user)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

# TODO: we should test this out once we buy a plan
# Protected endpoint
@router.post("/action", status_code=201)  # Initiates a specific action
async def action(message_id: str, button: str, user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.action(message_id, button, user)

# TODO: we should test this out once we buy a plan
# Protected endpoint
@router.delete("/message/{message_id}", status_code=204)  # Cancels a specific job, status 204 for No Content
async def cancel_job(message_id: str, user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.cancel_job(message_id, user)
