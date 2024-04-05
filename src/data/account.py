import requests
import json

# TODO: use the auth0 endpoints to manage user

def change_email(email: str, user_id: str) -> None:
    url = f"https://login.auth0.com/api/v2/users/{user_id}"

    payload = json.dumps({
      "email": email,
      "connection": "passwordless"
    })

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

def get(user_id: str) -> None:
    url = f"https://login.auth0.com/api/v2/users/{user_id}"

    payload = {}

    headers = {
      'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

def change_profile_picture(profile_uri: str, user_id: str) -> None:
    url = f"https://login.auth0.com/api/v2/users/{user_id}"

    payload = json.dumps({
      "picture": profile_uri
    })

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

def delete(user_id: str) -> None:
    url = f"https://login.auth0.com/api/v2/users/{user_id}"

    payload = {}

    headers = {}

    response = requests.request("DELETE", url, headers=headers, data=payload)