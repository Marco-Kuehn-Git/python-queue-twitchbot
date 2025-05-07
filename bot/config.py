import json
import os
import sys

from helper.helper import show_popup

class Config:
    DEFAULT_CONFIG = {
        "twitch_oauth_token": "",
        "twitch_refresh_token": "",
        "twitch_client_id": "",
        "twitch_client_secret": "",
        "twitch_app_redirect_uri": "http://localhost:8080",
        "twitch_scopes": ["chat:read", "chat:edit"],
        "twitch_channel": "",
        "sorting_option": 0
    }

    def __init__(self):
        # Load existing config
        config = self.load_config()

        # Merge user config with defaults
        merged_config = {**self.DEFAULT_CONFIG, **config}

        # Dynamically set attributes
        for key, value in merged_config.items():
            setattr(self, key, value)

    def load_config(self):
        """
        Loads the configuration data from config.json.
        Returns an empty dict if the file doesn't exist or is invalid.
        """
        try:
            with open(self._get_config_path(), "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_config(self):
        """
        Saves the current configuration to config.json.
        """
        config_data = {key: getattr(self, key) for key in self.DEFAULT_CONFIG}

        try:
            with open(self._get_config_path(), "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except (IOError, TypeError) as e:
            show_popup("error",
                       "Couldn't save config",
                       "There was an error trying to save the configuration:\n {e}")

    def _get_config_path(self):
        """
        Returns the absolute path to config.json based on execution context.
        """
        if getattr(sys, 'frozen', False):
            # Running as a bundled executable
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running as a normal Python script
            base_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_dir, "config.json")
