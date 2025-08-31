# Twitch Queue Bot

## About the Project
A simple self-hosted Twitch bot written in Python that allows viewers to join a queue. The streamer can manage the queue and select viewers through a UI.

Viewers are sorted based on the number of times queued, subscription tier, and time joined.

---

### Planned Features  

Features listed are in no particular order:  

- **Persistant Queue Data** - Save current queue in case the application crashes. Option to load previous queue when starting the application.
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

3. **Get Your Client Secret**
   - Still on the Twitch Developer Console website, go to the "Applications" tab and click "Manage" on your application
   - Find your **Client ID** at the bottom of the page
   - Click "Generate New Secret" to get your **Client Secret** (__DO NOT SHARE THIS!__)

4. **Run the Application**
   - On your first start, an empty config file will be automaticly created.
   - Open the settings on the top right and set your Twitch Channel, Client Id and Secret. Then click save.
   - Now authorize a Twitch account with the **Authorize Twitch** Button.
   - Any Twitch account can be used, but the account used will send confirmation messages for joining and leaving the queue.

> **Note:** If prompted by the firewall, click "Allow." Then restart the authorization process. The app temporarily starts a local server to retrieve the authentication data and closes it afterward.

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

3. **Follow Steps 2 and 3 from the User Installation**

4. **Run the Bot**
   ```sh
   python main.py
   ```

