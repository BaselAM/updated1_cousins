from shared_imports import *
from translator import Translator
from database.car_parts_db import CarPartsDB
from themes import get_color  # Add theme import


class SearchBarWidget(QWidget):
    def __init__(self, translator, product_db=None):
        super().__init__()
        self.translator = translator
        self.product_db = product_db
        self.setup_ui()
        self.notification_count = 0
        self.init_clock()
        self.apply_theme()  # Apply theme on initialization

    def setup_ui(self):
        self.setFixedHeight(70)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.translator.t('search_placeholder'))
        self.search_input.setFixedHeight(40)
        self.search_input.setMinimumWidth(400)

        # Search icon (theme-colored)
        search_icon_path = str(SCRIPT_DIR / 'resources' / "search_icon.png")
        self.search_icon = QIcon(search_icon_path)
        search_action = QAction(self.search_icon, "", self.search_input)
        self.search_input.addAction(search_action, QLineEdit.LeadingPosition)

        layout.addWidget(self.search_input, 1)

        # Clock label
        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.clock_label)

        # Notification system
        self.notification_btn = QPushButton()
        self.notification_btn.setIconSize(QSize(28, 28))

        # Load base notification icon
        icon_path = str(SCRIPT_DIR / 'resources' / "danger.png")
        self.base_notification_icon = QIcon(icon_path)

        # Notification badge
        self.notification_badge = QLabel("0")
        self.notification_badge.setAlignment(Qt.AlignCenter)
        self.notification_badge.setFixedSize(18, 18)

        # Create overlay container
        notification_container = QWidget()
        notification_layout = QHBoxLayout(notification_container)
        notification_layout.setContentsMargins(0, 0, 0, 0)
        notification_layout.addWidget(self.notification_btn)

        # Add badge as overlay
        self.notification_badge.setParent(self.notification_btn)
        self.notification_badge.move(12, 2)
        self.notification_badge.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout.addWidget(notification_container)

        # Autocomplete setup
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model, self.search_input)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.search_input.setCompleter(self.completer)
        self.search_input.textChanged.connect(self.on_text_changed)

    def apply_theme(self):
        """Apply current theme to all elements"""
        # Main widget styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {get_color('header')};
                border-bottom: 2px solid {get_color('border')};
            }}
        """)

        # Search input styling
        search_style = f"""
            QLineEdit {{
                background-color: {get_color('input_bg')};
                border: 2px solid {get_color('border')};
                border-radius: 18px;
                color: {get_color('text')};
                padding: 4px 25px 4px 45px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {get_color('button')};
                background-color: {get_color('input_bg')};
            }}
        """
        self.search_input.setStyleSheet(search_style)

        # Color the search icon
        search_pixmap = self.search_icon.pixmap(24, 24)
        painter = QPainter(search_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(search_pixmap.rect(), QColor(get_color('text')))
        painter.end()
        self.search_input.findChild(QAction).setIcon(QIcon(search_pixmap))

        # Notification button styling
        notification_icon = self.base_notification_icon.pixmap(28, 28)
        painter = QPainter(notification_icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(notification_icon.rect(), QColor(get_color('text')))
        painter.end()

        self.notification_btn.setIcon(QIcon(notification_icon))
        self.notification_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 5px;
                border-radius: 16px;
            }}
            QPushButton:hover {{
                background-color: {get_color('secondary')};
                border: 1px solid {get_color('border')};
            }}
        """)

        # Notification badge styling
        self.notification_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {get_color('warning')};
                color: {get_color('text')};
                border-radius: 9px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)

        # Clock label styling
        self.clock_label.setStyleSheet(f"""
            color: {get_color('text')};
            font-size: 14px;
            font-family: 'Segoe UI';
        """)

        # Completer styling
        self.completer.popup().setStyleSheet(f"""
            QListView {{
                background-color: {get_color('background')};
                color: {get_color('text')};
                border: 1px solid {get_color('border')};
                border-radius: 4px;
            }}
            QListView::item {{
                padding: 6px 8px;
                border-bottom: 1px solid {get_color('border')};
            }}
            QListView::item:selected {{
                background-color: {get_color('button')};
                color: {get_color('text')};
            }}
        """)

    def update_clock(self):
        now = datetime.now()
        if self.translator.language == 'he':
            month_english = now.strftime("%B")
            hebrew_month = TRANSLATIONS.get("months", {}).get(month_english,
                                                              month_english)
            formatted = now.strftime("%H:%M") + " | " + f"{now.day} {hebrew_month}"
        else:
            formatted = now.strftime("%I:%M %p | %b %d")
        self.clock_label.setText(formatted)

    def update_translations(self):
        self.search_input.setPlaceholderText(self.translator.t('search_placeholder'))
        self.update_clock()  # Refresh date format on language change
    def show_notifications(self):
        print("Show notifications dialog")  # Implement your notification UI here

    def update_notification_count(self, count):
        self.notification_count = count
        self.notification_badge.setText(str(count))
        self.notification_badge.setVisible(count > 0)

    def init_clock(self):
        self.update_clock()
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)


    def on_text_changed(self, text):
        """Update autocomplete suggestions based on the current text."""
        # If no product database is provided, do nothing
        if not self.product_db:
            return

        # If the text is empty, clear the model
        if not text:
            self.completer_model.setStringList([])
            return

        try:
            # Fetch all products from the database
            all_products = self.product_db.get_all_parts()
            # Assuming the product name is at index 4 (as used in ProductsWidget)
            suggestions = [
                prod[4] for prod in all_products
                if prod[4] and prod[4].lower().startswith(text.lower())
            ]
            # Limit to five suggestions
            suggestions = suggestions[:5]
        except Exception as e:
            print("Error fetching suggestions:", e)
            suggestions = []

        self.completer_model.setStringList(suggestions)

