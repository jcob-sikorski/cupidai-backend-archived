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


def has_permissions(feature: str, 
                    user: Account) -> bool:
    # TODO: unccomment this for hollistic tests
    # return data.has_permissions(feature, user.user_id)
    return True

def create_checkout_session(create_checkout_session_request: CreateCheckoutSessionRequest,
                            user: Account) -> str:
    session = stripe.checkout.Session.create(
        success_url="https://deep-safe-spaniel.ngrok-free.app/dashboard",
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
                referral_service.update_statistics(referral.host_id, session["amount_total"] / 100, False)

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


# def get_transaction_history(last_object_id: str, 
#                             limit: str, 
#                             user: Account) -> Tuple[List[dict], Optional[str], bool]:
#     try:
#         customer_id = data.get_customer_id(user.user_id)

#         transaction_history = []
#         has_more = False

#         if customer_id:
#             payment_intents = stripe.PaymentIntent.list(customer=customer_id,
#                                                         starting_after=last_object_id if last_object_id else None,
#                                                         limit=int(limit))
            
#             print("PAYMENT INTENTS: ", payment_intents)

#             for intent in payment_intents.data:
#                 date = datetime.fromtimestamp(intent.created).strftime("%Y-%m-%d %H:%M:%S")

#                 # Creating transaction dictionary
#                 transaction = {
#                     "date": date,
#                     "id": intent.id,
#                     "description": intent.description,
#                     "status": intent.status
#                 }
#                 transaction_history.append(transaction)

#             # Extract the ID of the last object for pagination
#             if payment_intents.data:
#                 last_object_id = payment_intents.data[-1].id
#                 has_more = payment_intents.has_more

#         return transaction_history, last_object_id, has_more

#     except stripe.error.InvalidRequestError as e:
#         raise HTTPException(status_code=404, detail="There is no track record of payment intents for this user.")


def accept_tos(user: Account) -> None:
    try:
        data.accept_tos(user.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Failed to accept Terms of Conditions.")


def get_current_plan(user: Account) -> Optional[str]:
    customer_id = data.get_customer_id(user.user_id)

    if customer_id:
        try:
            customer = stripe.Customer.retrieve(customer_id, expand=['subscriptions'])
            if 'subscriptions' in customer:
                subscriptions = customer.subscriptions.data  # Access the list of subscriptions
    
                for subscription in subscriptions:  # Iterate over each subscription
                    plan_id = subscription.plan.id  # Access the plan ID for each subscription
                    return plan_id
        except InvalidRequestError as e:
            # Handle the case where the customer does not exist or there was an error retrieving their data
            print(f"Error retrieving customer {customer_id}: {e}")
            return None
        

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
                "price": f"{price/100}$",
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