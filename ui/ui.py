from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QGroupBox, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
import sys

class QueueManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queue Manager")
        self.setGeometry(100, 60, 1100, 700)
        self.setStyleSheet(self.get_styles())

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
        
        # Add to main layout
        main_layout.addWidget(self.queue_box)
        main_layout.addWidget(self.selected_box)
        self.setLayout(main_layout)

        # Sample data
        self.add_to_queue("Viewer1", "Tier 1", 0)
        self.add_to_queue("Viewer2", "Tier 0", 1)
        self.add_to_selected("Viewer3")

    def add_to_queue(self, name, tier, games):
        item_frame = QFrame()
        item_layout = QHBoxLayout()
        item_frame.setLayout(item_layout)
        item_frame.setObjectName("queueItem")
        
        name_label = QLabel(name)
        name_label.setObjectName("nameLabel")
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        details_label = QLabel(f"{tier} | Queued: {games}")
        details_label.setObjectName("detailsLabel")
        
        move_button = QPushButton("⮞")
        move_button.setObjectName("mooveButton")
        move_button.setToolTip("Move to selected")
        move_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        
        item_layout.addWidget(name_label)
        item_layout.addWidget(details_label)
        item_layout.addWidget(move_button)
        
        list_item = QListWidgetItem()
        list_item.setSizeHint(item_frame.sizeHint())
        self.queue_list.addItem(list_item)
        self.queue_list.setItemWidget(list_item, item_frame)

    def add_to_selected(self, name):
        item_frame = QFrame()
        item_layout = QHBoxLayout()
        item_frame.setLayout(item_layout)
        item_frame.setObjectName("selectedItem")
        
        name_label = QLabel(name)
        name_label.setObjectName("nameLabel")
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        back_button = QPushButton("⮜")
        back_button.setToolTip("Move back to queue")
        back_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        
        remove_button = QPushButton("X")
        remove_button.setToolTip("Remove from list")
        remove_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        
        item_layout.addWidget(name_label)
        item_layout.addWidget(back_button)
        item_layout.addWidget(remove_button)
        
        list_item = QListWidgetItem()
        list_item.setSizeHint(item_frame.sizeHint())
        self.selected_list.addItem(list_item)
        self.selected_list.setItemWidget(list_item, item_frame)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueueManager()
    window.show()
    sys.exit(app.exec())
