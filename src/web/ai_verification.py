from fastapi import APIRouter, Depends

from model.user import User
from model.ai_verification import Settings, Prompt, Progress, Response
from web.user import get_current_user

from service import ai_verification as service

router = APIRouter(prefix = "/ai-verification")

@router.post("/webhook", status_code=201)
async def webhook(progress: Progress) -> None:
    return service.webhook(progress)


@router.post("/imagine", status_code=201)
async def imagine(prompt: Prompt, user: User = Depends(get_current_user)) -> Response:
    return service.imagine(prompt, user)


@router.post("/faceswap", status_code=201)
async def faceswap(source_uri: str, target_uri: str, user: User = Depends(get_current_user)) -> Response:
    return service.faceswap(source_uri, target_uri, user)


@router.post("/action", status_code=201)
async def action(message_id: str, button: str, user: User = Depends(get_current_user)) -> Response:
    return service.action(message_id, button, user)

# @router.post("/isolate", status_code=201)
# async def webhook(,) -> :
#     pass

@router.post("/cancel-job", status_code=201)
async def cancel_job(message_id: str, user: User = Depends(get_current_user)) -> Response:
    return service.cancel_job(message_id, user)

# @router.post("/update-settings", status_code=201)
# async def update_settings(settings: Settings, user: User = Depends(get_current_user)) -> :
#     return service.update_settings(settings, user)

# @router.get("/get-settings")
# async def get_settings(user: User = Depends(get_current_user)) -> :
#     pass
    
# @router.get("/download-settings")
# async def download_settings(, : User = Depends(get_current_user)) -> :
#     pass

# @router.get("/get-progress")
# async def get_progress(, : User = Depends(get_current_user)) -> :
#     pass