import json
import requests
import webbrowser
import http.server
import socketserver
import threading
from urllib.parse import urlparse, parse_qs

from helper.helper import show_popup
from bot.config import (
    TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, TWITCH_OAUTH_TOKEN,
    TWITCH_REFRESH_TOKEN, TWITCH_APP_REDIRECT_URI, TWITCH_SCOPES,
    get_config_path
)

CONFIG_PATH = get_config_path()

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class TwitchAuthHandler:
    def __init__(self):
        self.auth_code = None
        self.oauth_token = None if not TWITCH_OAUTH_TOKEN else TWITCH_OAUTH_TOKEN
        self.refresh_token = None if not TWITCH_REFRESH_TOKEN else TWITCH_REFRESH_TOKEN
        self.server = None
        self.auth_event = threading.Event()

    # Start the authorization process
    def start_auth(self):
        print("Starting Twitch authorization...")
        auth_url = (
            f"https://id.twitch.tv/oauth2/authorize?"
            f"client_id={TWITCH_CLIENT_ID}&"
            f"response_type=code&"
            f"redirect_uri={TWITCH_APP_REDIRECT_URI}&"
            f"scope={' '.join(TWITCH_SCOPES)}"
        )
        webbrowser.open(auth_url)
        self.start_local_server()
        
        print("Waiting for Twitch authorization...")
        self.auth_event.wait()
        self.exchange_code_for_token()

    # Start local server to retrives twitch response
    def start_local_server(self):
        handler_self = self

        class AuthHandler(http.server.SimpleHTTPRequestHandler):
            # Disable request logging. Ensures application works as exe file with no console or log file
            def log_message(self, format, *args):
                return  

            def do_GET(handler):
                parsed_path = urlparse(handler.path)
                query_params = parse_qs(parsed_path.query)
                if "code" in query_params:
                    handler_self.auth_code = query_params["code"][0]
                    handler.send_response(200)
                    handler.send_header("Content-type", "text/html")
                    handler.end_headers()
                    handler.wfile.write(b"Authorization successful. You can close this window now.")
                    handler.wfile.flush()
                    handler_self.auth_event.set()
                else:
                    handler.send_response(400)
                    handler.end_headers()
                    handler.wfile.write(b"Authorization failed.")

        self.server = ThreadingTCPServer(("127.0.0.1", 8080), AuthHandler)
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()

    # Stop local server
    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    # Exchange access code for tokens
    def exchange_code_for_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "code": self.auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": TWITCH_APP_REDIRECT_URI
        }
        response = requests.post(url, data=data)
        token_data = response.json()
        
        if "access_token" in token_data:
            self.oauth_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            print("Twitch authentication successful!")
            self.save_tokens()
        else:
            show_popup("error", "Error exchanging code for token", "While trying to exchange auth code for token an error occoured:\n" + str(token_data))
            print("Error exchanging code for token:", token_data)
            exit(1)

    # Refresh expired or wrong token
    def refresh_twitch_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET
        }
        response = requests.post(url, data=data)
        token_data = response.json()
        
        if "access_token" in token_data:
            self.oauth_token = token_data["access_token"]
            self.refresh_token = token_data.get("refresh_token", self.refresh_token)
            self.save_tokens()
            print("Token refresh successful!")
            return self.oauth_token
        else:
            show_popup("error", "Error trying to refresh token", "While trying to to refresh the token an error occoured:\n" + str(token_data))
            print("Failed to refresh token:", token_data)
            exit(1)

    # Saves token to config.json
    def save_tokens(self):
        with open(CONFIG_PATH, "r") as file:
            config = json.load(file)
        config["twitch_oauth_token"] = self.oauth_token
        config["twitch_refresh_token"] = self.refresh_token
        with open(CONFIG_PATH, "w") as file:
            json.dump(config, file, indent=4)
        print("Tokens saved successfully!")
