import stripe

from typing import Optional, List

from datetime import datetime

from model.billing import PaymentAccount, TermsOfService, Plan
# from model.team import Team

# from .init import payment_account_col, team_col, tos_col, plan_col
from .init import payment_account_col, tos_col, plan_col


def has_permissions(feature: str, user_id: str) -> bool:
    print("CHECKING PERMISSIONS")
    current_plan = get_current_plan(user_id)

    return current_plan and feature in current_plan.features


def create_payment_account(user_id: str, customer_id: str):
    # If Stripe account does not exist then add it to the collection
    payment_account = payment_account_col.find_one({"user_id": user_id})

    if not payment_account:
        payment_account = PaymentAccount(
            user_id=user_id,
            customer_id=customer_id
        )
        payment_account_col.insert_one(payment_account.dict())


def get_customer_id(user_id: str) -> Optional[str]:
    print("GETTING CUSTOMER ID FROM MONGODB")

    result = payment_account_col.find_one({"user_id": user_id})

    if result is not None:
        payment_account = PaymentAccount(**result)

        return payment_account.customer_id
    
    return None


def accept_tos(user_id: str) -> None:
    # Get the current date and time
    now = datetime.now()


    # Create a new TermsOfService object
    tos = TermsOfService(user_id=user_id, 
                         date_accepted=now)

    result = tos_col.insert_one(tos.dict())

    if not result.inserted_id:
        raise ValueError("Failed to accept Terms of Conditions.")
    

def get_available_plans() -> Optional[List[Plan]]:
    result = plan_col.find()
    return result


def get_product(radom_product_id: str) -> Optional[Plan]:
    # Query the MongoDB collection to find one document by radom_product_id
    result = plan_col.find_one({"radom_product_id": radom_product_id})
    
    # If a result is found, convert it to a Plan instance
    if result:
        return Plan(**result)
    
    # If no result is found, return None
    return None

# TODO: create endpoint: get current plan TBD