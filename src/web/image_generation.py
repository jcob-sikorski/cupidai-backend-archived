from fastapi import APIRouter, Depends

from model.image_generation import Settings, Message

import service.image_generation as service

router = APIRouter(prefix="/image-generation")

@router.post("/webhook", status_code=201)
async def webhook(message: Message) -> None:
    print("COMFYUI WEBHOOK ACTIVATED")
    return service.webhook(message)

@router.post("/", status_code=201)
async def generate(settings: Settings, user_id: str) -> None:
    return await service.generate(settings, user_id)