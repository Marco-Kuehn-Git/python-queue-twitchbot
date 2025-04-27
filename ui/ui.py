from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, 
    QHBoxLayout, QListWidgetItem, QGroupBox, QFrame, QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter
from .controller import QueueController

from ui.toggleButton import ToggleSwitch
from ui.options_ui import OptionsWindow

class UI(QWidget):
    def __init__(self, controller: QueueController, config):
        super().__init__()
        self.setWindowTitle("Queue Manager")
        self.setGeometry(100, 60, 1100, 700)

        self.config = config
        self.controller = controller
        self.controller.queue_updated.connect(self.refresh_queue)
        self.controller.selected_updated.connect(self.refresh_selected)
        self.controller.connection_status.connect(self.update_status_icon)
        self.controller.status_message.connect(self.update_status_text)

        self.__setup_ui()
        self.setStyleSheet(self.get_styles())

    def __setup_ui(self):
        """
        Initialize the UI
        """
        # Set up status area and twitch authorization button
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Disconnected")
        self.status_label.setObjectName("statusLabel")

        self.status_icon = QLabel()
        self.status_icon.setFixedSize(20, 20)
        self.update_status_icon(False)

        # Set up the option button to open option window
        self.options_button = QPushButton("⚙")
        self.options_button.setToolTip("Options")
        self.options_button.setFixedSize(40,40)
        self.options_button.clicked.connect(self.open_options_window)

        # Set up the ui above the lists
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.options_button)

        # Toggle layout for closing the queue
        toggle_layout = QHBoxLayout()
        toggle_label = QLabel("Close queue: ")
        toggle_label.setObjectName("toggleLabel")
        toggle_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Create the toggle switch for closing the queue
        queue_toggle_button = ToggleSwitch()
        queue_toggle_button.toggled.connect(self.controller.set_queue_closed)
        queue_toggle_button.setFixedSize(
            queue_toggle_button.sizeHint().width() * 2,
            queue_toggle_button.sizeHint().height()
        )
        toggle_layout.addWidget(toggle_label)
        toggle_layout.addWidget(queue_toggle_button)
        toggle_layout.addStretch()

        # Main layout including status and the two lists (queue and selected)
        main_layout = QVBoxLayout()
        main_layout.addLayout(status_layout)
        main_layout.addLayout(toggle_layout)

        queue_selected_layout = QHBoxLayout()

        # Queue group box
        self.queue_box = QGroupBox("Queue")
        self.queue_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.queue_box.setObjectName("queueBox")
        queue_layout = QVBoxLayout()
        self.queue_list = QListWidget()
        self.queue_list.setObjectName("queueList")
        self.queue_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        queue_layout.addWidget(self.queue_list)
        self.queue_box.setLayout(queue_layout)

        # Selected group box
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

    def add_to_list(self, list_widget, name, tier, games, move_callback):
        """
        Add a user item to the provided list widget with a move button.
        For the selected list, also add two remove buttons.
        """
        item_frame = QFrame()
        item_layout = QHBoxLayout()
        item_frame.setLayout(item_layout)
        
        name_label = QLabel(name)
        name_label.setObjectName("nameLabel")
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        item_layout.addWidget(name_label)

        if list_widget == self.queue_list:
            details_label = QLabel(f"Tier {tier} | Queued: {games}")
            details_label.setObjectName("detailsLabel")
            item_layout.addWidget(details_label)

        move_button = QPushButton("⮞" if list_widget == self.queue_list else "⮜")
        move_button.setObjectName("moveButton")
        move_button.setToolTip("Move to selected" if list_widget == self.queue_list else "Move back to queue")
        move_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        move_button.clicked.connect(lambda: move_callback(name))
        item_layout.addWidget(move_button)

        # For selected list items, add two remove buttons.
        if list_widget == self.selected_list:
            # Remove without incrementing count
            remove_no_count_button = QPushButton("X")
            remove_no_count_button.setToolTip("Remove from list without increasing queued counter")
            remove_no_count_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            remove_no_count_button.clicked.connect(lambda: self.remove_from_selected_without_count(name))
            item_layout.addWidget(remove_no_count_button)

            # Remove and increase queued counter
            remove_button = QPushButton("✓")
            remove_button.setToolTip("Remove from list (increases queued count)")
            remove_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            remove_button.clicked.connect(lambda: self.remove_from_selected(name))
            item_layout.addWidget(remove_button)

        list_item = QListWidgetItem()
        list_item.setSizeHint(item_frame.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, item_frame)

    def update_status_icon(self, connected: bool):
        """
        Update the connection status icon and text based on the connection state.
        """
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

    def refresh_queue(self):
        """
        Clear and repopulate the queue list widget.
        """
        self.queue_list.clear()
        for name, tier, games, _ in self.controller.queue_manager.get_queue():
            self.add_to_list(self.queue_list, name, tier, games, self.move_to_selected)

    def refresh_selected(self):
        """
        Clear and repopulate the selected list widget.
        """
        self.selected_list.clear()
        for name, tier, games, _ in self.controller.queue_manager.get_selected():
            self.add_to_list(self.selected_list, name, tier, games, self.move_back_to_queue)

    def move_to_selected(self, name):
        """
        Move a user from the queue to the selected list.
        """
        if self.controller.queue_manager.move_to_selected(name):
            self.controller.update_ui()

    def move_back_to_queue(self, name):
        """
        Move a user from the selected list back to the queue.
        """
        if self.controller.queue_manager.move_back_to_queue(name):
            self.controller.update_ui()

    def remove_from_selected(self, name):
        """
        Remove a user from the selected list and increment their queued count.
        """
        if self.controller.queue_manager.remove_user(name):
            self.controller.increase_queue_count(name)
            self.controller.update_ui()
    
    def remove_from_selected_without_count(self, name):
        """
        Remove a user from the selected list without modifying the queued count.
        """
        if self.controller.queue_manager.remove_user(name):
            self.controller.update_ui()
    
    def update_status_text(self, message: str):
        """
        Update the status label text.
        """
        self.status_label.setText(message)

    def open_options_window(self):
        self.options_window = OptionsWindow(self.config)
        self.options_window.show()

    def get_styles(self):
        """
        Return the UI stylesheet.
        """
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
                height: 40px;
                width: 40px;
                color: #E9E9E9; 
                border: none;
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
