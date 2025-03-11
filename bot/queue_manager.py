# bot/queue_manager.py

class QueueManager:
    def __init__(self):
        self.queue = []
        self.selected = []

    def add_user(self, username, sub_tier, times_queued, join_time):
        # Prevent duplicate entries in both lists.
        if any(entry[0] == username for entry in self.queue) or any(entry[0] == username for entry in self.selected):
            return False
        self.queue.append((username, sub_tier, times_queued, join_time))
        self.sort_queue()
        return True

    def remove_from_queue(self, username):
        # Only remove the user if they are in the regular queue.
        if any(entry[0] == username for entry in self.queue):
            self.queue = [entry for entry in self.queue if entry[0] != username]
            return True
        return False

    def remove_user(self, username):
        # Remove from both lists (used for administrative removal from UI).
        removed = False
        for lst in (self.queue, self.selected):
            if any(entry[0] == username for entry in lst):
                lst[:] = [entry for entry in lst if entry[0] != username]
                removed = True
        return removed

    def sort_queue(self):
        # Sort the queue by (times queued ascending, sub tier descending, join time ascending)
        self.queue.sort(key=lambda x: (x[2], -x[1], x[3]))

    def move_to_selected(self, username):
        user = next((entry for entry in self.queue if entry[0] == username), None)
        if user:
            self.queue.remove(user)
            self.selected.append(user)
            return True
        return False

    def move_back_to_queue(self, username):
        user = next((entry for entry in self.selected if entry[0] == username), None)
        if user:
            self.selected.remove(user)
            self.queue.append(user)
            self.sort_queue()
            return True
        return False

    def get_queue(self):
        return self.queue

    def get_selected(self):
        return self.selected
