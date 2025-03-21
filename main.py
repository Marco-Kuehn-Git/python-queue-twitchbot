import sys
import threading
import time
import asyncio
from PyQt6.QtWidgets import QApplication

from helper.popup import show_popup
from ui.ui import UI
from ui.controller import QueueController
from bot.bot_twitch import TwitchBot
from bot.queue_manager import QueueManager

def start_bot_loop(controller, shared_queue_manager):
    restart_count = 0
    while restart_count < 3:
        # Create and set a new event loop for this thread so that TwitchIO can use it.
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        # Create a new bot instance
        bot_instance = TwitchBot(controller, shared_queue_manager)
        
        # Run the bot instance in a separate thread
        bot_thread = threading.Thread(target=bot_instance.run)
        bot_thread.start()
        bot_thread.join()
        
        # Check if the bot signaled a restart due to a token refresh
        if bot_instance.should_restart:
            print("Bot instance ended due to token refresh. Restarting bot...")
            restart_count += 1
            time.sleep(2)
            continue
        else:
            print("Bot terminated normally. Exiting restart loop.")
            break
    else:
        # If we reached 5 restarts, warn the user.
        print("Maximum bot restarts reached. Please restart the application manually.")
        show_popup("warning", "Restart needed", "Tokens have been refreshed but the bot failed to restart.\nPlease restart the application.\n\n"
                                                "If this error continues to show, check your config.json file for any wrong values.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the shared queue manager
    shared_queue_manager = QueueManager()
    # Create the controller, passing the shared queue manager to it
    controller = QueueController(shared_queue_manager)
    
    ui = UI(controller)
    
    # Start the bot loop in a separate thread
    bot_loop_thread = threading.Thread(target=start_bot_loop, args=(controller, shared_queue_manager), daemon=True)
    bot_loop_thread.start()

    ui.show()
    sys.exit(app.exec())
    