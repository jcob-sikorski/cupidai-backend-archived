import os
from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import explorer as service
else:
    from service import explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix = "/explorer")

@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{uri}")
def get_one(uri, token: str = Depends(oauth2_dep)) -> File:
    try:
        return service.get_one(uri, token)
    except  as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
@router.get("/{uri}")
def download_one(uri, token: str = Depends(oauth2_dep)) -> File:
    try:
        return service.download_one(uri, token)
    except  as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201)
def upload_one(file: File, token: str = Depends(oauth2_dep)) -> UploadStatus:
    try:
        return service.upload_one(file, token)
    except  as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
