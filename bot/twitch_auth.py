import json
import requests
import webbrowser
import http.server
import socketserver
import threading
import time
from urllib.parse import urlparse, parse_qs

from bot.config import (
    TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, TWITCH_OAUTH_TOKEN, TWITCH_REFRESH_TOKEN,
    TWITCH_APP_REDIRECT_URI, TWITCH_SCOPES
)

FAIL_SAFE_TIMEOUT = 60 # In Seconds


class TwitchAuthHandler:
    def __init__(self):
        self.auth_code = None
        self.oauth_token = None if not TWITCH_OAUTH_TOKEN else TWITCH_OAUTH_TOKEN
        self.refresh_token = None if not TWITCH_REFRESH_TOKEN else TWITCH_REFRESH_TOKEN
        self.server = None

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

    # Start local server to retrives twitch response
    def start_local_server(self):
        class AuthHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(handler):
                parsed_path = urlparse(handler.path)
                query_params = parse_qs(parsed_path.query)

                # Handle response
                if "code" in query_params:
                    self.auth_code = query_params["code"][0]
                    print("Authorization code received!")
                    handler.send_response(200)
                    handler.send_header("Content-type", "text/html")
                    handler.end_headers()
                    handler.wfile.write(b"Authorization successful. You can close this window.")
                    threading.Thread(target=self.stop_server).start()
                else:
                    handler.send_response(400)
                    handler.end_headers()
                    handler.wfile.write(b"Authorization failed.")

        self.server = socketserver.TCPServer(("", 8080), AuthHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Waiting for Twitch authorization...")

        # Timeout fail safe
        start_time = time.time()
        while self.auth_code is None and time.time() - start_time < FAIL_SAFE_TIMEOUT:
            time.sleep(1)

        if self.auth_code is None:
            print("Authorization timed out! Exiting...")
            self.stop_server()
            exit(1)
        
        self.exchange_code_for_token()

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
            self.refresh_token = token_data.get("refresh_token")
            print("Twitch authentication successful!")
            self.save_tokens()
        else:
            print("Error exchanging code for token:", token_data)
            exit(1)

    # Refresh expired token
    def refresh_twitch_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": TWITCH_REFRESH_TOKEN,
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET
        }

        response = requests.post(url, data=data)
        token_data = response.json()
        
        if "access_token" in token_data:
            self.oauth_token = token_data["access_token"]
            self.refresh_token = token_data.get("refresh_token", TWITCH_REFRESH_TOKEN)
            self.save_tokens()
            print("Token refreshed successfully!")
        else:
            print("Failed to refresh token:", token_data)
            exit(1)

    def save_tokens(self):
        with open("config.json", "r") as file:
            config = json.load(file)
        
        config["twitch_oauth_token"] = self.oauth_token
        config["twitch_refresh_token"] = self.refresh_token
        
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

        print("Tokens saved successfully!")
