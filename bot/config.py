import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
CONFIG = load_config()

TWITCH_OAUTH_TOKEN = CONFIG["twitch_oauth_token"]
TWITCH_CHANNEL = CONFIG["twitch_channel"]