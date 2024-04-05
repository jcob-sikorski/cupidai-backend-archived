import data.history as data

def update(domain: str, user_id: str) -> None:
    return data.update(domain, user_id)

def get(user_id: str) -> None:
    return data.get(user_id)