from fastapi import APIRouter, Depends

from model.user import User
from model.deepfake import DeepfakeStatus, DeepfakeUsage, Deepfake
from web.user import get_current_user

from service import deepfake as service

router = APIRouter(prefix = "/ai-verification")

@router.post("/text-to-image", status_code=201)
async def text_to_img(, : User = Depends(get_current_user)) -> :
    pass

@router.post("/faceswap", status_code=201)
async def faceswap(, : User = Depends(get_current_user)) -> :
    pass

@router.post("/image-action", status_code=201)
async def image_action(, : User = Depends(get_current_user)) -> :
    pass


@router.post("/cancel-job", status_code=201)
async def cancel_job(, : User = Depends(get_current_user)) -> :
    pass

@router.post("/update-settings", status_code=201)
async def update_settings(, : User = Depends(get_current_user)) -> :
    pass

@router.post("/webhook", status_code=201)
async def webhook(,) -> :
    pass

@router.get("/get-progress")
async def get_progress(, : User = Depends(get_current_user)) -> :
    pass
    

@router.get("/get-settings")
async def get_settings(, : User = Depends(get_current_user)) -> :
    pass
    
@router.get("/download-settings")
async def download_settings(, : User = Depends(get_current_user)) -> :
    pass