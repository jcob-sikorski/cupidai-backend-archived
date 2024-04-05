from typing import List

import data.team as data

def accept(member_id: str, user_id: str) -> None:
    return data.accept(member_id, user_id)

def invite(email: str, user_id: str) -> None:
    # TODO: do the invite here using loops

def update_permissions(permissions: List[str], member_id: str, user_id: str) -> None:
    return data.update_permissions(permissions, member_id, user_id)

def delete(member_id: str, user_id: str) -> None:
    return data.delete(member_id, user_id)

def transfer_ownership(member_id: str, user_id: str) -> None:
    return data.transfer_ownership(member_id, user_id)

def get_members(user_id: str) -> None:
    return data.get_members(user_id)

def get_activity(user_id: str) -> None:
    return data.get_activity(user_id)

def disband(user_id: str) -> None:
    return data.disband(user_id)

def leave(user_id: str) -> None:
    return data.leave(user_id)

def owner(user_id: str) -> None:
    return data.owner(user_id)