# Twitch Queue Bot

## About the Project
A simple self-hosted Twitch bot written in Python that allows viewers to join a queue. The streamer can manage the queue and select viewers through a UI.

Viewers are sorted based on the number of times queued, subscription tier, and time joined.

---

### Planned Features  

Features listed are in no particular order:  

- **UI-Based Configuration** – Enable users to modify `config.json` settings through a graphical interface.  
- **Advanced Queue Sorting** – Provide different queue sorting options. Changable in the settings.
- **Persistant Queue Data** - Save current queue in case the application crashes. Option to load previous queue when starting the application.
- **Optional YouTube Live Chat Integration** – Add support for YouTube Live Chat, allowing users to choose Twitch, YouTube, or both. 
- **Support for Additional OS** - Make the application available on Linux and macOS.

---

## Installation (User)

1. **Download and Extract**
   - Download and extract the latest `QueueManager.zip` file from the [Releases](https://github.com/Marco-Kuehn-Git/python-queue-twitchbot/releases) section.

2. **Create a Twitch Application**
   - Visit the [Twitch Developer Console](https://dev.twitch.tv/console)
   - Log in with your Twitch account
   - Click on the "Applications" tab
   - Click "Register Your Application"
   - Fill in the details:
     - **Name**: Choose any name
     - **OAuth Redirect URL**: `http://localhost:8080`
     - **Category**: "Chat Bot"
     - **Client Type**: "Confidential"
   - Click "Create"

3. **Add Your Client ID and Secret to `config.json`**
   - Go to the "Applications" tab and click "Manage" on your application
   - Find your **Client ID** at the bottom of the page
   - Click "Generate New Secret" to get your **Client Secret** (__DO NOT SHARE THIS!__)
   - Save both values in your `config.json` file:

   ```json
   {
     "twitch_oauth_token": "",
     "twitch_refresh_token": "",
     "twitch_client_id": "YOUR_CLIENT_ID",
     "twitch_client_secret": "YOUR_CLIENT_SECRET",
     "twitch_app_redirect_uri": "http://localhost:8080",
     "twitch_scopes": [
         "chat:read",
         "chat:edit"
     ],
     "twitch_channel": "YOUR_TWITCH_CHANNEL"
   }
   ```

4. **Add Your Twitch Channel**
   - Inside `config.json`, replace `your_twitch_channel` with your actual Twitch channel name.

5. **Run the Application**
   - On your first start, you need to authorize a Twitch account with the **Authorize Twitch** Button.
   - Any Twitch account can be used, but the account used will send confirmation messages for joining and leaving the queue.

> **Note:** If prompted by the firewall, click "Allow." Then restart the authorization process. The bot temporarily starts a local server to retrieve authentication data and closes it afterward.

---

## Installation (Developer)

1. **Clone the Repository**
   ```sh
   git clone https://github.com/Marco-Kuehn-Git/python-queue-twitchbot.git
   cd python-queue-twitchbot
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Create a `config.json` File in the `bot` Folder**
   ```json
   {
     "twitch_oauth_token": "",
     "twitch_refresh_token": "",
     "twitch_client_id": "YOUR_CLIENT_ID",
     "twitch_client_secret": "YOUR_CLIENT_SECRET",
     "twitch_app_redirect_uri": "http://localhost:8080",
     "twitch_scopes": [
         "chat:read",
         "chat:edit"
     ],
     "twitch_channel": "YOUR_TWITCH_CHANNEL"
   }
   ```

4. **Follow Steps 2-4 from the User Installation**

5. **Run the Bot**
   ```sh
   python main.py
   ```

