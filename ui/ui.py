from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, 
    QHBoxLayout, QListWidgetItem, QGroupBox, QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter
from .controller import QueueController

class UI(QWidget):
    def __init__(self, controller: QueueController):
        super().__init__()
        self.setWindowTitle("Queue Manager")
        self.setGeometry(100, 60, 1100, 700)
        self.setStyleSheet(self.get_styles())

        self.controller = controller
        self.controller.queue_updated.connect(self.refresh_queue)
        self.controller.selected_updated.connect(self.refresh_selected)
        self.controller.connection_status.connect(self.update_status_icon)

        # Status Indicator
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Disconnected")
        self.status_label.setObjectName("statusLabel")

        self.status_icon = QLabel()
        self.status_icon.setFixedSize(20, 20)
        self.update_status_icon(False)

        # Twitch auth button
        self.twitch_auth_button = QPushButton("Connect Twitch")
        self.twitch_auth_button.setToolTip("Click to authorize Twitch")
        self.twitch_auth_button.clicked.connect(self.authorize_twitch)

        # Youtube auth button
        self.youtube_auth_button = QPushButton("Connect YouTube")
        self.youtube_auth_button.setToolTip("Click to authorize Youtube")
        self.youtube_auth_button.clicked.connect(self.authorize_youtube)

        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.twitch_auth_button)
        status_layout.addWidget(self.youtube_auth_button)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(status_layout)

        # Queue & Selected Players Layout
        queue_selected_layout = QHBoxLayout()
        
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

        queue_selected_layout.addWidget(self.queue_box)
        queue_selected_layout.addWidget(self.selected_box)
        
        main_layout.addLayout(queue_selected_layout)
        self.setLayout(main_layout)


    # Add a user to one of the lists (queue or selected)
    def add_to_list(self, list_widget, name, tier, games, move_callback):
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

    # Updates the status to show if connected or disconnected
    def update_status_icon(self, connected: bool):
        color = QColor("#28a745") if connected else QColor("#dc3545")
        text = "Connected" if connected else "Disconnected"

        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawEllipse(0, 0, 18, 18)
        painter.end()

        self.status_icon.setPixmap(pixmap)
        self.status_label.setText(text)

    def authorize_twitch(self):
        import threading
        from bot.twitch_auth import TwitchAuthHandler

        def auth_thread():
            print("Starting Twitch authorization via UI button...")
            auth_handler = TwitchAuthHandler()
            auth_handler.start_auth() 

        threading.Thread(target=auth_thread, daemon=True).start()

    def authorize_youtube(self):
        return 0

    # Refresh queue list in ui
    def refresh_queue(self):
        self.queue_list.clear()
        for name, tier, games, _ in self.controller.queue_manager.get_queue():
            self.add_to_list(self.queue_list, name, tier, games, self.move_to_selected)

    # Refresh selected list in ui
    def refresh_selected(self):
        self.selected_list.clear()
        for name, tier, games, _ in self.controller.queue_manager.get_selected():
            self.add_to_list(self.selected_list, name, tier, games, self.move_back_to_queue)
    # Move user from queue to 'next up'
    def move_to_selected(self, name):
        if self.controller.queue_manager.move_to_selected(name):
            self.controller.update_ui()

    # Move user back to queue inserting them into the correct position
    def move_back_to_queue(self, name):
        if self.controller.queue_manager.move_back_to_queue(name):
            self.controller.update_ui()

    # Remove user from selected and increase their queue count
    def remove_from_selected(self, name):
        if self.controller.queue_manager.remove_user(name):
            self.controller.increase_queue_count(name)
            self.controller.update_ui()


    # Style for the ui
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