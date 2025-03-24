class QueueManager:
    """
    Manages the viewer queue and selected lists.
    """
    def __init__(self):
        self.queue = []
        self.selected = []

    def add_user(self, username, sub_tier, times_queued, join_time):
        """
        Adds a user to the queue if they are not already present in either list.
        Returns True if the user is added, otherwise False.
        """
        if any(entry[0] == username for entry in self.queue) or any(entry[0] == username for entry in self.selected):
            return False
        self.queue.append((username, sub_tier, times_queued, join_time))
        self.sort_queue()
        return True

    def remove_from_queue(self, username):
        """
        Removes a user from the queue.
        Returns True if the user was found and removed, otherwise False.
        """
        if any(entry[0] == username for entry in self.queue):
            self.queue = [entry for entry in self.queue if entry[0] != username]
            return True
        return False

    def remove_user(self, username):
        """
        Removes a user from the selected list.
        Returns True if the user was found and removed, otherwise False.
        """
        if any(entry[0] == username for entry in self.selected):
            self.selected = [entry for entry in self.selected if entry[0] != username]
            return True
        return False

    def sort_queue(self):
        """
        Sorts the queue based on:
          - times queued (ascending),
          - subscriber tier (descending),
          - join time (ascending).
        """
        self.queue.sort(key=lambda x: (x[2], -x[1], x[3]))

    def move_to_selected(self, username):
        """
        Moves a user from the queue to the selected list.
        Returns True if the user was found and moved, otherwise False.
        """
        user = next((entry for entry in self.queue if entry[0] == username), None)
        if user:
            self.queue.remove(user)
            self.selected.append(user)
            return True
        return False

    def move_back_to_queue(self, username):
        """
        Moves a user from the selected list back to the queue.
        Returns True if the user was found and moved, otherwise False.
        """
        user = next((entry for entry in self.selected if entry[0] == username), None)
        if user:
            self.selected.remove(user)
            self.queue.append(user)
            self.sort_queue()
            return True
        return False

    def get_queue(self):
        """
        Returns the current queue list.
        """
        return self.queue

    def get_selected(self):
        """
        Returns the current selected list.
        """
        return self.selected
