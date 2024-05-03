from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, List

from pydantic import BaseModel

from model.account import Account
from model.ai_verification import Prompt
from model.midjourney import Message

from service import account as account_service
from service import ai_verification as service

router = APIRouter(prefix="/ai-verification")

# class FaceswapRequest(BaseModel):
#     source_uri: str
#     target_uri: str

# @router.post("/faceswap", status_code=201)  # Initiates a face swap
# async def faceswap(req: FaceswapRequest, 
#                    user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
#     return await service.faceswap(req.source_uri,
#                                   req.target_uri,
#                                   user)


@router.post("/imagine", status_code=201)  # Initiates an imagination process
async def imagine(prompt: Prompt, 
                  user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.imagine(prompt, user)


@router.get("/history", status_code=200)  # Retrieves job history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> List[Message]:
    history = service.get_history(user)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history


class ActionRequest(BaseModel):
    messageId: str
    button: str

@router.post("/action", status_code=201)  # Initiates a specific action
async def action(req: ActionRequest, 
                 user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.action(req.messageId, 
                                req.button, 
                                user)


# @router.delete("/message/{messageId}", status_code=204)  # Cancels a specific job, status 204 for No Content
# async def cancel_job(messageId: str, 
#                      user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
#     return await service.cancel_job(messageId, user)
