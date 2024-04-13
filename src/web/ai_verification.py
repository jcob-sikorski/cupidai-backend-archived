from fastapi import APIRouter, Depends, HTTPException
from typing import List

from model.ai_verification import Prompt
from model.midjourney import Message, Response

from service import ai_verification as service

router = APIRouter(prefix="/ai-verification")

# TODO: this should make request to our custo facefusion server
# Protected endpoint
@router.post("/faceswap", status_code=201)  # Initiates a face swap
async def faceswap(source_uri: str, target_uri: str, user_id: str) -> None:
    return await service.faceswap(source_uri, target_uri, user_id)

# Protected endpoint
@router.post("/imagine", status_code=201)  # Initiates an imagination process
async def imagine(prompt: Prompt, user_id: str) -> None:
    return await service.imagine(prompt, user_id)

# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves job history
async def get_history(user_id: str) -> List[Message]:
    history = service.get_history(user_id)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

# TODO: we should test this out once we buy a plan
# Protected endpoint
@router.post("/action", status_code=201)  # Initiates a specific action
async def action(message_id: str, button: str, user_id: str) -> None:
    return await service.action(message_id, button, user_id)

# Protected endpoint
@router.delete("/message/{message_id}", status_code=204)  # Cancels a specific job, status 204 for No Content
async def cancel_job(message_id: str, user_id: str) -> None:
    return await service.cancel_job(message_id, user_id)
