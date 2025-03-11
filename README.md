# python-queue-twitchbot
A simple twitch bot written in python that allowes viewers to join a queue. The streamer is able to select veiwers from this queue through a UI.

<br />

Create a config.json file at the same level as main.py
<br />
   ```sh
   {
    "twitch_oauth_token": "",
    "twitch_refresh_token": "",
    "twitch_client_id": "your_twitch_client_id",
    "twitch_client_secret": "your_twitch_client_secret",
    "twitch_app_redirect_uri": "http://localhost:8080",
    "twitch_scopes": [
        "chat:read",
        "chat:edit"
    ]
```
