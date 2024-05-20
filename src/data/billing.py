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


def create_payment_account(user_id: str, 
                           subscription_id: str,
                           checkout_session_id: str,
                           amount: float,
                           product_id: str,
                           referral_id: Optional[str] = None):
    # If Stripe account does not exist then add it to the collection
    payment_account = payment_account_col.find_one({"user_id": user_id})

    if not payment_account:
        # Create a new payment account
        payment_account = {
            "user_id": user_id,
            "subscription_id": subscription_id,
            "checkout_session_id": checkout_session_id,
            "amount": amount,
            "product_id": product_id,
            "referral_id": referral_id
        }
        payment_account_col.insert_one(payment_account)
    else:
        # Update the existing payment account
        update_fields = {
            "subscription_id": subscription_id,
            "checkout_session_id": checkout_session_id,
            "amount": amount,
            "product_id": product_id
        }
        
        if referral_id is not None:
            update_fields["referral_id"] = referral_id
        
        payment_account_col.update_one(
            {"user_id": user_id},
            {"$set": update_fields}
        )


def remove_payment_account(checkout_session_id: str) -> None:
    # Find the payment account
    payment_account = payment_account_col.find_one({"checkout_session_id": checkout_session_id})

    if payment_account:
        payment_account_col.delete_one({"checkout_session_id": checkout_session_id})


def get_payment_account(user_id: str, 
                        checkout_session_id: str = None) -> Optional[PaymentAccount]:
    print("GETTING CUSTOMER ID FROM MONGODB")

    if checkout_session_id is not None:
        result = payment_account_col.find_one({"checkout_session_id": checkout_session_id})
    else:
        result = payment_account_col.find_one({"user_id": user_id})

    if result is not None:
        payment_account = PaymentAccount(**result)
        return payment_account

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