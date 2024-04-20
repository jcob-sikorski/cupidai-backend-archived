import stripe

from typing import Optional

from datetime import datetime

from model.billing import StripeAccount, TermsOfService, Plan
# from model.team import Team

# from .init import stripe_account_col, team_col, tos_col, plan_col
from .init import stripe_account_col, tos_col, plan_col

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

# TESTING DONE ✅
def get_history(user_id: str) -> dict:
    # Fetch customer ID
    customer_id = get_customer_id(user_id)

    if customer_id is not None:
        # Fetch invoices from Stripe
        invoices = stripe.Invoice.list(customer=customer_id)
        
        # Prepare dictionary data
        dict_data = []
        for invoice in invoices.auto_paging_iter():
            for line_item in invoice.lines.auto_paging_iter():
                dict_data.append({
                    'Date': invoice.created,
                    'Invoice ID': invoice.id,
                    'Purchase Method': line_item.type,
                    'Plan Name': line_item.description
                })

        return dict_data
    else:
        raise ValueError("There is no track record of transactions for this user.")


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

    raise ValueError("There is no track record of transactions for this user.")