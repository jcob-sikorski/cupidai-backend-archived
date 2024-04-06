from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

import data.history as data

router = APIRouter(prefix = "/history")

@router.get("/", status_code=200)  # Retrieves account details
async def get() -> None:
    return data.get(user_id)