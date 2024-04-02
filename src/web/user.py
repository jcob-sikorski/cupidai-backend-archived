from typing import Optional
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import (
    OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from starlette.status import HTTP_401_UNAUTHORIZED
from model.user import User
from service import user as service

ACCESS_TOKEN_EXPIRE_MINUTES = 15

router = APIRouter(prefix = "/user")

# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# return an access token.
oauth2_dep = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="JWT"
)

def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_dep)) -> User:
    user = service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# This endpoint is directed to by any call that has the
# oauth2_dep() dependency:
@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Get username and password from OAuth form,
        return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.name}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create-user")
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Optional[User]:
    """Create a new user"""
    created_user = service.create_user(form_data.username, form_data.password)
    return created_user