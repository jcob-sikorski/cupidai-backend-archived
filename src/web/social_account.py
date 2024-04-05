from fastapi import APIRouter, Depends

from auth import VerifyToken

from service import social_account as service

from model.social_account import SocialAccount

router = APIRouter(prefix = "/social-account")

auth = VerifyToken()

@router.post("/", status_code=201)  # Creates a new social account
async def create(social_account: SocialAccount, user_id: str = Depends(auth.verify)) -> None:
    return service.create(social_account, user_id)

@router.patch("/{account_id}", status_code=200)  # Updates social account information
async def update(social_account: SocialAccount, user_id: str = Depends(auth.verify)) -> None:
    return service.update(social_account, user_id)

@router.get("/", status_code=200)  # Retrieves all social accounts
async def get(user_id: str = Depends(auth.verify)) -> None:
    return service.get(user_id)