from fastapi import APIRouter, Depends

from auth.dependencies import validate_token

from typing import List

from service import team as service

router = APIRouter(prefix = "/team")

# TODO: implement the logic also for the new user
@router.post("/accept/{member_id}/{user_id}", status_code=201)  # Accepts the invite
async def accept(member_id: str, user_id: str) -> None:
    return service.accept(member_id, user_id)

@router.post("/members/invite", dependencies=[Depends(validate_token)], status_code=201)  # Invites a new member
async def invite(email: str) -> None:
    return service.invite(email, user_id)

@router.patch("/members/{member_id}/permissions", dependencies=[Depends(validate_token)], status_code=200)  # Updates permissions of a member
async def update_permissions(permissions: List[str], member_id: str) -> None:
    return service.update_permissions(permissions, member_id, user_id)

@router.delete("/members/{member_id}", dependencies=[Depends(validate_token)], status_code=204)  # Removes a member, status 204 for No Content
async def delete(member_id: str) -> None:
    return service.delete(member_id, user_id)

@router.patch("/ownership", dependencies=[Depends(validate_token)], status_code=200)  # Transfers ownership, status 200 for successful update
async def transfer_ownership(member_id: str) -> None:
    return service.transfer_ownership(member_id, user_id)

@router.get("/members", dependencies=[Depends(validate_token)], status_code=200)  # Lists members, status 200 for OK
async def get_members() -> None:
    return service.get_members(user_id)

@router.get("/members/activity", dependencies=[Depends(validate_token)], status_code=200)  # Lists members activity, status 200 for OK
async def get_activity() -> None:
    return service.get_activity(user_id)

@router.delete("/disband", dependencies=[Depends(validate_token)], status_code=204)  # Disbands the group, status 204 for No Content
async def disband() -> None:
    return service.disband(user_id)

@router.post("/leave", dependencies=[Depends(validate_token)], status_code=200)  # Member initiates leave, status 200 for OK
async def leave() -> None:
    return service.leave(user_id)

@router.get("/owner", dependencies=[Depends(validate_token)], status_code=200)  # Gets the group owner, status 200 for OK
async def owner() -> None:
    return service.owner(user_id)