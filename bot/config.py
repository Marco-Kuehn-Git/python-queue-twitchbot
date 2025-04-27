import json
import os
import sys

class Config():
    def __init__(self):
        config = self.load_config()
        self.twitch_oauth_token = config["twitch_oauth_token"]
        self.twitch_refresh_token = config["twitch_refresh_token"]
        self.twitch_client_id = config["twitch_client_id"]
        self.twitch_client_secret = config["twitch_client_secret"]
        self.twitch_app_redirect_uri = config["twitch_app_redirect_uri"]
        self.twitch_scopes = config["twitch_scopes"]
        self.twitch_channel = config["twitch_channel"]
        self.sorting_option = config["sorting_option"]

    def load_config(self):
        """
        Loads the data from the config.json
        """
        with open(self.__get_config_path(), "r") as f:
            return json.load(f)

    def save_config(self):
        """
        Saves the current config object as a json file.
        """
        config_data = {
            "twitch_oauth_token": self.twitch_oauth_token,
            "twitch_refresh_token": self.twitch_refresh_token,
            "twitch_client_id": self.twitch_client_id,
            "twitch_client_secret": self.twitch_client_secret,
            "twitch_app_redirect_uri": self.twitch_app_redirect_uri,
            "twitch_scopes": self.twitch_scopes,
            "twitch_channel": self.twitch_channel,
            "sorting_option": self.sorting_option
        }

        with open(self.__get_config_path(), "w") as f:
            json.dump(config_data, f, indent=4)

    def __get_config_path(self):
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
