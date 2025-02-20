import json
import requests
from datetime import datetime
from twitchio.ext import commands

from bot.config import TWITCH_OAUTH_TOKEN, TWITCH_REFRESH_TOKEN, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET ,TWITCH_CHANNEL

class QueueBot(commands.Bot):
    def __init__(self, controller):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )
        self.controller = controller
        self.queue = []

    async def event_ready(self):
        print(f"Bot is online as {self.nick}")
        self.controller.connection_status.emit(True)

    async def event_disconnect(self):
        print("Bot disconnected!")
        self.controller.ui.connection_status_changed.emit(False)

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    # Refresh Twitch OAuth token when expired and update config.json.
    def refresh_token(self):
        with open("config.json", "r") as file:
            config = json.load(file)

        refresh_token = TWITCH_REFRESH_TOKEN
        client_id = TWITCH_CLIENT_ID
        client_secret = TWITCH_CLIENT_SECRET

        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(url, params=params)
        data = response.json()

        if "access_token" in data:
            # Update tokens in config.json
            config["TWITCH_OAUTH_TOKEN"] = data["access_token"]
            config["TWITCH_REFRESH_TOKEN"] = data.get("refresh_token", refresh_token)

            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

            print("Token refreshed successfully!")
            return data["access_token"]
        else:
            print("Failed to refresh token:", data)
            return None

    @commands.command(name="join")
    async def join_queue(self, ctx):
        username = ctx.author.name
        sub_tier = self.get_sub_tier(ctx.author)

        # Get previous queue count from the controller, default to 0
        times_queued = self.controller.get_queue_count(username)
        # Get timestamp for when user joined the queue
        join_time = datetime.now().timestamp()

        # Prevent duplicate queue entries
        if any(user[0] == username for user in self.queue):
            await ctx.send(f"@{username}, you're already in the queue!")
            return

        # Add user to queue, sort and update the ui
        self.queue.append((username, sub_tier, times_queued, join_time))
        self.sort_queue()
        self.controller.update_queue(self.queue)

        await ctx.send(f"@{username}, you joined the queue!")

    @commands.command(name="leave")
    async def leave_queue(self, ctx):
        username = ctx.author.name
        
        # Check if user is in queue and remove if true
        if any(user[0] == username for user in self.queue):
            self.queue = [user for user in self.queue if user[0] != username]
            self.controller.update_queue(self.queue)
            await ctx.send(f"@{username}, you left the queue!")
        else:
            await ctx.send(f"@{username}, you're not in the queue!")

    # Returns the sub tier (0 = no sub, 1 = tier 1, etc.)
    def get_sub_tier(self, user):
        return user.subscription_tier // 1000 if user.is_subscriber else 0

    # Sorts the queue by: (times queued ascending, sub tier descending)
    def sort_queue(self):
        self.queue.sort(key=lambda x: (x[2], -x[1], x[3]))
