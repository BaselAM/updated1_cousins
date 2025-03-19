from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from themes import get_color, set_theme
from translator import Translator

class LoginWidget(QWidget):
    # Signal emitted when the login is successful.
    login_successful = pyqtSignal(str)

    def __init__(self, translator=None, parent=None):
        super().__init__(parent)
        self.translator = translator if translator is not None else Translator('en')
        self.setWindowTitle(self.translator.t('window_title'))
        self.resize(400, 300)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Elegant title label matching GUI header styling.
        title_label = QLabel("Abu Mukh Car Parts")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 28, QFont.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Form layout for entering credentials.
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Password:", self.password_edit)
        main_layout.addLayout(form_layout)

        # Login button.
        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(140, 45)
        main_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # Status label for feedback.
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()

        self.login_button.clicked.connect(self.login)

    def apply_theme(self):
        # Apply a stylesheet that matches your main GUI.
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {get_color('background')};
                color: {get_color('text')};
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel {{
                font-size: 16px;
            }}
            QLineEdit {{
                background-color: {get_color('input_bg')};
                border: 2px solid {get_color('border')};
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 16px;
            }}
            QPushButton {{
                background-color: {get_color('button')};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                color: {get_color('text')};
            }}
            QPushButton:hover {{
                background-color: {get_color('button_hover')};
            }}
            QPushButton:pressed {{
                background-color: {get_color('button_pressed')};
            }}
        """)

    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        # Check against the hard-coded default credentials.
        if username == "abumukh" and password == "123":
            self.status_label.setText("Login successful!")
            self.login_successful.emit(username)  # Pass the username
        else:
            self.status_label.setText("Invalid credentials!")
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
