import stripe

from typing import Optional

from datetime import datetime

from model.billing import StripeAccount, TermsOfService, Plan
from model.team import Team

from .init import stripe_account_col, team_col, tos_col, plan_col

# TESTING DONE ✅
def has_permissions(feature: str, user_id: str) -> bool:
    print("CHECKING PERMISSIONS")
    current_plan = get_current_plan(user_id)

    return current_plan and feature in current_plan.features

# TESTING DONE ✅
def get_customer_id(user_id: str) -> Optional[str]:
    print("GETTING CUSTOMER ID FROM MONGODB")

    result = stripe_account_col.find_one({"user_id": user_id})
    if result is not None:
        print("PARSING RESPONSE TO MODEL")
        stripe_account = StripeAccount(**result)
        return stripe_account.customer_id
    return None

# TODO: why this is here - we already have similar function in a team
def get_team_owner_id(member_id: str) -> Optional[str]:
    result = team_col.find_one({"members": member_id})
    if result is not None:
        team = Team(**result)
        return team.owner
    return None


# TESTING DONE ✅
def get_history(solo: bool, user_id: str) -> None:
    if solo:
        customer_id = get_customer_id(user_id)
    else:
        # TODO: test when solo is false
        owner_id = get_team_owner_id(user_id)
        customer_id = get_customer_id(owner_id)

    if customer_id is not None:
        invoices = stripe.Invoice.list(customer=customer_id)
        return invoices
    else:
        print("User ID not found in StripeAccount collection.")
        return None

# TESTING DONE ✅
def accept_tos(user_id: str) -> None:
    # Get the current date and time
    now = datetime.now()

    # Format the date and time in the format you prefer
    date_accepted = now.strftime("%Y-%m-%d %H:%M:%S")

    # Create a new TermsOfService object
    tos = TermsOfService(user_id=user_id, date_accepted=date_accepted)

    # Insert the new TermsOfService object into the tos_col collection
    tos_col.insert_one(tos.dict())

    result = tos_col.insert_one(tos.dict())

    return result.inserted_id is not None

# TESTING DONE ✅
def get_current_plan(user_id: str) -> Optional[Plan]:
    customer_id = get_customer_id(user_id)

    if customer_id is not None:
        print("RETRIEVING CUSTOMER'S SUBSCRIPTIONS FROM STRIPE")
        # TODO: test when the customer_id is in the subcription list
        # Retrieve the customer's subscriptions from Stripe
        subscriptions = stripe.Subscription.list(customer=customer_id)

        # If the customer has at least one subscription
        if len(subscriptions.data) > 0:
            print("GOT THE PLAN NAME OF THE FIRST SUBSCRIPTION IN THE LIST")

            # Initialize variables to track the most recent subscription
            most_recent_subscription_plan_id = None
            most_recent_billing_cycle_anchor = 0

            print("ITERATING THORUGH SUBSCRIPTIONS")
            for subscription in subscriptions:
                billing_cycle_anchor = subscription["billing_cycle_anchor"]
                if billing_cycle_anchor > most_recent_billing_cycle_anchor:
                    most_recent_billing_cycle_anchor = billing_cycle_anchor
                    most_recent_subscription_plan_id = subscription["plan"]["id"]

            # Search for the plan with the given plan_id
            plan_doc = plan_col.find_one({"plan_id": most_recent_subscription_plan_id})
            if plan_doc:
                print("GOT THE PLAN DOC")
                # If found, return the plan as a Plan object
                return Plan(**plan_doc)
            else:
                # If not found, return None
                return None

    return None

