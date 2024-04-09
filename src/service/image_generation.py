from fastapi import APIRouter, Depends

from model.image_generation import Settings

from comfyui import generate_workflow

def generate(settings: Settings, user_id: str) -> None:
    # 1. based on the json settings create the request using the compiler for json
    workflow_json = generate_workflow(settings)

    pass