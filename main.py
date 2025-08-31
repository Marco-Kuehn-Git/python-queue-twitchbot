import sys
import threading
import time
import asyncio
from PyQt6.QtWidgets import QApplication

from ui.ui import UI
from ui.controller import QueueController
from bot.bot_twitch import TwitchBot
from bot.queue_manager import QueueManager
from bot.twitch_auth import TwitchAuthHandler
from bot.config import Config
from helper.helper import show_popup, can_connect_with_token

def wait_for_valid_token(controller, config):
    """
    Wait until a valid Twitch token is available.
    If the token is invalid, attempt to refresh it.
    """
    while True:
        token = config.twitch_oauth_token
        if token:
            if can_connect_with_token(token, config):
                print("Valid Twitch token found.")
                controller.status_message.emit("Twitch authorized. Connecting...")
                return
            else:
                print("Invalid Twitch token found. Refreshing token...")
                controller.status_message.emit("Refreshing Twitch token...")
                TwitchAuthHandler(config).refresh_twitch_token()
        else:
            print("Waiting for Twitch token...")
            controller.status_message.emit("Waiting for Twitch authorization...")
        time.sleep(2)

def start_bot_loop(controller, shared_queue_manager, config):
    """
    Wait for a valid token, then repeatedly run the Twitch bot.
    The bot is restarted up to three times if a token refresh occurs.
    """
    # Wait for a valid token before starting the bot
    wait_for_valid_token(controller, config)

    restart_count = 0
    while restart_count < 3:
        # Create and set a new event loop for this thread so TwitchIO can use it.
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        # Create and run a new Twitch bot instance
        bot_instance = TwitchBot(controller, shared_queue_manager, config) 
        bot_thread = threading.Thread(target=bot_instance.run)
        bot_thread.start()
        bot_thread.join()
        
        # Restart the bot if the token was refreshed, otherwise exit loop.
        if bot_instance.should_restart:
            print("Bot instance ended due to token refresh. Restarting bot...")
            restart_count += 1
            time.sleep(2)
            continue
        else:
            print("Bot terminated normally. Exiting restart loop.")
            break
    else:
        print("Maximum bot restarts reached. Please restart the application manually.")
        show_popup(
            "warning",
            "Restart needed",
            ("Tokens have been refreshed but the bot failed to restart.\n"
             "Please restart the application.\n\n"
             "If this error continues, check your config.json for any incorrect values.")
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = Config()

    # Initialize shared queue manager and controller
    shared_queue_manager = QueueManager(config)
    controller = QueueController(shared_queue_manager)
    
    # Create and display the main UI
    ui = UI(controller, config)
    
    # Start the Twitch bot loop in a separate daemon thread
    bot_loop_thread = threading.Thread(
        target=start_bot_loop, args=(controller, shared_queue_manager, config), daemon=True
    )
    bot_loop_thread.start()
    
    ui.show()
    sys.exit(app.exec())