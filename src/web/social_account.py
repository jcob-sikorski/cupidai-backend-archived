from fastapi import APIRouter, Depends

from service import social_account as service

from model.social_account import SocialAccount
from model.user import User

from web.user import get_current_user

router = APIRouter(prefix = "/social-account")

@router.post("/", status_code=201)  # Creates a new social account
async def create(social_account: SocialAccount, user: User = Depends(get_current_user)) -> None:
    return service.create(social_account, user)

@router.patch("/{account_id}", status_code=200)  # Updates social account information
async def update(social_account: SocialAccount, user: User = Depends(get_current_user)) -> None:
    return service.update(social_account, user)

@router.get("/", status_code=200)  # Retrieves all social accounts
async def get(user: User = Depends(get_current_user)) -> None:
    return service.get(user)