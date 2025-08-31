from datetime import datetime
from twitchio.ext import commands

from bot.twitch_auth import TwitchAuthHandler
from helper.helper import show_popup

class TwitchBot(commands.Bot):
    """
    Twitch chat bot for managing the viewer queue.
    """
    def __init__(self, controller, queue_manager, config):
        self.config = config
        token_from_config = config.twitch_oauth_token
        super().__init__(
            token=token_from_config,
            prefix="!",
            initial_channels=[config.twitch_channel]
        )
        self.controller = controller
        self.queue_manager = queue_manager
        self.should_restart = False

    async def event_ready(self):
        """
        Called when the bot is ready. Emits connection status.
        """
        print(f"Bot is online as {self.nick}")
        self.controller.connection_status.emit(True)

    async def event_disconnect(self):
        """
        Called when the bot disconnects. Emits disconnection status and shows a popup.
        """
        print("Bot disconnected!")
        self.controller.connection_status.emit(False)
        show_popup("warning", "Bot disconnected!", "The bot got disconnected from Twitch")

    async def event_message(self, message):
        """
        Processes incoming messages. Ignores messages sent by the bot itself.
        """
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name="join")
    async def join_queue(self, ctx):
        """
        Command to add a user to the queue.
        """
        username = ctx.author.name

        if self.controller.queue_closed:
            await ctx.send(f"@{username}, the queue is currently closed. You can’t join right now.")
            return

        sub_tier = self.get_sub_tier(ctx.author)
        times_queued = self.controller.get_queue_count(username)
        join_time = datetime.now().timestamp()

        # If the user is in the selected list, they should not join.
        # Prevents users from joining again before thier times queued counter is increased.
        if any(entry[0] == username for entry in self.queue_manager.get_selected()):
            await ctx.send(f"@{username}, You can't join right now! You are up!")
            return

        # Add user to the shared queue if not already present.
        if not self.queue_manager.add_user(username, sub_tier, times_queued, join_time):
            await ctx.send(f"@{username}, you're already in the queue!")
            return

        self.controller.update_ui()
        await ctx.send(f"@{username}, you joined the queue!")

    @commands.command(name="leave")
    async def leave_queue(self, ctx):
        """
        Command to remove a user from the queue.
        """
        username = ctx.author.name
        # If the user is in the selected list, they should not leave.
        # Prevents user from leaving withtout increasing times queued counter.
        if any(entry[0] == username for entry in self.queue_manager.get_selected()):
            await ctx.send(f"@{username}, You can't leave right now! You are up!")
            return

        if self.queue_manager.remove_from_queue(username):
            self.controller.update_ui()
            await ctx.send(f"@{username}, you left the queue!")
        else:
            await ctx.send(f"@{username}, you're not in the queue!")

    @commands.command(name="queue")
    async def print_queue(self, ctx):
        """
        Command to show the next 9 viewers and how many remaining people are in the queue.
        """
        username = ctx.author.name
        queue = self.queue_manager.get_queue()

        if not queue:
            await ctx.send("The queue is currently empty.")
            return

        max_display = 9
        display_queue = [entry[0] for entry in queue[:max_display]]
        queue_message = ", ".join(display_queue)

        # Check if there are more people in the queue
        remaining = len(queue) - len(display_queue)

        if remaining > 0:
            await ctx.send(f"@{username}, Next in queue: {queue_message} (+{remaining} more)")
        else:
            await ctx.send(f"@{username},Next in queue: {queue_message}")



    def get_sub_tier(self, user):
        """
        Determine and return the subscription tier for a user.
        Returns 0 if the user is not a subscriber.
        """
        if user.is_subscriber:
            # Convert raw subscriber badge value into a clean tier (ensuring a minimum of 1)
            # Ensuring the minium of 1 is needed to properly display tier 1 subscribers
            sub_tier_unclean = int(user.badges.get("subscriber"))
            sub_tier_clean = max(sub_tier_unclean // 1000, 1)
            print("Unclean sub tier:", sub_tier_unclean, "Clean sub tier:", sub_tier_clean)
            return sub_tier_clean
        else:
            return 0

    def run(self):
        """
        Override the run method to handle token refresh when encountering authentication issues.
        """
        try:
            super().run()
        except Exception as e:
            error_str = str(e).lower()
            token_error = False

            if "401" in error_str or ("invalid" in error_str and "token" in error_str):
                token_error = True
            elif e.__class__.__name__.lower() == "loginfailure":
                token_error = True

            if token_error:
                print("Detected invalid or expired token. Attempting token refresh...")
                auth_handler = TwitchAuthHandler(self.config)
                auth_handler.refresh_twitch_token()

                # Update bots token with the refreshed token
                self._http.token = auth_handler.oauth_token
                self.token = auth_handler.oauth_token
                print("Token refreshed successfully.")

                # Signal that the bot should restart
                self.should_restart = True
            else:
                show_popup("error", "Failed to refresh tokens!", "Failed to refresh tokens:\n" + str(e))
                raise e
