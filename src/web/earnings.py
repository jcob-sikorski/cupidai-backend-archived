from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

router = APIRouter(prefix = "/earnings")

# @router.get("/earnings", status_code=200)  # Retrieves earnings

# @router.post("/withdraw", status_code=201)  # Initiates withdrawal