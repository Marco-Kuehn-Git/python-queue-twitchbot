from PyQt6.QtCore import QObject, pyqtSignal

class QueueController(QObject):

    # Signals for UI updates
    queue_updated = pyqtSignal(list)
    selected_updated = pyqtSignal(list)
    connection_status = pyqtSignal(bool)
    status_message = pyqtSignal(str)

    def __init__(self, queue_manager):
        super().__init__()
        self.queue_manager = queue_manager
        self.queue_count = {}

    # Update queue list in the ui
    def update_ui(self):
        self.queue_updated.emit(self.queue_manager.get_queue())
        self.selected_updated.emit(self.queue_manager.get_selected())

    # Update selected list
    def update_selected(self, selected):
        self.selected = selected
        self.selected_updated.emit(selected)

    # Increase number of times user has queued
    def increase_queue_count(self, name):
        self.queue_count[name] = self.queue_count.get(name, 0) + 1

    # Get the nuber of times user has queued (default 0)
    def get_queue_count(self, name):
        return self.queue_count.get(name, 0)
