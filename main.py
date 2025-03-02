import sys
import threading
from PyQt6.QtWidgets import QApplication
from ui.ui import QueueManager
from ui.controller import QueueController
from bot.bot_twitch import QueueBot

def start_bot(bot):
    bot.run()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = QueueController()
    ui = QueueManager(controller)
    bot = QueueBot(controller)

    # Start the bot on a separate thread
    bot_thread = threading.Thread(target=start_bot, args=(bot,), daemon=True)
    bot_thread.start()

    ui.show()
    sys.exit(app.exec())
    