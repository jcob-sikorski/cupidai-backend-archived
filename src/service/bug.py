from fastapi import APIRouter, Depends

import data.bug as data

from model.bug import Bug
from model.user import User

def report_bug(description: str, user) -> None:
    return data.report_bug(description, user)