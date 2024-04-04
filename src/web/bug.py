from fastapi import APIRouter, Depends

from model.bug import Bug
from model.user import User

from service import bug as service

from web.user import get_current_user

router = APIRouter(prefix = "/bug")

@router.post("/", status_code=201)  # Creates a bug report
async def create(description: str, user: User = Depends(get_current_user)) -> None:
    return service.create(description, user)