import requests

# TODO: we must also probably set the transactionalId 
#       so that we can send specific email
def send(email: str, transactional_id: str, **data_variables):
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
