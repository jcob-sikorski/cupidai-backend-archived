from fastapi import APIRouter

from model.mdj_progress import Progress

from service import ai_verification as service

router = APIRouter(prefix = "/mdj-progress")

@router.post("/webhook", status_code=201)
async def webhook(progress: Progress) -> None:
    return service.webhook(progress)