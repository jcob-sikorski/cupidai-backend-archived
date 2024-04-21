from typing import Annotated, Optional

from fastapi import Depends, APIRouter, Path
from fastapi.security import OAuth2PasswordRequestForm

from model.account import Account, Token

from service import account as service

router = APIRouter(prefix="/account")

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await service.login(form_data)

@router.post("/signup")
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await service.signup(form_data)

@router.post("/reset-password-request/{password_reset_id}", status_code=200)
async def reset_password_request(password_reset_id: str = Path(...)) -> None:
    return service.reset_password_request(password_reset_id)


@router.post("/reset-password", status_code=200)
async def reset_password(email: str) -> None:
    return service.reset_password(email)

# TODO: this should be run to map the referral id to the new user_id
#       then in the webhook we update the referral model
# Protected endpoint
@router.post("/signup/ref", status_code=200)  # Creates new user account
async def signup_ref(ref: str) -> None:
    return service.signup_ref(ref)

# Protected endpoint
@router.patch("/email", status_code=200)  # Changes the account's email
async def change_email(email: str, 
                       user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    return service.change_email(email, user) # TODO: we should do authentication of new email

# Protected endpoint
@router.get("/", response_model=Account)
async def get(user: Annotated[Account, Depends(service.get_current_active_user)]) -> Optional[Account]:
    return user

# Protected endpoint
@router.patch("/profile-picture", status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: str, 
                                 user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    return service.change_profile_picture(profile_uri, user)

# Protected endpoint
@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content
async def delete(user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    return service.delete(user)
