# python-queue-twitchbot
A simple twitch bot written in python that allowes viewers to join a queue. The streamer is able to select veiwers from this queue through a UI.

The viewers are sorted based on times queued, sub tier and time joined.

<br />

If wanting to run this as a script:

Create a config.json file inside the bot folder.
The content should look like this:
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
    ],
    "twitch_channel": "your_twitch_channel"
```
