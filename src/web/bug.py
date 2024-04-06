from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from service import bug as service

router = APIRouter(prefix = "/bug")

@router.post("/", dependencies=[Depends(validate_token)], status_code=201)  # Creates a bug report
async def create(description: str) -> None:
    return service.create(description, user_id)