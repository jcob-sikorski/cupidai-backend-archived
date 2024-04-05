from model.bug import Bug

from .init import bug_col

from datetime import datetime

def create(description: str, user_id: str) -> None:
    bug = Bug(user_id=user_id, description=description, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    bug_col.insert_one(bug.dict())