from fastapi import APIRouter, Depends

from auth import VerifyToken

router = APIRouter(prefix = "/team")

auth = VerifyToken()

@router.post("/members/invite", status_code=201)  # Invites a new member

@router.post("/members/{member_id}/roles", status_code=201)  # Adds a role to a member

@router.delete("/members/{member_id}", status_code=204)  # Removes a member, status 204 for No Content

@router.patch("/ownership", status_code=200)  # Transfers ownership, status 200 for successful update

@router.get("/members", status_code=200)  # Lists members, status 200 for OK

@router.post("/members/{member_id}/activity", status_code=201)  # Logs member activity

@router.delete("/disband", status_code=204)  # Disbands the group, status 204 for No Content

@router.post("/leave", status_code=200)  # Member initiates leave, status 200 for OK

@router.get("/owner", status_code=200)  # Gets the group owner, status 200 for OK
