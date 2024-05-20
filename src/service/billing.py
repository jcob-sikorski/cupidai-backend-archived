from fastapi import Request, HTTPException

from typing import Optional, Dict, Any

import os

from datetime import datetime

import requests

import json

from stripe.error import InvalidRequestError

import data.billing as data

from model.account import Account
from model.billing import Plan, CheckoutSessionRequest

import service.account as account_service
import service.email as email_service
import service.referral as referral_service

# from data.init import stripe_account_col, referral_col

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
# stripe.api_key = os.getenv('STRIPE_API_KEY')

# This is your Stripe CLI webhook secret for testing your endpoint locally.


# TODO: check if the user has current plan - if he has then check 
#       if the requested feature in is the plan features
def has_permissions(feature: str, 
                    user: Account) -> bool:
    pass


# TODO: need to create sth similar in radom and get the checkout url
def create_checkout_session(
    req: CheckoutSessionRequest,
    user: Account
) -> Dict[str, Any]:
    
    # TODO: check if the customer has referenced subscription id.
    #       if cusomter has subscription id then return error - he needs 
    #       to cancel the plan in order to make a new subscription
    
    product = get_product(req.radom_product_id)

    line_items = [
        {
            "productId": req.radom_product_id,
            "itemData": {
                "name": product.name,
                "description": product.description,
                "chargingIntervalSeconds": 3600 * 24 * 30,
                "price": product.price,
                "isMetered": False,
                "currency": "GBP",
                "sendSubscriptionEmails": True
            }
        }
    ]
    
    gateway = {
        "managed": {
            "methods": [
                {
                    "network": "SepoliaTestnet",
                    "token": "0xa4fCE8264370437e718aE207805b4e6233638b9E",
                    "discountPercentOff": 0
                }
            ]
        }
    }
    
    metadata = [
        {
            "key": "user_id",
            "value": user.user_id
        },
        {
            "key": "referral_id",
            "value": req.referral_id
        }
    ]
    
    customizations = {
        "leftPanelColor": "#FFFFFF",
        "primaryButtonColor": "#000000",
        "slantedEdge": True,
        "allowDiscountCodes": False
    }

    url = "https://api.radom.com/checkout_session"

    payload = {
        "lineItems": line_items,
        # "total": total,
        "currency": "ETH",
        "gateway": gateway,
        "successUrl": "http://localhost:3000/dashboard",
        "cancelUrl": "http://localhost:3000/dashboard",
        "metadata": metadata,
        "expiresAt": 1747827000,
        "customizations": customizations,
        "chargeCustomerNetworkFee": True
    }

    headers = {
        'Authorization': "eyJhZGRyZXNzIjpudWxsLCJvcmdhbml6YXRpb25faWQiOiI1Njc3ZTU0OC0zMWEwLTRmZWMtODA5OS1kM2QyODkzYjYwZmQiLCJzZXNzaW9uX2lkIjoiYWY4ZjA2YTktNzliOS00NGM3LTk0ODgtZDk2MGUyMDRlZTAzIiwiZXhwaXJlZF9hdCI6IjIwMjUtMDUtMjBUMTQ6MzM6NDQuMjczNDU0NTExWiIsImlzX2FwaV90b2tlbiI6dHJ1ZX0=",
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for any HTTP error
        response_data = response.json()
        print("CHECKOUT SESSION RESPONSE")
        print(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print("Error creating checkout session:", e)
        return {}  # Return an empty dictionary in case of error


async def webhook(request: Request) -> None:
    print("WEBHOOK REQUEST")
    body = await request.body()
    body_str = body.decode()
    print(body_str)


    # Parse JSON string into a Python dictionary
    body_dict = json.loads(body_str)

    # Extract the event type
    event_type = body_dict.get("eventType")

    if event_type == "newSubscription":
        subscription_id = body_dict.get("eventData", {}).get("newSubscription", {}).get("subscriptionId")

        checkout_session_id = body_dict.get("radomData", {}).get("checkoutSession", {}).get("checkoutSessionId")

        amount = body_dict.get("eventData", {}).get("newSubscription", {}).get("amount", {})

        product_id = body_dict.get("eventData", {}).get("newSubscription", {}).get("tags", {}).get("productId")

        metadata = body_dict.get("radomData", {}).get("checkoutSession", {}).get("metadata", [])

        user_id = None
        referral_id = None
        for item in metadata:
            if item.get("key") == "user_id":
                user_id = item.get("value")
            elif item.get("key") == "referral_id":
                referral_id = item.get("value")

        create_payment_account(user_id=user_id, 
                               subscription_id=subscription_id, 
                               checkout_session_id=checkout_session_id, 
                               amount=amount,
                               product_id=product_id,
                               referral_id=referral_id)

    elif event_type == "paymentTransactionConfirmed":
        # Handle payment transaction confirmed event
        # TODO: using checkout session id mark the referral as eligible for payment just like in the webhook in the past

        checkout_session_id = body_dict.get("radomData", {}).get("checkoutSession", {}).get("checkoutSessionId")

        payment_account = get_payment_account(user_id='',
                                              checkout_session_id=checkout_session_id)
        if payment_account.referral_id:
            referral = referral_service.get_referral(payment_account.referral_id)

            if referral:
                # TODO: get the price from the payment_account
                referral_service.update_statistics(referral.host_id, session["amount_total"], False, False)

                user = account_service.get_by_id(referral.host_id)
                if user:
                    email_service.send(user.email, 'clv2tl6jd00vybfeainihiu2j')

    elif event_type == "subscriptionExpired":
        # TODO: get the subscription_id
        # TODO: based on the subscription id find the payment account 
        #       and remove the subscription id from the payment account

        subscription_id = body_dict.get("eventData", {}).get("newSubscription", {}).get("subscriptionId")
        
        pass
    elif event_type == "subscriptionCancelled":
        # TODO: get the subscription_id
        # TODO: based on the subscription id find the payment account 
        #       and remove the subscription id from the payment account
        pass

    return


# TODO: get the customer id from database and create a 
#       request to radom to cancel the plan for this specific user
def cancel_plan(user: Account) -> bool:
    # TODO: instead get subscription id
    # TODO: subscription
    customer_id = data.get_customer_id(user.user_id)

    if customer_id:
        pass


def get_available_plans(user: Account) -> Optional[Dict[str, Any]]:
    # Retrieve available plans
    plans = data.get_available_plans()
    
    # Get the current plan for the user
    current_plan = get_current_plan(user)
    
    # Extract the current plan ID
    current_plan_id = current_plan.id if current_plan else None
    
    # Format available plans as a list of Plan instances
    formatted_plans = [Plan(**plan_dict) for plan_dict in plans]
    
    # Return the result as a dictionary
    return {
        "plans": formatted_plans,
        "current_plan_id": current_plan_id
    }
    

def get_product(radom_product_id: str) -> Optional[Plan]:
    return data.get_product(radom_product_id)


def create_payment_account(user_id: str, 
                           subscription_id: str,
                           checkout_session_id: str,
                           amount: float,
                           product_id: str,
                           referral_id: Optional[str] = None):
    
    return data.create_payment_account(user_id, 
                                       subscription_id,
                                       checkout_session_id,
                                       amount,
                                       product_id,
                                       referral_id)


# TODO: return a Plan document based on the customer's subscription_id/price_id whatever
def get_current_plan(user: Account) -> Optional[str]:
    customer_id = data.get_customer_id(user.user_id)

    if customer_id:
        pass
