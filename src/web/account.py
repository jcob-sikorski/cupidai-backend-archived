from typing import Annotated, Optional

from fastapi import Depends, APIRouter, Path, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from model.account import Account, Token

from service import account as service

router = APIRouter(prefix="/account")

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await service.login(form_data)

# TODO: email and username should be unique
@router.post("/signup")
async def signup(email: str,
                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await service.signup(email, form_data)


@router.post("/signup-ref")
async def signup_ref(referral_id: str, 
                     email: str,
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await service.signup_ref(referral_id, email, form_data)


@router.post("/reset-password-request", status_code=200)
async def reset_password_request(password_reset_id: str, 
                                 password: str) -> None:
    return service.reset_password_request(password_reset_id, password)


@router.post("/reset-password", status_code=200)
async def reset_password(email: dict) -> None:
    email = email.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email field is required")
    
    return service.reset_password(email)

# TODO: this should be run to map the referral id to the new user_id
#       then in the webhook we update the referral model

@router.post("/signup/ref", status_code=200)  # Creates new user account
async def signup_ref(ref: str) -> None:
    return await service.signup_ref(ref)

# TODO: we should do authentication of new email

@router.patch("/email", status_code=200)  # Changes the account's email
async def change_email(email: dict,
                       user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    email = email.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email field is required")
    return service.change_email(email, user)


@router.get("/", response_model=Account)
async def get(user: Annotated[Account, Depends(service.get_current_active_user)]) -> Optional[Account]:
    user_without_password = Account(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            profile_uri=user.profile_uri,
            disabled=user.disabled
        )
    
    return user_without_password


@router.patch("/profile-picture", status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: dict, 
                                 user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    
    profile_uri = profile_uri.get("profile_uri")
    if not profile_uri:
        raise HTTPException(status_code=400, detail="Profile URI is required")
    
    return service.change_profile_picture(profile_uri, user)


@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content
async def delete(user: Annotated[Account, Depends(service.get_current_active_user)]) -> None:
    return service.delete(user)
