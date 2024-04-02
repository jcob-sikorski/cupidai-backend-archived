import os
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse
from model.user import User
from web.user import get_current_user
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import explorer as service
else:
    from service import explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix = "/explorer")
    
@router.get("/{uri}")
def download_one(uri, user: User = Depends(get_current_user)) -> StreamingResponse:
        return service.download_one(uri, user)

@router.post("/", status_code=201)
def upload_one(file: UploadFile, user: User = Depends(get_current_user)) -> UploadStatus:
    return service.upload_one(file, user)
