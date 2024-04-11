from data import account as data

def create(email: str, user_id: str) -> None:
    return data.create(email, user_id)

def change_email(email: str, user_id: str) -> None:
    return data.change_email(email, user_id)

def get(user_id: str) -> None:
    return data.get(user_id)

def get_by_email(email: str) -> None:
    return data.get_by_email(email)

def change_profile_picture(profile_uri: str, user_id: str) -> None:
    return data.change_profile_picture(profile_uri, user_id)

def delete(user_id: str) -> None:
    return data.delete(user_id)

def get_invite(invite_id: str) -> None:
    return data.get_invite(invite_id)