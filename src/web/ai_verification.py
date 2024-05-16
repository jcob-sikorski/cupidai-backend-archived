from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, Optional, List

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


class ActionRequest(BaseModel):
    messageId: str
    button: str

@router.post("/action", status_code=201)  # Initiates a specific action
async def action(req: ActionRequest, 
                 user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return await service.action(req.messageId, 
                                req.button, 
                                user)

@router.post("/prompt", status_code=201)  # Creates a new prompt
async def create_prompt(prompt: Prompt,
                        user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Prompt]:
    return service.create_prompt(prompt, 
                                 user)


@router.patch("/prompt", status_code=200)  # Updates prompt information
async def update_prompt(prompt: Prompt,
                        _: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.update_prompt(prompt)


@router.get("/prompts", status_code=200)  # Retrieves all prompts
async def get_prompts(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[List[Prompt]]:
    return service.get_prompts(user)


@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> List[Message]:
    return service.get_history(user)


# @router.delete("/message/{messageId}", status_code=204)  # Cancels a specific job, status 204 for No Content
# async def cancel_job(messageId: str, 
#                      user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
#     return await service.cancel_job(messageId, user)
