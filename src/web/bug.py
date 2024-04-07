from fastapi import APIRouter, Depends



from service import bug as service

router = APIRouter(prefix="/bug")

# Protected endpoint
@router.post("/", status_code=201)  # Creates a bug report
async def create(description: str, user_id: str) -> None:
    return service.create(description, user_id)
