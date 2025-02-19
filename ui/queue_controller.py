from PyQt6.QtCore import QObject, pyqtSignal

class QueueController(QObject):

    # Signals for UI updates
    queue_updated = pyqtSignal(list)
    selected_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.queue = []
        self.selected = []
        self.queue_count = {}

    # Update queue list
    def update_queue(self, queue):
        self.queue = queue
        self.queue_updated.emit(queue)

    # Update selected list
    def update_selected(self, selected):
        self.selected = selected
        self.selected_updated.emit(selected)

    # Increase number of times user has queued
    def increase_queue_count(self, name):
        if name in self.queue_count:
            self.queue_count[name] += 1
        else:
            self.queue_count[name] = 1

    # Get the nuber of times user has queued (default 0)
    def get_queue_count(self, name):
        return self.queue_count.get(name, 0)
