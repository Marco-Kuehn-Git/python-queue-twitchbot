from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, 
    QHBoxLayout, QListWidgetItem, QGroupBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from .queue_controller import QueueController

class QueueManager(QWidget):
    def __init__(self, controller: QueueController):
        super().__init__()
        self.setWindowTitle("Queue Manager")
        self.setGeometry(100, 60, 1100, 700)
        self.setStyleSheet(self.get_styles())

        self.controller = controller
        self.controller.queue_updated.connect(self.refresh_queue)
        self.controller.selected_updated.connect(self.refresh_selected)

        # Layout
        main_layout = QHBoxLayout()
        
        # Queue Box
        self.queue_box = QGroupBox("Queue")
        self.queue_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.queue_box.setObjectName("queueBox")
        queue_layout = QVBoxLayout()
        self.queue_list = QListWidget()
        self.queue_list.setObjectName("queueList")
        self.queue_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        queue_layout.addWidget(self.queue_list)
        self.queue_box.setLayout(queue_layout)


        # Selected Players Box
        self.selected_box = QGroupBox("Up Next")
        self.selected_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_box.setObjectName("selectedBox")
        selected_layout = QVBoxLayout()

        self.selected_list = QListWidget()
        self.selected_list.setObjectName("selectedList")
        self.selected_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        selected_layout.addWidget(self.selected_list)
        self.selected_box.setLayout(selected_layout)
        
        main_layout.addWidget(self.queue_box)
        main_layout.addWidget(self.selected_box)
        self.setLayout(main_layout)


    def add_to_list(self, list_widget, name, tier, games, move_callback):
        """Add user to a list (queue or selected)."""
        item_frame = QFrame()
        item_layout = QHBoxLayout()
        item_frame.setLayout(item_layout)
        
        name_label = QLabel(name)
        name_label.setObjectName("nameLabel")
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        details_label = QLabel(f"Tier {tier} | Queued: {games}")
        details_label.setObjectName("detailsLabel")

        move_button = QPushButton("⮞" if list_widget == self.queue_list else "⮜")
        move_button.setObjectName("moveButton")
        move_button.setToolTip("Move to selected" if list_widget == self.queue_list else "Move back to queue")
        move_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        move_button.clicked.connect(lambda: move_callback(name))

        remove_button = QPushButton("X")
        remove_button.setToolTip("Remove from list")
        remove_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        remove_button.clicked.connect(lambda: self.remove_from_selected(name))

        item_layout.addWidget(name_label)
        item_layout.addWidget(details_label)
        item_layout.addWidget(move_button)

        if list_widget == self.selected_list:
            item_layout.addWidget(remove_button)

        list_item = QListWidgetItem()
        list_item.setSizeHint(item_frame.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, item_frame)


    def refresh_queue(self, queue):
        """Clear and update queue list in UI."""
        self.queue_list.clear()
        for name, tier, games in queue:
            self.add_to_list(self.queue_list, name, tier, games, self.move_to_selected)

    def refresh_selected(self, selected):
        """Clear and update selected list in UI."""
        self.selected_list.clear()
        for name, tier, games in selected:
            self.add_to_list(self.selected_list, name, tier, games, self.move_back_to_queue)

    def move_to_selected(self, name):
        """Move user from queue to selected."""
        user = next((user for user in self.controller.queue if user[0] == name), None)
        if user:
            self.controller.queue.remove(user)
            self.controller.selected.append(user)
            self.controller.update_queue(self.controller.queue)
            self.controller.update_selected(self.controller.selected)

    def move_back_to_queue(self, name):
        """Move user back from selected to queue."""
        user = next((user for user in self.controller.selected if user[0] == name), None)
        if user:
            self.controller.selected.remove(user)
            self.controller.queue.append(user)
            self.controller.queue.sort(key=lambda x: (x[2], -x[1]))
            self.controller.update_queue(self.controller.queue)
            self.controller.update_selected(self.controller.selected)

    def remove_from_selected(self, name):
        """Remove user from selected and increase their queue count."""
        user = next((user for user in self.controller.selected if user[0] == name), None)
        if user:
            self.controller.selected.remove(user)
            self.controller.update_selected(self.controller.selected)
            self.controller.increase_queue_count(name)



    def get_styles(self):
        return """
            QWidget {
                background-color: #18181b; 
                color: #E9E9E9;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 14px;
            }

            QGroupBox {
                background: #292b2f; 
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                border: 2px solid #3a3a3c; 
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #E9E9E9; 
            }

            QListWidget {
                background: #40444b; 
                border-radius: 6px;
                padding: 10px;
                margin-top: 10px;
                color: #E9E9E9; 
                border: none;
            }

            QFrame#queueItem, QFrame#selectedItem {
                border-radius: 6px;
                border: 1px solid #3a3a3c; 
            }

            QLabel#nameLabel {
                font-weight: bold;
                color: #FFFFFF; 
            }

            QLabel#detailsLabel {
                color: #939393;
                font-size: 14px;
                text-align: right;
            }

            QPushButton {
                background: #5865f2;
                color: #E9E9E9; 
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 16px;
            }

            QPushButton#mooveButton{
                margin-left: 15px;
            }

            QPushButton:hover {
                background: #4752c4;
            }

            QPushButton:pressed {
                background: #3b43a1; 
            }

            QPushButton:focus {
                outline: none;
                border: 2px solid #5865f2;
            }
        """