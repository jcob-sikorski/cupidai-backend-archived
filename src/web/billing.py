from fastapi import APIRouter, Depends, Request

from auth.dependencies import validate_token

from model.billing import Item

import service.billing as service

router = APIRouter(prefix = "/billing")

@router.post('/webhook')
async def webhook(item: Item, request: Request) -> None:
    return service.webhook(item , request)

@router.get("/download-history", dependencies=[Depends(validate_token)], status_code=200)  # Downloads billing history
async def download_history() -> None:
    return service.download_history(user_id)

@router.get("/history", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves billing history
async def get_history(solo: bool) -> None:
    return service.get_history(solo, user_id)

@router.post("/terms-of-service", dependencies=[Depends(validate_token)], status_code=201)  # Accepts terms of service for billing
async def accept_tos() -> None:
    return service.accept_tos(user_id)

@router.get("/current-plan", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves current billing plan
async def get_current_plan() -> None:
    return service.get_current_plan(user_id)