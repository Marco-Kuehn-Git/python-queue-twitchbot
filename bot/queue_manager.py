# bot/queue_manager.py

class QueueManager:
    def __init__(self):
        self.queue = []
        self.selected = []

    # Adds user to queue(Called when user uses !join)
    def add_user(self, username, sub_tier, times_queued, join_time):
        # Prevent duplicate entries in both lists.
        if any(entry[0] == username for entry in self.queue) or any(entry[0] == username for entry in self.selected):
            return False
        self.queue.append((username, sub_tier, times_queued, join_time))
        self.sort_queue()
        return True

    # Remove user from queue (Called when user uses !leave)
    def remove_from_queue(self, username):
        # Only remove the user if they are in the regular queue.
        if any(entry[0] == username for entry in self.queue):
            self.queue = [entry for entry in self.queue if entry[0] != username]
            return True
        return False

    # Remove user from selected. (Called when hitting 'x' on UI)
    def remove_user(self, username):
        for lst in (self.selected):
            if any(entry[0] == username for entry in lst):
                lst[:] = [entry for entry in lst if entry[0] != username]
                return True
        return False

    # Sort the queue by (times queued ascending, sub tier descending, join time ascending)
    def sort_queue(self):
        self.queue.sort(key=lambda x: (x[2], -x[1], x[3]))

    # Moove user from queue to selected list
    def move_to_selected(self, username):
        user = next((entry for entry in self.queue if entry[0] == username), None)
        if user:
            self.queue.remove(user)
            self.selected.append(user)
            return True
        return False

    # Moove user from selected back to queue list
    def move_back_to_queue(self, username):
        user = next((entry for entry in self.selected if entry[0] == username), None)
        if user:
            self.selected.remove(user)
            self.queue.append(user)
            self.sort_queue()
            return True
        return False

    # Get the list of viewers in queue
    def get_queue(self):
        return self.queue

    # Get the list of viewers in selected
    def get_selected(self):
        return self.selected
