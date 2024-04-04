from fastapi import APIRouter, Depends

from model.ai_verification import Prompt
from model.user import User

from service import ai_verification as service

from web.user import get_current_user

router = APIRouter(prefix = "/ai-verification")

@router.post("/faceswap", status_code=201)  # Initiates a face swap
async def faceswap(source_uri: str, target_uri: str, user: User = Depends(get_current_user)) -> None:
    return service.faceswap(source_uri, target_uri, user)

@router.post("/imagine", status_code=201)  # Initiates an imagination process
async def imagine(prompt: Prompt, user: User = Depends(get_current_user)) -> None:
    return service.imagine(prompt, user)

@router.get("/history", status_code=200)  # Retrieves job history
async def get_history(user: User = Depends(get_current_user)) -> None:
    return service.get_history(user)

@router.post("/action", status_code=201)  # Initiates a specific action
async def action(message_id: str, button: str, user: User = Depends(get_current_user)) -> None:
    return service.action(message_id, button, user)

@router.delete("/message/{message_id}", status_code=204)  # Cancels a specific job, status 204 for No Content
async def cancel_job(message_id: str, user: User = Depends(get_current_user)) -> None:
    return service.cancel_job(message_id, user)