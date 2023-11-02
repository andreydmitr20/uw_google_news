import requests
from config import config

# Replace these with your actual values
webflow_api_token = config.webflow_api_token
site_id = "64fd3e5ccd4e50ccc351a436"

# Webflow API endpoint for members
endpoint = f"https://api.webflow.com/v2/sites/{site_id}/users"
# endpoint = f"https://api.webflow.com/sites/{site_id}/members"
# endpoint = f"https://api.webflow.com/sites"

# Set up the request headers with the API key
headers = {
    "Authorization": f"Bearer {webflow_api_token}",
}

# Make the GET request
response = requests.get(endpoint, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # print(f"{response}")

    # response = response.json()
    # Parse and print the user data
    data = response.json()
    print(f"{data}")
    users_partial_list = data["users"]
    for user in users_partial_list:
        print(
            f"User ID: {user['id']}, Name: {user['data']['name']}, Email: {user['data']['email']}"
        )
else:
    print(f"Error: {response.status_code}, {response.text}")
