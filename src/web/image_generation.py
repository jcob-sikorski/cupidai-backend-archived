from fastapi import APIRouter, Depends

from model.image_generation import Settings

from service import image_generation as service

router = APIRouter(prefix="/image-generation")

@router.post("/", status_code=201)
async def generate(settings: Settings, user_id: str) -> None:
    return service.generate(settings, user_id)