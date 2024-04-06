from fastapi import Request, HTTPException

import stripe

from model.billing import Item

import data.billing as data

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_..."

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_ed116b6b56e5b4cf34a61e6d5b8aa2708976207e53a2a6957dcf2b51eba4db85'

async def webhook(item: Item, request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers.get('STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    # TODO: for each event add or delete the StripeAccount model in stripe_acconut_col
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: update sth here in collection if needed
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # TODO: update sth here in collection if needed
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # TODO: update sth here in collection if needed
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return {"success": True}

def download_history(user_id: str) -> None:
    # TODO: implement fetching hisotry from stripe and getting this to user in the form of csv

    pass

def get_history(solo: bool, user_id: str) -> None:
    return data.get_history(solo, user_id)

def accept_tos(user_id: str) -> None:
    return data.accept_tos(user_id)

def get_current_plan(user_id: str) -> None:
    return data.get_current_plan(user_id)