from fastapi import Request, HTTPException

import stripe

import data.billing as data

from model.billing import Item, StripeAccount

import service.referral as referral_service

from .init import stripe_account_col

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51P2KoI09MTVFbataUH3MvtXza4vM1XflPRcmj2tPfVcbPCTvkOaLqA2CuQQE2rREuBFppTnPsKWzAz8I9tO5Pi1g00Ea3qEZft"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_ed116b6b56e5b4cf34a61e6d5b8aa2708976207e53a2a6957dcf2b51eba4db85'

# TESTING DONE ✅
def has_permissions(feature: str, user_id: str) -> bool:
    return data.has_permissions(feature, user_id)

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

    # TODO: figure out how the event structure looks like

    # Handle the event
    # TODO: for each event add or delete the StripeAccount model in stripe_acconut_col
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: if stripe account does not exist then add it to the collection
        # TODO: update the Plan the user bought
        # TODO: get the user+id by getting StripeAccount and check if user got here thanks to referral
        # TODO: update the statistics for the user who made the referral link

        # then remove this specific referral so user 
        #       of the specific link - if yes then update statistics for the user who generated the link
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # TODO: remove this plan from bought plans of this customer
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']

        # TODO: depending on the situation - if user bought, delted, upgraded, or downgraded
        # TODO: what to do?       
    else:
        print('Unhandled event type {}'.format(event['type']))

    return {"success": True}

async def webhook_proposal(item: Item, request: Request):
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
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # TODO: for all the operations below we must get 
        #       association between the user_id and customer_id

        # If Stripe account does not exist then add it to the collection
        stripe_account = stripe_account_col.find_one({"customer_id": session["customer"]})
        if not stripe_account:
            stripe_account = StripeAccount(
                customer_id =session["customer"],
                user_id=user_id
            )
            stripe_account_col.insert_one(stripe_account.dict())

        # Get the user_id by getting StripeAccount and check if user got here thanks to referral
        referral = referral_col.find_one({"referral_id": session["client_reference_id"]})
        if referral:
            referral_service.update_statistics(user_id, session["amount_total"] / 100)

            # Then remove this specific referral so user can't use it again
            referral_col.delete_one({"referral_id": session["client_reference_id"]})

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']

        # Remove this plan from bought plans of this customer
        plan_col.delete_one({"user_id": subscription["customer"], "plan_id": subscription["items"]["data"][0]["plan"]["id"]})

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']

        # Depending on the situation - if user bought, deleted, upgraded, or downgraded
        # Update the plan details for this customer
        plan_col.update_one({"user_id": subscription["customer"]}, {"$set": {"plan_id": subscription["items"]["data"][0]["plan"]["id"]}})

    else:
        print('Unhandled event type {}'.format(event['type']))

    return {"success": True}


def download_history(user_id: str) -> None:
    # TODO: implement fetching hisotry from stripe and getting this to user in the form of csv

    pass

# TESTING DONE ✅
def get_history(solo: bool, user_id: str) -> None:
    return data.get_history(solo, user_id)

# TESTING DONE ✅
def accept_tos(user_id: str) -> None:
    return data.accept_tos(user_id)

# TESTING DONE ✅
def get_current_plan(user_id: str) -> None:
    return data.get_current_plan(user_id)