from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from model.ai_verification import Prompt

from service import ai_verification as service

router = APIRouter(prefix = "/ai-verification")

@router.post("/faceswap", dependencies=[Depends(validate_token)], status_code=201)  # Initiates a face swap
async def faceswap(source_uri: str, target_uri: str) -> None:
    return service.faceswap(source_uri, target_uri, user_id)

@router.post("/imagine", dependencies=[Depends(validate_token)], status_code=201)  # Initiates an imagination process
async def imagine(prompt: Prompt) -> None:
    return service.imagine(prompt, user_id)

@router.get("/history", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves job history
async def get_history() -> None:
    return service.get_history(user_id)

@router.post("/action", dependencies=[Depends(validate_token)], status_code=201)  # Initiates a specific action
async def action(message_id: str, button: str) -> None:
    return service.action(message_id, button, user_id)

@router.delete("/message/{message_id}", dependencies=[Depends(validate_token)], status_code=204)  # Cancels a specific job, status 204 for No Content
async def cancel_job(message_id: str) -> None:
    return service.cancel_job(message_id, user_id)