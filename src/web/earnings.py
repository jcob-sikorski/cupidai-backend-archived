from fastapi import APIRouter, Depends

from auth import VerifyToken

router = APIRouter(prefix = "/earnings")

auth = VerifyToken()

@router.get("/earnings", status_code=200)  # Retrieves earnings

@router.post("/withdraw", status_code=201)  # Initiates withdrawal