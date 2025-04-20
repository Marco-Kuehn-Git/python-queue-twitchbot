import json
import requests
import webbrowser
import http.server
import socketserver
import threading
from urllib.parse import urlparse, parse_qs

from helper.helper import show_popup

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class TwitchAuthHandler:
    """
    Handles Twitch authentication by starting a local server to capture the auth code,
    exchanging it for tokens, and refreshing tokens when necessary.
    """
    def __init__(self, config):
        self.config = config
        self.oauth_token = self.config.twitch_oauth_token if self.config.twitch_oauth_token else None
        self.refresh_token = self.config.twitch_refresh_token if self.config.twitch_refresh_token else None
        self.auth_code = None
        self.server = None
        self.auth_event = threading.Event()

    def start_auth(self):
        """
        Starts the Twitch authorization process by opening the auth URL,
        starting a local server to capture the response, and exchanging the auth code for tokens.
        """
        print("Starting Twitch authorization...")
        auth_url = (
            f"https://id.twitch.tv/oauth2/authorize?"
            f"client_id={self.config.twitch_client_id}&"
            f"response_type=code&"
            f"redirect_uri={self.config.twitch_app_redirect_uri}&"
            f"scope={' '.join(self.config.twitch_scopes)}"
        )
        webbrowser.open(auth_url)
        self.start_local_server()
        
        print("Waiting for Twitch authorization...")
        self.auth_event.wait()
        self.exchange_code_for_token()
        self.stop_server()

    def start_local_server(self):
        """
        Starts a local TCP server to listen for Twitch's authorization redirect.
        """
        handler_self = self

        class AuthHandler(http.server.SimpleHTTPRequestHandler):
            # Disable logging for cleaner output and possibillity to run executable wihtout console
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

    def exchange_code_for_token(self):
        """
        Exchanges the captured authorization code for an access token and refresh token.
        """
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.config.twitch_client_id,
            "client_secret": self.config.twitch_client_secret,
            "code": self.auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.config.twitch_app_redirect_uri
        }
        response = requests.post(url, data=data)
        token_data = response.json()
        
        if "access_token" in token_data:
            self.oauth_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            print("Twitch authentication successful!")
            self.save_tokens()
        else:
            show_popup("error", "Error exchanging code for token",
                       "Error during token exchange:\n" + str(token_data))
            print("Error exchanging code for token:", token_data)
            exit(1)

    def refresh_twitch_token(self):
        """
        Refreshes the access token using the current refresh token.
        """
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.config.twitch_client_id,
            "client_secret": self.config.twitch_client_secret
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
            show_popup("error", "Error refreshing token",
                       "Error during token refresh:\n" + str(token_data))
            print("Failed to refresh token:", token_data)
            exit(1)

    def save_tokens(self):
        """
        Saves the current access and refresh tokens to the configuration file.
        """
        self.config.twitch_oauth_token = self.oauth_token
        self.config.twitch_refresh_token = self.refresh_token
        self.config.save_config()

    def stop_server(self):
        """
        Stops the local server used for authentication.
        """
        if self.server:
            self.server.shutdown()
            self.server.server_close()