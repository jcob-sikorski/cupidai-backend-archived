from typing import Optional

from model.user import User
from model.billing import Plan, UserPlan

from data.user import get_user

from .init import plan_col, user_plan_col

def get_current_plan(user: User) -> Optional[Plan]:
    user = get_user(user.name)

    result = user_plan_col.find_one({"_id": user._id})
    if result is not None:
        user_plan = UserPlan(**result)
        result = plan_col.find_one({"name": user_plan.name})

        if result is not None:
            return Plan(**result)

    return None
