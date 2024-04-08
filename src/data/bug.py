from model.bug import Bug

from .init import bug_col

from datetime import datetime

# TESTING DONE ✅
def create(description: str, user_id: str) -> None:
    bug = Bug(user_id=user_id, description=description, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    result = bug_col.insert_one(bug.dict())

    return result.inserted_id is not None