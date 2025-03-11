import sys
import threading
from PyQt6.QtWidgets import QApplication

from ui.ui import UI
from ui.controller import QueueController
from bot.bot_twitch import TwitchBot
from bot.queue_manager import QueueManager

def start_bot(bot):
    bot.run()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    shared_queue_manager = QueueManager()
    controller = QueueController(shared_queue_manager)

    ui = UI(controller)
    twitch_bot = TwitchBot(controller, shared_queue_manager)

    # Start the Twitch bot on a separate thread
    bot_thread = threading.Thread(target=start_bot, args=(twitch_bot,), daemon=True)
    bot_thread.start()

    ui.show()
    sys.exit(app.exec())
    