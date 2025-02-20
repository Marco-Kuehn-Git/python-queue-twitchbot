import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
CONFIG = load_config()

TWITCH_OAUTH_TOKEN = CONFIG["twitch_oauth_token"]
TWITCH_REFRESH_TOKEN = CONFIG["twitch_refresh_token"]
TWITCH_CLIENT_ID = CONFIG["twitch_client_id"]
TWITCH_CLIENT_SECRET = CONFIG["twitch_client_secret"]
TWITCH_CHANNEL = CONFIG["twitch_channel"]