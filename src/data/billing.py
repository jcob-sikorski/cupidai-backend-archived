import stripe

from typing import Optional

from datetime import datetime

from model.billing import PaymentAccount, TermsOfService, Plan
# from model.team import Team

# from .init import stripe_account_col, team_col, tos_col, plan_col
from .init import stripe_account_col, tos_col, plan_col


def has_permissions(feature: str, user_id: str) -> bool:
    print("CHECKING PERMISSIONS")
    current_plan = get_current_plan(user_id)

    return current_plan and feature in current_plan.features

def create_payment_account(user_id: str, customer_id: str, provider: str):
    # If Stripe account does not exist then add it to the collection
    stripe_account = stripe_account_col.find_one({"user_id": user_id})

    if not stripe_account:
        stripe_account = PaymentAccount(
            user_id=user_id,
            customer_id=customer_id
        )
        stripe_account_col.insert_one(stripe_account.dict())


def get_customer_id(user_id: str, provider: str) -> Optional[str]:
    print("GETTING CUSTOMER ID FROM MONGODB")

    result = payment_col.find_one({"user_id": user_id, "provider": provider})
    if result is not None:
        print("PARSING RESPONSE TO MODEL")
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

# TODO: create modals: for each plan create a document, with the provider and plan id 
#       as a dictionary mapping to plan id to the provider and feature list
# TODO: create endpoint: get current plan TBD