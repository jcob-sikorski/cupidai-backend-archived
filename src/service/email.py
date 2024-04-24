import requests


def send(email: str, transactional_id: str, **data_variables):
    print("SENDING EMAIL")
    response = requests.request(
        "POST", 
        "https://app.loops.so/api/v1/transactional", 
        json={
            "transactionalId": transactional_id,
            "email": email,
            "dataVariables": data_variables
        },
        headers={
            "Authorization": "Bearer 1dd67db210159eeff8910667b5db9b91",
            "Content-Type": "application/json"
        }
    )
    return response
