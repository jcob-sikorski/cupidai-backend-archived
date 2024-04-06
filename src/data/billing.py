import stripe

from typing import Optional

from datetime import datetime

from model.billing import Plan, StripeAccount, TermsOfService
from model.team import Team

from .init import plan_col, stripe_account_col, team_col, tos_col

def has_permissions(feature: str, user_id: str) -> bool:
    current_plan = get_current_plan(user_id)

    if feature in current_plan.features:
        return False
    return True

def get_customer_id(user_id: str) -> Optional[str]:
    result = stripe_account_col.find_one({"user_id": user_id})
    if result is not None:
        stripe_account = StripeAccount(**result)
        return stripe_account.customer_id
    return None

def get_team_owner_id(member_id: str) -> Optional[str]:
    result = team_col.find_one({"members": member_id})
    if result is not None:
        team = Team(**result)
        return team.owner
    return None

def get_history(solo: bool, user_id: str) -> None:
    if solo:
        customer_id = get_customer_id(user_id)
    else:
        owner_id = get_team_owner_id(user_id)
        customer_id = get_customer_id(owner_id)

    if customer_id is not None:
        invoices = stripe.Invoice.list(customer=customer_id)
        return invoices
    else:
        print("User ID not found in StripeAccount collection.")
        return None

def accept_tos(user_id: str) -> None:
    # Get the current date and time
    now = datetime.now()

    # Format the date and time in the format you prefer
    date_accepted = now.strftime("%Y-%m-%d %H:%M:%S")

    # Create a new TermsOfService object
    tos = TermsOfService(user_id=user_id, date_accepted=date_accepted)

    # Insert the new TermsOfService object into the tos_col collection
    tos_col.insert_one(tos.dict())

def get_current_plan(user_id: str) -> Optional[Plan]:
    # Get the customer ID associated with the user ID
    customer_id = get_customer_id(user_id)

    if customer_id is not None:
        # Retrieve the customer's subscriptions from Stripe
        subscriptions = stripe.Subscription.list(customer=customer_id)

        # If the customer has at least one subscription
        if len(subscriptions.data) > 0:
            # Get the plan ID of the first subscription
            plan_id = subscriptions.data[0].plan.id

            # Find the plan in the plan_col collection
            result = plan_col.find_one({"id": plan_id})

            if result is not None:
                # Return the plan
                return Plan(**result)

    return None
