import datetime as datetime_outer
from datetime import datetime as datetime_inner
import os
from jose import jwt
from model.user import User
from data import user as data
from typing import Optional
from passlib.context import CryptContext

TOKEN_EXPIRES = 15 # minutes

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hash: str) -> bool:
    """Hash <plain> and compare with <hash> from the database"""
    return pwd_context.verify(plain, hash)


def get_hash(plain: str) -> str:
    """Return the hash of a <plain> string"""
    return pwd_context.hash(plain)


def get_jwt_username(token:str) -> Optional[str]:
    """Return username from JWT access <token>"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username


def get_current_user(token: str) -> Optional[User]:
    """Decode an OAuth access <token> and return the User"""
    if not (username := get_jwt_username(token)):
        return None
    if (user := lookup_user(username)):
        return user
    return None
    

def lookup_user(name: str) -> Optional[User]:
    """Return a matching User fron the database for <name>"""
    if (user := data.get_user(name)):
        return user
    return None


def auth_user(name: str, plain: str) -> Optional[User]:
    """Authenticate user <name> and <plain> password"""
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(data: dict,
    expires: Optional[datetime_outer.timedelta] = None
):
    """Return a JWT access token"""
    src = data.copy()
    now = datetime_inner.utcnow()
    expires = expires or datetime_outer.timedelta(minutes=TOKEN_EXPIRES)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(name: str, plain: str) -> Optional[User]:
    hash = get_hash(plain)
    if (new_user := data.create_user(name, hash)):
        return new_user
    return None