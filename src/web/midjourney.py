from fastapi import APIRouter

from model.midjourney import Message

from service import midjourney as service

router = APIRouter(prefix = "/midjourney")

@router.post("/webhook", status_code=201)
async def webhook(message: Message) -> None:
    return service.webhook(message)