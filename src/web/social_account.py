from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/social-account")

@router.post("/", status_code=201)  # Creates a new social account

@router.patch("/{account_id}", status_code=200)  # Updates social account information

@router.get("/", status_code=200)  # Retrieves all social accounts
