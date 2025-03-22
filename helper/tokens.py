import requests
from bot.config import TWITCH_CLIENT_ID, load_config

# A simple check to see if token is valid or not
def can_connect_with_token(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": TWITCH_CLIENT_ID,
    }
    try:
        response = requests.get("https://api.twitch.tv/helix/users", headers=headers, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print("Error testing token connectivity:", e)
        return False