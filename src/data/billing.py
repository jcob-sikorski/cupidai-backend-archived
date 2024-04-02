from typing import Optional

from model.user import User
from model.billing import Plan, UserPlan

from .init import plan_col, user_plan_col

def get_current_plan(user: User) -> Optional[Plan]:
    result = user_plan_col.find_one({"user_id": user.id})
    if result is not None:
        user_plan = UserPlan(**result)
        result = plan_col.find_one({"name": user_plan.name})

        if result is not None:
            return Plan(**result)

    return None
