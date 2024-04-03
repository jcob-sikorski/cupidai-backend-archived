from fastapi import APIRouter, Depends

from model.user import User
from model.ai_verification import Settings, Prompt, Progress, Response
from web.user import get_current_user

from service import deepfake as service

router = APIRouter(prefix = "/ai-verification")

@router.post("/webhook", status_code=201)
async def webhook(progress: Progress) -> None:
    return service.webhook(progress)

@router.post("/faceswap", status_code=201)
async def faceswap(source_uri: str, target_uri: str, user: User = Depends(get_current_user)) -> Response:
    return service.faceswap(source_uri, target_uri, user)

@router.post("/action", status_code=201)
async def action(button: str, user: User = Depends(get_current_user)) -> Response:
    return service.action(button, user)

# @router.post("/isolate", status_code=201)
# async def webhook(,) -> :
#     pass

@router.post("/cancel-job", status_code=201)
async def cancel_job(, : User = Depends(get_current_user)) -> :
    pass

@router.post("/update-settings", status_code=201)
async def update_settings(settings: Settings, user: User = Depends(get_current_user)) -> :
    return service.update_settings(settings, user)

@router.post("/text-to-image-webhook", status_code=201)
async def text_to_image_webhook(progress: Progress) -> None:
    return service.webhook(progress)

@router.get("/get-progress")
async def get_progress(, : User = Depends(get_current_user)) -> :
    pass

@router.get("/get-settings")
async def get_settings(, : User = Depends(get_current_user)) -> :
    pass
    
@router.get("/download-settings")
async def download_settings(, : User = Depends(get_current_user)) -> :
    pass