from fastapi import APIRouter, Depends

import data.bug as data

from model.bug import Bug
from model.user import User

from .init import bug_col

from datetime import datetime

def report_bug(description: str, user: User) -> None:
    bug = Bug(account_id=user.id, description=description, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    bug_col.insert_one(bug.dict())