from twitchio.ext import commands

from config import TWITCH_OAUTH_TOKEN, TWITCH_CHANNEL

class QueueBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )

        # Queue format: [(username, sub_tier, times_queued)]
        self.queue = []
        self.times_queued = {}  # Tracks how many times a user was selected

    async def event_ready(self):
        print(f"Bot is online as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return  # Ignore own messages

        await self.handle_commands(message)

    @commands.command(name="join")
    async def join_queue(self, ctx):
        username = ctx.author.name
        sub_tier = self.get_sub_tier(ctx.author)
        times_queued = self.times_queued.get(username, 0)

        # Check if user is already in the queue
        if any(user[0] == username for user in self.queue):
            await ctx.send(f"@{username}, you are already in the queue!")
            return

        # Add to queue
        self.queue.append((username, sub_tier, times_queued))
        self.sort_queue()
        await ctx.send(f"@{username} joined the queue!")

    @commands.command(name="leave")
    async def leave_queue(self, ctx):
        username = ctx.author.name
        
        # Check if the user is in the queue
        if not any(user[0] == username for user in self.queue):
            await ctx.send(f"@{username}, you are not in the queue!")
        else:
            # Remove from queue
            self.queue = [user for user in self.queue if user[0] != username]
            await ctx.send(f"@{username}, you left the queue!")

    # Returns the sub tier of the user (T3 = 3, T2 = 2, T1 = 1, No sub = 0)
    def get_sub_tier(self, user):
        if user.is_subscriber:
            return user.subscription_tier // 1000  # Convert 3000 -> 3, 2000 -> 2, etc.
        return 0

    # Sort queue by (times queued ascending, sub tier descending)
    def sort_queue(self):
        self.queue.sort(key=lambda x: (x[2], -x[1]))

    # Called when a user is removed from selection, increasing queue count
    def remove_from_selected(self, username):
        if username in [user[0] for user in self.queue]:
            self.queue = [user for user in self.queue if user[0] != username]
            self.times_queued[username] = self.times_queued.get(username, 0) + 1
            self.sort_queue()
