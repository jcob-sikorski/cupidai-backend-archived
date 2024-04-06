from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from service import social_account as service

from model.social_account import SocialAccount

router = APIRouter(prefix = "/social-account")

@router.post("/", dependencies=[Depends(validate_token)], status_code=201)  # Creates a new social account
async def create(social_account: SocialAccount) -> None:
    return service.create(social_account, user_id)

@router.patch("/{account_id}", dependencies=[Depends(validate_token)], status_code=200)  # Updates social account information
async def update(social_account: SocialAccount) -> None:
    return service.update(social_account, user_id)

@router.get("/", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves all social accounts
async def get() -> None:
    return service.get(user_id)