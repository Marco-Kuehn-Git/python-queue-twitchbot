from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QFrame, QSizePolicy
)
from PyQt6.QtGui import QIcon, QAction
import functools, os

class OptionsWindow(QDialog):
    def __init__(self, config, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setFixedSize(700, 500)

        self.config = config
        self.controller = controller

        self._input_width = 400
        self._header_sep_spacing = 10
        dir = os.path.dirname(__file__)
        self.icon_show = QIcon(os.path.join(dir, "assets/visibility_on.svg"))
        self.icon_hide = QIcon(os.path.join(dir, "assets/visibility_off.svg"))

        # Map display label to actual config attribute names
        self.twitch_cred_labels = ["Oauth token", "Refresh token", "Client ID", "Client Secret"]
        self.twitch_config_map = {
            "Oauth token": "twitch_oauth_token",
            "Refresh token": "twitch_refresh_token",
            "Client ID": "twitch_client_id",
            "Client Secret": "twitch_client_secret"
        }

        self._setup_ui()
        self.setStyleSheet(self._get_styles())

    def _setup_ui(self):
        """
        Initialize the UI
        """
        main_layout = QVBoxLayout()

        # Authorization buttons
        auth_layout = QHBoxLayout()
        self.twitch_button = QPushButton("Authorize Twitch")
        self.twitch_button.setToolTip("Click to authorize Twitch")
        self.twitch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.twitch_button.clicked.connect(self.authorize_twitch)
        auth_layout.addWidget(self.twitch_button, 1)
        main_layout.addLayout(auth_layout)

        # General options header and separator
        main_layout.addSpacing(self._header_sep_spacing)
        general_label = QLabel("General options")
        general_label.setObjectName("headerLabel")
        main_layout.addWidget(general_label)
        sep_general = QFrame()
        sep_general.setObjectName("sepGeneral")
        sep_general.setFrameShape(QFrame.Shape.HLine)
        sep_general.setLineWidth(2)
        main_layout.addWidget(sep_general)

        # Twitch channel input
        twitch_channel_layout = QHBoxLayout()
        twitch_channel_label = QLabel("Twitch Channel:")
        self.twitch_channel_input = QLineEdit()
        self.twitch_channel_input.setText(self.config.twitch_channel or "")
        self.twitch_channel_input.setFixedWidth(300)
        twitch_channel_layout.addWidget(twitch_channel_label)
        twitch_channel_layout.addStretch()
        twitch_channel_layout.addWidget(self.twitch_channel_input)
        main_layout.addLayout(twitch_channel_layout)

        # Sort options dropdown
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort option:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Times queued, Sub Tier",
            "Sub tier",
            "Times queued",
            "Time joined"
        ])
        self.sort_combo.setFixedWidth(300)
        self.sort_combo.setCurrentIndex(self.config.sorting_option or 0)
        sort_layout.addWidget(sort_label)
        sort_layout.addStretch()
        sort_layout.addWidget(self.sort_combo)
        main_layout.addLayout(sort_layout)

        # Twitch credentials header and separator
        main_layout.addSpacing(self._header_sep_spacing)
        creds_label = QLabel("Twitch credentials")
        creds_label.setObjectName("headerLabel")
        main_layout.addWidget(creds_label)
        sep_creds = QFrame()
        sep_creds.setObjectName("sepCreds")
        sep_creds.setFrameShape(QFrame.Shape.HLine)
        sep_creds.setLineWidth(2)
        main_layout.addWidget(sep_creds)

        # Credentials inputs
        self.credentials = {}

        for label_text in self.twitch_cred_labels:
            row = QHBoxLayout()
            label = QLabel(f"{label_text}:")
            edit = QLineEdit()
            edit.setEchoMode(QLineEdit.EchoMode.Password)
            edit.setFixedWidth(self._input_width)

            # Pull value from config
            config_attr = self.twitch_config_map.get(label_text)
            if config_attr and hasattr(self.config, config_attr):
                edit.setText(getattr(self.config, config_attr) or "")

            # Add eye icon action
            action = edit.addAction(self.icon_show, QLineEdit.ActionPosition.TrailingPosition)
            action.setToolTip("Show / hide")
            action.triggered.connect(functools.partial(self._toggle_field, edit, action))

            row.addWidget(label)
            row.addStretch()
            row.addWidget(edit)
            main_layout.addLayout(row)
            self.credentials[label_text] = edit

        # Spacer
        main_layout.addStretch()

        # Save and Back buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.save_button = QPushButton("Save")
        self.close_button = QPushButton("Close")
        self.save_button.clicked.connect(lambda: self.save())
        self.close_button.clicked.connect(self.close)
        bottom_layout.addWidget(self.close_button)
        bottom_layout.addWidget(self.save_button)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def _toggle_field(self, edit: QLineEdit, action: QAction):
        """Flip password visibility and swap the eye icon."""
        if edit.echoMode() == QLineEdit.EchoMode.Password:
            edit.setEchoMode(QLineEdit.EchoMode.Normal)
            action.setIcon(self.icon_hide)
        else:
            edit.setEchoMode(QLineEdit.EchoMode.Password)
            action.setIcon(self.icon_show)

    def save(self):
        """Updated the config class with new values and saves them to the config file"""
        # Update Twitch channel
        self.config.twitch_channel = self.twitch_channel_input.text()
        self.config.sorting_option = self.sort_combo.currentIndex()

        # Update twitch credentials
        for label, line_edit in self.credentials.items():
            text = line_edit.text()
            config_attr = self.twitch_config_map.get(label)
            if config_attr:
                setattr(self.config, config_attr, text)

        # Resort queue and refresh UI
        self.controller.queue_manager.sort_queue()
        self.controller.update_ui()
        self.config.save_config()

    def authorize_twitch(self):
        """
        Initiate Twitch authorization.
        """
        if not self.validate_required_fields():
            print("Missing required fields. Please fill them in before authorizing.")
            return

        import threading
        from bot.twitch_auth import TwitchAuthHandler

        def auth_thread():
            auth_handler = TwitchAuthHandler(self.config)
            auth_handler.start_auth()

            # Reload config values
            self.config = self.config.__class__()
            self.update_fields()

        threading.Thread(target=auth_thread, daemon=True).start()
    
    def validate_required_fields(self):
        """
        Check if required fields for Twitch authorization are set.
        Highlights missing fields with red border.
        Returns True if all required fields are valid, else False.
        """
        valid = True

        # Fields to check
        required_fields = {
            "Client ID": self.credentials["Client ID"],
            "Client Secret": self.credentials["Client Secret"],
            "Twitch Channel": self.twitch_channel_input
        }

        for label, field in required_fields.items():
            if not field.text().strip():
                # Mark field as invalid
                field.setStyleSheet("border: 2px solid red;")
                valid = False
            else:
                # Reset style if filled
                field.setStyleSheet("")

        return valid

    def update_fields(self):
        """
        Update UI fields to match the current config values.
        """
        # Update Twitch Channel
        self.twitch_channel_input.setText(self.config.twitch_channel or "")

        # Update Sort Option
        print("Current index before: ", self.sort_combo.currentIndex())
        print("Saved index: ", self.config.sorting_option)
        self.sort_combo.setCurrentIndex(self.config.sorting_option or 0)
        print("Current index after: ", self.sort_combo.currentIndex())

        # Update Credentials
        for label_text, line_edit in self.credentials.items():
            config_attr = self.twitch_config_map.get(label_text)
            if config_attr and hasattr(self.config, config_attr):
                line_edit.setText(getattr(self.config, config_attr) or "")

    def _get_styles(self):
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
            QLabel {
                font-size: 16px;
                color: #E9E9E9;
            }
            QLabel#headerLabel {
                font-weight: bold;
            } 
            QFrame#sepGeneral, QFrame#sepCreds {
                background-color: #6272a4;
                max-height: 4px;
                border: none;
            }
            QPushButton {
                background: #5865f2;
                height: 40px;
                width: 100px;
                color: #E9E9E9;
                border: none;
                border-radius: 4px;
                font-size: 16px;
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
            QComboBox {
                background: #40444b;
                color: #E9E9E9;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit {
                background: #40444b;
                color: #E9E9E9;
                border: 1px solid #3a3a3c;
                border-radius: 4px;
                padding: 5px;
            }
            """