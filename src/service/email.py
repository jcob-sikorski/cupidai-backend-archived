import requests

def send_request(email: str, **data_variables):
    response = requests.request(
        "POST", 
        "https://app.loops.so/api/v1/transactional", 
        json={
            "transactionalId": "cltertje200k7zf04tzzdhmgx",
            "email": email,
            "dataVariables": data_variables
        },
        headers={
            "Authorization": "Bearer 1dd67db210159eeff8910667b5db9b91",
            "Content-Type": "application/json"
        }
    )
    return response
