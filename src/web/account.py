from fastapi import APIRouter, Depends

from service import account as service

router = APIRouter(prefix="/account")

# Protected endpoint
@router.post("/signup", status_code=200)  # Creates new user account
async def create(email: str, user_id: str) -> None:
    return service.create(email, user_id)

# TODO: this should be run to map the referral id to the new user_id
#       then in the webhook we update the referral model
# Protected endpoint
@router.post("/signup/ref", status_code=200)  # Creates new user account
async def create_ref(ref: str) -> None:
    return service.create_ref(ref)

# Protected endpoint
@router.patch("/email", status_code=200)  # Changes the account's email
async def change_email(email: str, user_id: str) -> None:
    return service.change_email(email, user_id)

# Protected endpoint
@router.get("/", status_code=200)  # Retrieves account details
async def get(user_id: str) -> None:
    return service.get(user_id)

# Protected endpoint
@router.patch("/profile-picture", status_code=200)  # Changes the profile picture
async def change_profile_picture(profile_uri: str, user_id: str) -> None:
    return service.change_profile_picture(profile_uri, user_id)

# Protected endpoint
@router.delete("/", status_code=204)  # Deletes the account, status 204 for No Content
async def delete(user_id: str) -> None:
    return service.delete(user_id)
