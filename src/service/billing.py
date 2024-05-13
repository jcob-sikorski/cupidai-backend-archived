from fastapi import Request, HTTPException

from typing import List, Optional

import os

from datetime import datetime

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
stripe.api_key = os.getenv('STRIPE_API_KEY')

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')


def has_permissions(feature: str, 
                    user: Account) -> bool:
    # TODO: unccomment this for hollistic tests
    # return data.has_permissions(feature, user.user_id)
    return True

async def create_checkout_session(referral_id: str, 
                                  user: Account) -> None:
    
    session = await stripe.checkout.Session.create(
        success_url="https://deep-safe-spaniel.ngrok-free.app/dashboard",
        cancel_url="https://deep-safe-spaniel.ngrok-free.app/billing",
        line_items=[
            {
                "price": "price_1P2ZR509MTVFbatacp2Bps8R", 
                "quantity": 1
            },
            {
                "price": "price_1P2ZTc09MTVFbata42n2Hqup", 
                "quantity": 1
            },
            {
                "price": "price_1P2ZUI09MTVFbatarjRaJvMH", 
                "quantity": 1
            },
            {
                "price": "price_1P2ZV609MTVFbataKtHmKS3z", 
                "quantity": 1
            },
        ],
        mode="subscription",
        client_reference_id=user.user_id,
        referral_id=referral_id,
        metadata={
            "referral_id": referral_id
        }
    )

    return session.url

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
    
    print("EVENT: ", event)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # TODO: By default checkout.session.completed will only have a 
        #       customer ID if the session was related to buying a subscription.
        # if session['mode'] == 'payment':
            # Note: session['customer'] is null for not real customers

            # create_stripe_account(session['client_reference_id'], session['customer'])

            # referral = referral_service.get_referral(session['metadata']['referral_id'])

            # if referral:
            #     referral_service.update_statistics(referral.host_id, session["amount_total"] / 100, False)

            #     user = account_service.get_by_id(referral.host_id)
            #     if user:
            #         # for env   
            #         email_service.send(user.email, 'clv2tl6jd00vybfeainihiu2j')

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


def get_payment_intents(starting_after: int, 
                        limit: int, 
                        user: Account) -> List[dict]:
    try:
        customer_id = data.get_customer_id(user.user_id)

        transaction_history = []

        if customer_id:
            payment_intents = stripe.PaymentIntent.list(customer=customer_id,
                                                        starting_after=starting_after, 
                                                        limit=limit)

            for intent in payment_intents.data:
                date = datetime.fromtimestamp(intent.created).strftime("%Y-%m-%d %H:%M:%S")
                plan = intent.description  # Assuming description contains the plan information
                status = intent.status

                # Creating transaction dictionary
                transaction = {
                    "date": date,
                    "plan": plan,
                    "status": status
                }
                transaction_history.append(transaction)

        return transaction_history

    except stripe.error.InvalidRequestError as e:
        raise HTTPException(status_code=404, detail="There is no track record of payment intents for this user.")


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
    

def get_available_plans() -> Optional[List[Plan]]:
    try:
        products = stripe.Product.list(limit=4, active=True)

        product_list = []

        for product in products["data"]:
            default_price_id = product["default_price"]

            price = stripe.Price.retrieve(default_price_id)["unit_amount"]   

            product_info = {
                "product_id": product["id"],
                "name": product["name"],
                "tag": product["metadata"].get("tag"),
                "description": product["description"],
                "features": [feature["name"] for feature in product["features"]],
                "default_price": f"{price/100}$",
            }
            product_list.append(product_info)

        return product_list
    except ValueError:
        raise HTTPException(status_code=404, detail="There are no available plans at the moment.")
    

def get_product(product_id: str) -> Optional[Plan]:
    try:
        product = stripe.Product.retrieve(product_id)

        default_price_id = product["default_price"]

        price = stripe.Price.retrieve(default_price_id)["unit_amount"]

        product_info = {
            "product_id": product["id"],
            "name": product["name"],
            "tag": product["metadata"].get("tag"),
            "description": product["description"],
            "features": [feature["name"] for feature in product["features"]],
            "default_price": f"${price / 100}$",
        }

        return product_info

    except stripe.error.StripeError as e:
        error_message = f"Error retrieving product information from Stripe: {e}"
        raise HTTPException(status_code=500, detail=error_message)

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        raise HTTPException(status_code=500, detail=error_message)