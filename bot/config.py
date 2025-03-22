import json
import os
import sys

def get_config_path():
    # If running as and exe file
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    # If running as script fro debugging    
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(BASE_DIR, "config.json")

def load_config():
    print("Reading config from: ", CONFIG_PATH)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

CONFIG_PATH = get_config_path()
CONFIG = load_config()

TWITCH_OAUTH_TOKEN = CONFIG["twitch_oauth_token"]
TWITCH_REFRESH_TOKEN = CONFIG["twitch_refresh_token"]
TWITCH_CLIENT_ID = CONFIG["twitch_client_id"]
TWITCH_CLIENT_SECRET = CONFIG["twitch_client_secret"]
TWITCH_APP_REDIRECT_URI = CONFIG["twitch_app_redirect_uri"]
TWITCH_SCOPES = CONFIG["twitch_scopes"]
TWITCH_CHANNEL = CONFIG["twitch_channel"]
