from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/team")

@router.patch("/email", status_code=200)  # Changes the account's email

@router.get("/", status_code=200)  # Retrieves account details

@router.patch("/profile-picture", status_code=200)  # Changes the profile picture

@router.post("/password", status_code=201)  # Saves a new password

@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content

@router.post("/", status_code=201)  # Creates a new account