from typing import Optional

from model.billing import Plan, UserPlan

from .init import plan_col, user_plan_col

def get_current_plan(user_id: str) -> Optional[Plan]:
    result = user_plan_col.find_one({"user_id": user_id})
    if result is not None:
        user_plan = UserPlan(**result)
        result = plan_col.find_one({"name": user_plan.name})

        if result is not None:
            return Plan(**result)

    return None

def has_permissions(feature: str, user_id: str) -> bool:
    current_plan = get_current_plan(user_id)

    if feature in current_plan.features:
        return False
    return True