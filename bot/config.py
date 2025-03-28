import json
import os
import sys

def get_config_path():
    """
    Returns the absolute path to the config.json file.
    """
    if getattr(sys, 'frozen', False):
        # Running as executable
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        # Running as python script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(BASE_DIR, "config.json")

def load_config():
    """
    Load and return the configuration from config.json.
    """
    print("Reading config from:", CONFIG_PATH)
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
