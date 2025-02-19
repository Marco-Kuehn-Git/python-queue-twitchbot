import sys
import threading
from PyQt6.QtWidgets import QApplication
from ui.queue_manager_ui import QueueManager
from ui.queue_controller import QueueController
from bot.queue_manager import QueueBot

def start_bot(bot):
    """Runs the bot in a separate thread."""
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
    