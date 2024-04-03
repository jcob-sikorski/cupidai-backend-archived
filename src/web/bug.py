from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/bug")

@router.post("/", status_code=201)  # Creates a bug report