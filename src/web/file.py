from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from tempfile import SpooledTemporaryFile

router = APIRouter(prefix="/file")

# Function to download a specific file by its ID
@router.get("/{file_id}", status_code=200)
async def download_file(file_id: str):
    # Dummy implementation: Replace this with actual file retrieval logic
    # Here, we just create a dummy file content for demonstration purposes
    async def generate():
        yield b"Dummy file content for file_id: " + file_id.encode()
    return StreamingResponse(generate(), media_type="application/octet-stream")

# Function to upload a new file
@router.post("/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    # Dummy implementation: Replace this with actual file processing logic
    # Here, we just print the file name and size
    print("Uploaded File Name:", file.filename)
    print("Uploaded File Size:", file.file._file._chunk_size)  # Access chunk size for demonstration
    return {"filename": file.filename}

