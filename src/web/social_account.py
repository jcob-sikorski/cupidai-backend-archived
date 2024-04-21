from fastapi import APIRouter, Depends

from typing import Annotated, List, Optional

from model.account import Account
from model.social_account import SocialAccount

from service import account as account_service
from service import social_account as service

router = APIRouter(prefix="/social-account")

# TESTING DONE ✅

@router.post("/", status_code=201)  # Creates a new social account
async def create(social_account: SocialAccount,
                 user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.create(social_account, user)

# TESTING DONE ✅

@router.patch("/{account_id}", status_code=200)  # Updates social account information
async def update(social_account: SocialAccount, 
                 user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> None:
    return service.update(social_account)

# TESTING DONE ✅

@router.get("/", status_code=200)  # Retrieves all social accounts
async def get(user: Annotated[Account, Depends(account_service.get_current_active_user)]) -> Optional[List[SocialAccount]]:
    return service.get(user)
