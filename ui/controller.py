from PyQt6.QtCore import QObject, pyqtSignal

class QueueController(QObject):
    # Signals for UI updates
    queue_updated = pyqtSignal(list)
    selected_updated = pyqtSignal(list)
    connection_status = pyqtSignal(bool)
    status_message = pyqtSignal(str)

    def __init__(self, queue_manager):
        """
        Initialize the controller with a shared queue manager.
        """
        super().__init__()
        self.queue_manager = queue_manager
        self.queue_count = {}

    def update_ui(self):
        """
        Emit signals to update both the queue and the selected lists in the UI.
        """
        self.queue_updated.emit(self.queue_manager.get_queue())
        self.selected_updated.emit(self.queue_manager.get_selected())

    def update_selected(self, selected):
        """
        Emit the new selected list.
        """
        self.selected_updated.emit(selected)

    def increase_queue_count(self, name):
        """
        Increase the count of how many times a user has joined the queue.
        """
        self.queue_count[name] = self.queue_count.get(name, 0) + 1

    def get_queue_count(self, name):
        """
        Return the number of times a user has joined the queue (default is 0).
        """
        return self.queue_count.get(name, 0)
