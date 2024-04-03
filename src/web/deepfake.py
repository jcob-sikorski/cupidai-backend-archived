from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/deepfake")

@router.post("/webhook", status_code=201)  # Registers a new webhook

@router.post("/generate", status_code=201)  # Generates a new resource

@router.get("/progress", status_code=200)  # Retrieves progress

@router.get("/history", status_code=200)  # Retrieves history