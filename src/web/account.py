from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from service import account as service

router = APIRouter(prefix = "/account")

@router.patch("/email", dependencies=[Depends(validate_token)], status_code=200)  # Changes the account's email
async def change_email(email: str) -> None:
    return service.change_email(email, user_id)

@router.get("/", dependencies=[Depends(validate_token)], status_code=200)  # Retrieves account details
async def get() -> None:
    # return service.get(user_id)
    return 200

@router.patch("/profile-picture", dependencies=[Depends(validate_token)], status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: str) -> None:
    return service.change_profile_picture(profile_uri, user_id)

@router.delete("/", dependencies=[Depends(validate_token)], status_code=204)  # Deletes the account, status 204 for No Content
async def delete() -> None:
    return service.delete(user_id)