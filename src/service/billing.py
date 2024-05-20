from fastapi import Request, HTTPException

from typing import List, Tuple, Optional

import os

from datetime import datetime

import stripe

from stripe.error import InvalidRequestError

import data.billing as data

from model.account import Account
from model.billing import Item, Plan, CreateCheckoutSessionRequest

import service.account as account_service
import service.email as email_service
import service.referral as referral_service

from data.init import stripe_account_col, referral_col

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.getenv('STRIPE_API_KEY')

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')


# TODO: check if the user has current plan - if he has then check 
#       if the requested feature in is the plan features
def has_permissions(feature: str, 
                    user: Account) -> bool:
    # TODO: unccomment this for hollistic tests
    # return data.has_permissions(feature, user.user_id)
    return True

# TODO: need to create sth similar in radom and get the checkout url
def create_checkout_session(create_checkout_session_request: CreateCheckoutSessionRequest,
                            user: Account) -> str:
    session = stripe.checkout.Session.create(
        success_url="http://localhost:3000/dashboard",
        # success_url="https://deep-safe-spaniel.ngrok-free.app/dashboard",
        cancel_url="https://deep-safe-spaniel.ngrok-free.app/billing",
        line_items=[
            {
                "price": create_checkout_session_request.price_id, 
                "quantity": 1
            },
        ],
        mode="subscription",
        client_reference_id=user.user_id,
        metadata={
            "referral_id": create_checkout_session_request.referral_id
        }
    )

    return session.url

# TODO: do the similar steps but for radom API
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
        
        if session['mode'] == 'subscription':
            # Note: session['customer'] is null for not real customers

            create_stripe_account(session['client_reference_id'], session['customer'])

            referral = referral_service.get_referral(session['metadata']['referral_id'])

            if referral:
                referral_service.update_statistics(referral.host_id, session["amount_total"] / 100, False, False)

                user = account_service.get_by_id(referral.host_id)
                if user:
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

# TODO: instead create a payment account with the requested 
#       provider - each webhook for payment provider uses that
def create_stripe_account(user_id: str, 
                          customer_id: str):
    return data.create_stripe_account(user_id, customer_id)

# TODO: return a Plan document based on the customer's subscription_id/price_id whatever
def get_current_plan(user: Account) -> Optional[str]:
    customer_id = data.get_customer_id(user.user_id)

    if customer_id:
        try:
            customer = stripe.Customer.retrieve(customer_id, expand=['subscriptions'])
            print(customer)
            if 'subscriptions' in customer:
                subscriptions = customer.subscriptions.data  # Access the list of subscriptions
    
                for subscription in subscriptions:  # Iterate over each subscription
                    plan_id = subscription.plan.id  # Access the plan ID for each subscription
                    return plan_id
        except InvalidRequestError as e:
            # Handle the case where the customer does not exist or there was an error retrieving their data
            print(f"Error retrieving customer {customer_id}: {e}")
            return None
        
# TODO: get the customer id from database and create a 
#       request to radom to cancel the plan for this specific user
def cancel_plan(user: Account) -> bool:
    customer_id = data.get_customer_id(user.user_id)

    if customer_id:
        try:
            customer = stripe.Customer.retrieve(customer_id, expand=['subscriptions'])
            if 'subscriptions' in customer:
                subscriptions = customer.subscriptions.data  # Access the list of subscriptions
    
                for subscription in subscriptions:  # Iterate over each subscription
                    subscription_id = subscription.id  # Access the plan ID for each subscription
                    
                    stripe.Subscription.cancel(subscription_id)

                    return True
        except InvalidRequestError as e:
            # Handle the case where the customer does not exist or there was an error retrieving their data
            print(f"Error cancellling subscription: {e}")
            return False

    return False


# TODO: instead use the plan representation in the database
#       get available plans from there
def get_available_plans() -> Optional[List[Plan]]:
    try:
        products = stripe.Product.list(limit=4, active=True)

        product_list = []

        for product in products["data"]:
            default_price_id = product["default_price"]

            price = stripe.Price.retrieve(default_price_id)["unit_amount"]   

            product_info = {
                "price_id": default_price_id,
                "product_id": product["id"],
                "name": product["name"],
                "tag": product["metadata"].get("tag"),
                "description": product["description"],
                "features": [feature["name"] for feature in product["features"]],
                "price": f"£{price/100}",
            }
            product_list.append(product_info)

        return product_list
    except ValueError:
        raise HTTPException(status_code=404, detail="There are no available plans at the moment.")
    

# TODO: based on the Radom API return the product by it's id or sth similar
def get_product(product_id: str) -> Optional[Plan]:
    try:
        product = stripe.Product.retrieve(product_id)

        default_price_id = product["default_price"]

        price = stripe.Price.retrieve(default_price_id)["unit_amount"]

        product_info = {
            "price_id": default_price_id,
            "product_id": product["id"],
            "name": product["name"],
            "tag": product["metadata"].get("tag"),
            "description": product["description"],
            "features": [feature["name"] for feature in product["features"]],
            "price": f"${price / 100}$",
        }

        return product_info

    except stripe.error.StripeError as e:
        error_message = f"Error retrieving product information from Stripe: {e}"
        raise HTTPException(status_code=500, detail=error_message)

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        raise HTTPException(status_code=500, detail=error_message)