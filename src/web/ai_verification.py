from fastapi import APIRouter, Depends

router = APIRouter(prefix = "/ai-verification")

@router.post("/faceswap", status_code=201)  # Initiates a face swap

@router.post("/imagine", status_code=201)  # Initiates an imagination process

@router.get("/history", status_code=200)  # Retrieves job history

@router.post("/action", status_code=201)  # Initiates a specific action

@router.delete("/jobs/{job_id}", status_code=204)  # Cancels a specific job, status 204 for No Content