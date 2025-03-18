from shared_imports import *
from translator import Translator
from themes import *


class HeaderWidget(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.update_translations()

    def apply_theme(self):
        self.setStyleSheet(f"""
            background-color: {get_color('header')};
            border-bottom: 2px solid {get_color('border')};
        """)
        self.title.setStyleSheet(f"""
            color: {get_color('text')};
            font-size: 24px;
            font-weight: bold;
        """)
    def update_translations(self):
        # Use self.translator to update the title text
        self.title.setText(self.translator.t('header_title'))


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
