from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from data import account as data

from model.account import Account, Token, TokenData, PasswordReset

import service.email as email_service

import uuid

# to get a string like this run:
# openssl rand -hex 32

# TODO: this should probably stored in env vars just like all other tokens
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = data.get_user(username)

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = data.get_user(username=token_data.username)

    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[Account, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

async def login(form_data: OAuth2PasswordRequestForm) -> Token:
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


def signup(form_data: OAuth2PasswordRequestForm) -> None:
    data.signup(form_data.username, form_data.password)
    
    return login(form_data.username, form_data.password)

def signup_ref(ref: str) -> None:
    return data.signup_ref(ref)

def forgot_password(email: str) -> None:
    user = get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_id = str(uuid.uuid4())

    # TODO for dev purposes use ngrok domain
    password_reset_link = f"https://cupidai.tech/account/new-password/{password_reset_id}"

    now = datetime.now()

    password_reset = PasswordReset(
        reset_id=password_reset_id,
        user_id=user.user_id,
        email=email,
        reset_link=password_reset_link,
        is_used=False,
        created_at=now.strftime("%Y-%m-%d %H:%M:%S")
    )

    data.create_password_reset(password_reset)

    email_service.send(email, 'clv2h2bt800bm1147nw7gtngv', password_reset_link=password_reset_link)

def change_email(email: str, user: Account) -> None:
    return data.change_email(email, user)

# TODO: all of the functions which get user should check if user was disabled
#       btw this function does not do that
def get_by_email(email: str) -> None:
    return data.get_by_email(email)

def change_profile_picture(profile_uri: str, user: Account) -> None:
    return data.change_profile_picture(profile_uri, user)

def delete(user: Account) -> None:
    return data.delete(user)

def get_invite(invite_id: str) -> None:
    return data.get_invite(invite_id)