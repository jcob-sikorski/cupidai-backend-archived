from fastapi import APIRouter, Depends, HTTPException

from typing import Annotated, Optional, List, Tuple

from pydantic import BaseModel

from model.account import Account
from model.ai_verification import Prompt, SocialAccount
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

@router.post("/add-account", status_code=201)  # Adds new account with a prompt
async def add_account(social_account: SocialAccount,
                      prompt: Prompt,
                      user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[Tuple[SocialAccount, Prompt]]:
    return service.add_account(social_account,
                               prompt,
                               user)


@router.patch("/account", status_code=200)  # Updates social account information
async def update(social_account: SocialAccount,
                 _: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.update_account(social_account)


@router.get("/accounts", status_code=200)  # Retrieves all social accounts
async def get(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[List[SocialAccount]]:
    return service.get_account(user)


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
