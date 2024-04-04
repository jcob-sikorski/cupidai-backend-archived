from fastapi import APIRouter, Depends

import data.history as data
from data.user import User

from web.user import get_current_user

router = APIRouter(prefix = "/history")

@router.get("/", status_code=200)  # Retrieves account details
async def get(user: User = Depends(get_current_user)) -> None:
    return data.get(user)