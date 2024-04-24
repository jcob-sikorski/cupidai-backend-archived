from fastapi import Request, HTTPException

from typing import Optional

from vars import STRIPE_API_KEY, STRIPE_ENDPOINT_SECRET

import csv

import stripe

import data.billing as data

from model.account import Account
from model.billing import Item, StripeAccount, Plan

import service.account as account_service
import service.email as email_service
import service.referral as referral_service

from data.init import stripe_account_col, referral_col

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = STRIPE_API_KEY

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = STRIPE_ENDPOINT_SECRET


def has_permissions(feature: str, 
                    user: Account) -> bool:
    # TODO: unccomment this for hollistic tests
    # return data.has_permissions(feature, user.user_id)
    return True

async def webhook(item: Item, 
                  request: Request) -> None:
    event = None
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session['mode'] == 'payment':
            # TODO: By default checkout.session.completed will only have a 
            #       customer ID if the session was related to buying a subscription.
            # Note: session['customer'] is null for not real customers
            create_stripe_account(session['client_reference_id'], session['customer'])

            referral = referral_service.get_referral(session['metadata']['referral_id'])

            if referral:
                referral_service.update_statistics(referral.host_id, session["amount_total"] / 100, False)

                user = account_service.get_by_id(referral.host_id)
                if user:
                    # for env   
                    email_service.send(user.email, 'clv2tl6jd00vybfeainihiu2j')

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

def create_stripe_account(user_id: str, 
                          customer_id: str):
    return data.create_stripe_account(user_id, customer_id)

# TODO: this does not in any way allows user to donwload a csv in chunks
def download_history(user: Account) -> None:
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
        raise HTTPException(status_code=404, detail="No purchase history found.")


def get_history(user: Account) -> dict:
    try:
        return data.get_history(user.user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="There is no track record of transactions for this user.")


def accept_tos(user: Account) -> None:
    try:
        data.accept_tos(user.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Failed to accept Terms of Conditions.")


def get_current_plan(user: Account) -> Optional[Plan]:
    try:
        return data.get_current_plan(user.user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="There is no track record of transactions for this user.")