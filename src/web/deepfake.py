from fastapi import APIRouter, BackgroundTasks

from model.deepfake import Deepfake

from service import deepfake as service

router = APIRouter(prefix="/deepfake")

# TODO: we must communicate with our custom facefusion running on rnupod
#       because users must be able to pass necessary params for the model
# Protected endpoint
@router.post("/generate", status_code=201)  # Generates a new resource
async def generate(deepfake: Deepfake, user_id: str, background_tasks: BackgroundTasks) -> None:
    return service.generate(deepfake, user_id, background_tasks)

# TESTING DONE ✅
# Protected endpoint
@router.get("/history", status_code=200)  # Retrieves history
async def get_history(user_id: str) -> None:
    return service.get_history(user_id)
