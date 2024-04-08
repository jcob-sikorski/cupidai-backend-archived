import data.history as data

# TESTING DONE ✅
def update(domain: str, user_id: str) -> None:
    return data.update(domain, user_id)

# TESTING DONE ✅
def get(user_id: str) -> None:
    return data.get(user_id)