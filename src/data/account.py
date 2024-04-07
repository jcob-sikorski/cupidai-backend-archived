import requests
import json

def change_email(email: str, user_id: str) -> None:
    # TODO:
    return 200
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = json.dumps({
    #   "email": email,
    #   "connection": "passwordless"
    # })

    # headers = {
    #   'Content-Type': 'application/json',
    #   'Accept': 'application/json'
    # }

    # response = requests.request("PATCH", url, headers=headers, data=payload)

def get(user_id: str) -> None:
    # TODO:
    return 200

    # TODO: is this really a user_id?
    # TODO: how to get access token which has the user_id?
    # TODO: is this user authenticated?
    # TODO: how to authenticate a user?
    # TODO: what is the setuo to use my fastapi endpoint as a usser and
    #       manage this user?

    # TODO: how to interact with this api? what is the user_id? what is the bearer token?
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = {}

    # headers = {
    #   'Accept': 'application/json',
    #   'Authorization': f'Bearer '
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

def change_profile_picture(profile_uri: str, user_id: str) -> None:
    # TODO:
    return 200
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = json.dumps({
    #   "picture": profile_uri
    # })

    # headers = {
    #   'Content-Type': 'application/json',
    #   'Accept': 'application/json'
    # }

    # response = requests.request("PATCH", url, headers=headers, data=payload)

def delete(user_id: str) -> None:
    # TODO:
    return 200
    # url = f"https://login.auth0.com/api/v2/users/{user_id}"

    # payload = {}

    # headers = {}

    # response = requests.request("DELETE", url, headers=headers, data=payload)