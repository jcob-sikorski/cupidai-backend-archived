from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/file")

@router.get("/{file_id}", status_code=200)  # Downloads a specific file by its ID

@router.post("/", status_code=201)  # Uploads a new file