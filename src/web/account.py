from fastapi import APIRouter, Depends

from service import account as service

from model.account import Account
from model.user import User

from web.user import get_current_user

router = APIRouter(prefix = "/account")

@router.patch("/email", status_code=200)  # Changes the account's email
async def change_email(email: str, account_id: str, user: User = Depends(get_current_user)) -> None:
    return service.change_email(email, account_id, user)

@router.get("/", status_code=200)  # Retrieves account details
async def get(account_id: str, user: User = Depends(get_current_user)) -> None:
    return service.get(account_id, user)

@router.patch("/profile-picture", status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: str, account_id: str, user: User = Depends(get_current_user)) -> None:
    return service.change_profile_picture(profile_uri, account_id, user)

@router.post("/password", status_code=201)  # Saves a new password
async def set_new_password(password: str, account_id: str, user: User = Depends(get_current_user)) -> None:
    return service.set_new_password(password, account_id, user)

@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content
async def delete(account_id: str, user: User = Depends(get_current_user)) -> None:
    return service.delete(account_id, user)

@router.post("/", status_code=201)  # Creates a new account
async def create(account: Account, user: User = Depends(get_current_user)) -> None:
    return service.create(account, user)