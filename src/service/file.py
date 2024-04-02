import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile
from pathlib import path
from typing import Generator
from fastapi.responses import StreamingResponse
from model.user import User
from web.user import get_current_user
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import explorer as service
else:
    from service import explorer as service
from error import Duplicate, Missing

def gen_file(path: str) -> Generator:
    with open(file=path, mode="rb") as file:
        yield file.read()
    
def download_one(uri, user: User = Depends(get_current_user)) -> StreamingResponse:
    gen_expr = gen_file(file_path=path)
    response = StreamingResponse(
        content=gen_expr,
        status_code=200,
    )
    return response

def upload_one(file: UploadFile, user: User = Depends(get_current_user)) -> UploadStatus:
    pass