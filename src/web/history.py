from fastapi import APIRouter, Depends

from auth import VerifyToken

import data.history as data

router = APIRouter(prefix = "/history")

auth = VerifyToken()

@router.get("/", status_code=200)  # Retrieves account details
async def get(user_id: str = Depends(auth.verify)) -> None:
    return data.get(user_id)