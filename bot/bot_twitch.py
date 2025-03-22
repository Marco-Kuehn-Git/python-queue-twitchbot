from datetime import datetime
from twitchio.ext import commands

from bot.twitch_auth import TwitchAuthHandler
from bot.config import load_config, TWITCH_CHANNEL
from helper.popup import show_popup

class TwitchBot(commands.Bot):
    def __init__(self, controller, queue_manager):
        config = load_config()
        token_from_config = config["twitch_oauth_token"]
        super().__init__(
            token=token_from_config,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )
        self.controller = controller
        self.queue_manager = queue_manager
        self.should_restart = False

    async def event_ready(self):
        print(f"Bot is online as {self.nick}")
        self.controller.connection_status.emit(True)

    async def event_disconnect(self):
        print("Bot disconnected!")
        self.controller.ui.connection_status_changed.emit(False)
        show_popup("warning", "Bot disconnected!", "The bot got disconnected from Twitch")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name="join")
    async def join_queue(self, ctx):
        username = ctx.author.name
        sub_tier = self.get_sub_tier(ctx.author)
        times_queued = self.controller.get_queue_count(username)
        join_time = datetime.now().timestamp()

        # Use the shared queue manager to add the user
        if not self.queue_manager.add_user(username, sub_tier, times_queued, join_time):
            await ctx.send(f"@{username}, you're already in the queue!")
            return

        # Update the UI with the latest queue
        self.controller.update_ui()
        await ctx.send(f"@{username}, you joined the queue!")

    @commands.command(name="leave")
    async def leave_queue(self, ctx):
        username = ctx.author.name
        if any(entry[0] == username for entry in self.queue_manager.get_selected()):
            await ctx.send(f"@{username}, you're not in the queue! You are selected!")
            return

        if self.queue_manager.remove_from_queue(username):
            self.controller.update_ui()
            await ctx.send(f"@{username}, you left the queue!")
        else:
            await ctx.send(f"@{username}, you're not in the queue!")

    # Returns the sub tier (0 = no sub, 1 = tier 1, etc.)
    def get_sub_tier(self, user):
        if user.is_subscriber:
            # Unclean subs are displayed like this (Tier3 9Months: 3009, Tier2 11Months:2011, Tier1 4Months:4)
            sub_tier_unclean = int(user.badges.get("subscriber"))
            # Using max() to make sure tier 1 subs actually show up 1
            sub_tier_clean = max(sub_tier_unclean // 1000, 1)
            if sub_tier_clean == 0:
                sub_tier_clean = 1
            print("Unclean sub tier:", sub_tier_unclean,"Clean sub tier:", sub_tier_clean)
            return sub_tier_clean
        else:
            return 0

    # Override the run method to handle token refresh on 401 or invalid token
    def run(self):
        try:
            super().run()
        except Exception as e:
            error_str = str(e).lower()
            token_error = False
        
            if "401" in error_str or ("invalid" in error_str and "token" in error_str):
                token_error = True
            elif e.__class__.__name__.lower() == "loginfailure":
                token_error = True

            elif token_error:
                print("Detected invalid or expired token. Attempting token refresh...")
                auth_handler = TwitchAuthHandler()
                auth_handler.refresh_twitch_token()

                # Update bots token with the new one
                self._http.token = auth_handler.oauth_token
                self.token = auth_handler.oauth_token
                print("Token refreshed successfully.")

                # Signal that the bot should restartd
                self.should_restart = True

            else:
                show_popup("error", "Failed to refresh tokens!", "Failed to refresh tokens:\n" + str(e))
                raise e

