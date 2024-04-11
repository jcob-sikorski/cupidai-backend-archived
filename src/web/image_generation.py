from fastapi import APIRouter, Depends

from typing import Dict, List, Optional

from model.image_generation import Settings, Message

import service.image_generation as service

router = APIRouter(prefix="/image-generation")

@router.post("/webhook", status_code=201)
async def webhook(message: Message) -> None:
    print("COMFYUI WEBHOOK ACTIVATED")
    return service.webhook(message)

@router.post("/", status_code=201)
async def generate(settings: Settings, uploadcare_uris: Dict[str, str], user_id: str) -> None:
    return await service.generate(settings, uploadcare_uris, user_id)