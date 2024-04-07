from fastapi import APIRouter, Depends



from service import social_account as service

from model.social_account import SocialAccount

router = APIRouter(prefix="/social-account")

# Protected endpoint
@router.post("/", status_code=201)  # Creates a new social account
async def create(social_account: SocialAccount, user_id: str) -> None:
    return service.create(social_account, user_id)

# Protected endpoint
@router.patch("/{account_id}", status_code=200)  # Updates social account information
async def update(account_id: str, social_account: SocialAccount, user_id: str) -> None:
    return service.update(account_id, social_account, user_id)

# Protected endpoint
@router.get("/", status_code=200)  # Retrieves all social accounts
async def get(user_id: str) -> None:
    return service.get(user_id)
