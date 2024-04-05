from fastapi import APIRouter, Depends

from auth import VerifyToken

from service import bug as service

router = APIRouter(prefix = "/bug")

auth = VerifyToken()

@router.post("/", status_code=201)  # Creates a bug report
async def create(description: str, user_id: str = Depends(auth.verify)) -> None:
    return service.create(description, user_id)