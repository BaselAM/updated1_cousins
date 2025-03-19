from shared_imports import *
from translator import Translator
from themes import *

# Add these imports if they're not already present
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon
from pathlib import Path


class HeaderWidget(QWidget):
    def __init__(self, translator, home_function=None):
        super().__init__()
        self.translator = translator
        self.home_function = home_function
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)

        # Left section with logo and home button
        left_section = QHBoxLayout()
        left_section.setSpacing(12)

        # Add application logo/icon
        self.logo_label = QLabel()
        logo_path = Path("resources/car-icon.jpg")
        if logo_path.exists():
            logo_pixmap = QPixmap(str(logo_path)).scaled(32, 32, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation)
            self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setFixedSize(32, 32)
        left_section.addWidget(self.logo_label)

        # Add home button with custom icon - CHECK FOR THE NEW DOWNLOADED ICON FIRST
        self.home_button = QPushButton()

        # Try these paths in order
        home_icon_paths = [
            Path("resources/blue_home_icon.png"),
            Path("resources/home_icon.png"),
            Path("resources/home.jpg")
        ]

        icon_set = False
        for icon_path in home_icon_paths:
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.home_button.setIcon(icon)
                self.home_button.setIconSize(QSize(24, 24))
                print(f"Using home icon from: {icon_path}")
                icon_set = True
                break

        if not icon_set:
            self.home_button.setText("🏠")
            print("No home icon found! Using fallback emoji.")

        self.home_button.setFixedSize(40, 40)
        self.home_button.setToolTip(self.translator.t('home_button_tooltip'))
        self.home_button.setCursor(Qt.PointingHandCursor)

        if self.home_function:
            self.home_button.clicked.connect(self.home_function)

        left_section.addWidget(self.home_button)
        left_section.addStretch()

        # Create title label with elegant font
        self.title_label = QLabel(self.translator.t('header_title'))
        title_font = QFont("Segoe UI", 16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        # Add spacer to center the title
        layout.addLayout(left_section)
        layout.addWidget(self.title_label, 1, Qt.AlignCenter)
        layout.addStretch()

    def apply_theme(self):
        header_bg = get_color('header')
        text_color = get_color('text')
        accent_color = get_color('highlight')

        self.setStyleSheet(f"""
            HeaderWidget {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                         stop:0 {header_bg}, stop:1 {QColor(header_bg).darker(105).name()});
                border-bottom: 1px solid {get_color('border')};
            }}
            QLabel {{
                color: {text_color};
            }}
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 20px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {QColor(accent_color).lighter(150).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(accent_color).lighter(130).name()};
            }}
        """)

    def update_translations(self):
        """Update text when language changes"""
        self.title_label.setText(self.translator.t('header_title'))
        self.home_button.setToolTip(self.translator.t('home_button_tooltip'))

class FooterWidget(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.update_translations()

    def apply_theme(self):
        self.setStyleSheet(f"""
            background-color: {get_color('footer')};
            border-top: 2px solid {get_color('border')};
        """)
        self.label.setStyleSheet(f"""
            color: {get_color('text')};
            font-size: 14px;
        """)

    def update_translations(self):
        # Use self.translator to update the footer text
        self.label.setText(self.translator.t('footer_content'))


class CopyrightWidget(QLabel):
    def __init__(self, translator):
        super().__init__(translator.t('copyright'))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            "color: rgba(255,255,255,0.6); font-size: 14px; margin: 20px 0 10px 0;")
