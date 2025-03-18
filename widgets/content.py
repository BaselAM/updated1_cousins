# content.py
from shared_imports import *
from translator import Translator
from themes import get_color  # Add theme import


class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.stack = QStackedLayout()
        self.setLayout(self.stack)
        self.apply_theme()  # Apply initial theme
        self.setup_margins()

    def setup_margins(self):
        """Set consistent spacing and margins"""
        self.stack.setContentsMargins(15, 15, 15, 15)
        self.stack.setSpacing(10)

    def apply_theme(self):
        """Apply current theme to content area"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {get_color('background')};
                border-radius: 8px;
                border: 1px solid {get_color('border')};
            }}
            QLabel {{
                color: {get_color('text')};
            }}
        """)

    def add_default_page(self):
        """Create default view with theme-aware styling"""
        default = QLabel("Central Content Area")
        default.setAlignment(Qt.AlignCenter)
        default.setStyleSheet(f"""
            font-size: 18px;
            color: {get_color('text')};
        """)
        self.stack.addWidget(default)

    def add_view(self, widget):
        """Add a view widget with theme propagation"""
        if self.stack.indexOf(widget) == -1:
            self.stack.addWidget(widget)

        # Apply theme to new widget if possible
        if hasattr(widget, 'apply_theme'):
            widget.apply_theme()

        self.stack.setCurrentWidget(widget)
        widget.show()
        QApplication.processEvents()

    def show_view(self, widget):
        """Show specific view with theme refresh"""
        self.stack.setCurrentWidget(widget)
        if hasattr(widget, 'apply_theme'):
            widget.apply_theme()