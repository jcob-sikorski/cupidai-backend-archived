from fastapi import Request, HTTPException

import csv

import stripe

import data.billing as data

from model.account import Account
from model.billing import Item, StripeAccount

import service.referral as referral_service

from data.init import stripe_account_col, referral_col

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51P2KoI09MTVFbataUH3MvtXza4vM1XflPRcmj2tPfVcbPCTvkOaLqA2CuQQE2rREuBFppTnPsKWzAz8I9tO5Pi1g00Ea3qEZft"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_ZXfcjSIaktj06YiEuynVD9xl1LTbHygr'

# TESTING DONE ✅
def has_permissions(feature: str, user: Account) -> bool:
    return data.has_permissions(feature, user.user_id)

async def webhook(item: Item, request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(e)
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print(e)
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # If Stripe account does not exist then add it to the collection
        stripe_account = stripe_account_col.find_one({"user_id": session["client_reference_id"]})
        if not stripe_account:
            stripe_account = StripeAccount(
                customer_id =session["customer"],
                user_id=session["client_reference_id"]
            )
            stripe_account_col.insert_one(stripe_account.dict())

        # Get the user_id by getting StripeAccount and check if user got here thanks to referral
        referral = referral_col.find_one({"referral_id": session.metadata['referral_id']})
        if referral:
            referral_service.update_statistics(session.metadata['host_id'], session["amount_total"] / 100)

            # referral_service.remove_link(session["client_reference_id"])

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']

        # TODO: are we doing something here?

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']

        # Depending on the situation - if user bought, deleted, upgraded, or downgraded
        # Update the plan details for this customer
        # TODO: are we doing something here?

    else:
        print('Unhandled event type {}'.format(event['type']))

    return {"success": True}


def download_history(user: Account):
    # Fetch purchase history from Stripe
    invoices = get_history(solo=True, user_id=user.user_id)

    if invoices:
        # Prepare CSV data
        csv_data = []
        for invoice in invoices.auto_paging_iter():
            for line_item in invoice.lines.auto_paging_iter():
                csv_data.append([invoice.created, invoice.id, line_item.type, line_item.description])

        # Write CSV data to file
        file_name = f"{user.user_id}_purchase_history.csv"
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Invoice ID', 'Purchase Method', 'Plan Name'])
            writer.writerows(csv_data)

        print(f"Purchase history downloaded and saved to {file_name}")
    else:
        print("No purchase history found.")

# TESTING DONE ✅
def get_history(user: Account) -> None:
    return data.get_history(user.user_id)
# def get_history(solo: bool, user: Account) -> None:
#     return data.get_history(solo, user_id)

# TESTING DONE ✅
def accept_tos(user: Account) -> None:
    return data.accept_tos(user.user_id)

# TESTING DONE ✅
def get_current_plan(user: Account) -> None:
    return data.get_current_plan(user.user_id)