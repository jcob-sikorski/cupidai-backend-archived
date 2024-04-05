from fastapi import APIRouter, Depends

from auth import VerifyToken

from service import account as service

router = APIRouter(prefix = "/account")

auth = VerifyToken()

@router.patch("/email", status_code=200)  # Changes the account's email
async def change_email(email: str, user_id: str = Depends(auth.verify)) -> None:
    return service.change_email(email, user_id)

@router.get("/", status_code=200)  # Retrieves account details
async def get(user_id: str = Depends(auth.verify)) -> None:
    return service.get(user_id)

@router.patch("/profile-picture", status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: str, user_id: str = Depends(auth.verify)) -> None:
    return service.change_profile_picture(profile_uri, user_id)

@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content
async def delete(user_id: str = Depends(auth.verify)) -> None:
    return service.delete(user_id)