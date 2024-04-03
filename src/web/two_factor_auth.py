from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/2fa")

@router.post("/enable", status_code=201)  # Enables two-factor authentication

@router.get("/qr-code", status_code=200)  # Generates QR code for two-factor authentication setup

@router.post("/generate-code", status_code=201)  # Generates a two-factor authentication code