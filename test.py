import requests

# Assuming you've obtained the access token in previous steps
access_token = "YOUR_ACCESS_TOKEN"

# Make a request to the userinfo endpoint
response = requests.get(
    "https://YOUR_AUTH0_DOMAIN/userinfo",
    headers={"Authorization": f"Bearer {access_token}"}
)

# Parse the response
user_info = response.json()
print(user_info)

# Extract the user's ID
user_id = user_info.get("sub")  # Often the user's ID is in the sub claim
print(f"User ID: {user_id}")