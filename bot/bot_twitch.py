from datetime import datetime
from twitchio.ext import commands

from helper.popup import show_popup
from bot.twitch_auth import TwitchAuthHandler
from bot.config import TWITCH_OAUTH_TOKEN, TWITCH_CHANNEL

class TwitchBot(commands.Bot):
    def __init__(self, controller, queue_manager):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )
        self.controller = controller
        self.queue_manager = queue_manager

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
            sub_tier_unclean = int(user.badges.get("subscriber"))
            sub_tier_clean = sub_tier_unclean // 1000
            return sub_tier_clean
        else:
            return 0

    # Override the run method to handle token refresh on 401 errors.
    def run(self):
        try:
            super().run()
        except Exception as e:
            error_str = str(e).lower()
            token_error = False
            # Check for 401 status or "invalid token" phrases in the error message.
            if "401" in error_str or ("invalid" in error_str and "token" in error_str):
                token_error = True
            # Additionally, check if the exception type indicates a login failure.
            elif e.__class__.__name__.lower() == "loginfailure":
                token_error = True
            if token_error:
                print("Detected invalid or expired token. Attempting token refresh...")
                auth_handler = TwitchAuthHandler()
                auth_handler.refresh_twitch_token()
                
                self._http.token = auth_handler.oauth_token
                self.token = auth_handler.oauth_token
                print("Token refreshed successfully. Please restart the application.")
                show_popup("info", "Token Refresh", 
                           "The tokens had to be automatically refreshed.\n"
                           "Please restart the application for the changes to take effect.")
            else:
                raise e

