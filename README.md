# Twitch Queue Bot

## About the Project
A simple self-hosted Twitch bot written in Python that allows viewers to join a queue. The streamer can manage the queue and select viewers through a UI.  

To handle the communications with Twitch's API, the app uses [TwitchIO](https://twitchio.dev/en/latest/), and for the UI, the app uses [PyQt6](https://pypi.org/project/PyQt6/).

Since it is self hosted, it requieres a bit of work from your end to setup, but Twitch makes it farily easy.

---
### Features:
1. Vewers can join and leave the queue with `!join` and `!leave`.
2. Viewers can use `!queue` to view the current queue.
3. The app tracks how many times a viewer has played and what tier of sub they are  
   - Times queued resets after restart.
4. The streamer can close the queue preventng viewers from joining.
5. You can select between the following queue order:
   - number of times queued and subscription tier (selected by default)
   - subscribtion tier
   - number of times queued
   - time joined

---

### Planned Features  

Features listed are in no particular order and not guranteed to be implemented:  

- **Persistant Queue Data** - Save current queue in case the application crashes. Option to load previous queue when starting the application.
- **Sub only mode** - Make a setting that only allows subs to join. Maybe with minimum tier selection.
- **Support for Additional OS** - Make the application available on Linux and macOS. Currently its only available for Windows.
- **Add auto updates** - Give users the option to update the app without having to download the newest version here everytime.

---

## Installation (User)

1. **Download and Extract**
   - Download and extract the latest `QueueManager.zip` file from the [Releases](https://github.com/Marco-Kuehn-Git/python-queue-twitchbot/releases).

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
   - Any Twitch account you own can be used. The account used will send confirmation messages for joining and leaving the queue.

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

4. **Run the App with**
   ```sh
   python main.py
   ```
   Follow step 4 of the User Installation
