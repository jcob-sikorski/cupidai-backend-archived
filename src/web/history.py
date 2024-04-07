from fastapi import APIRouter, Depends



import data.history as data

router = APIRouter(prefix="/history")

# Protected endpoint
@router.get("/", status_code=200)  # Retrieves account details
async def get(user_id: str) -> None:
    return data.get(user_id)
