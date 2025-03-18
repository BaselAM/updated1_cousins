import sys
import os
import logging
from pathlib import Path
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, \
    QMessageBox
from widgets.statistics import *
from widgets.search import *
from widgets.content import *
from widgets.sidebar import *
from widgets.layout import *
from widgets.help import *
from widgets.settings import *
from shared_imports import *
from translator import Translator
from database.settings_db import SettingsDB
from database.car_parts_db import CarPartsDB
from themes import set_theme, get_color
from widgets.products import ProductsWidget


class GUI(QMainWindow):
    language_changed = pyqtSignal()
    PANEL_SPACING = 10
    SIDEBAR_WIDTH = 200

    def __init__(self):
        super().__init__()
        self.settings_db = SettingsDB()
        self.parts_db = CarPartsDB()

        # Load theme first
        saved_theme = self.settings_db.get_setting('theme', 'classic')
        set_theme(saved_theme)

        # Initialize language and direction
        self.current_language = self.settings_db.get_setting('language', 'en')
        self.rtl_enabled = self.settings_db.get_rtl_setting()
        self.translator = Translator(self.current_language)

        self.preload_views()
        self.setup_window_properties()
        self.setup_ui()
        self.apply_theme()  # Apply theme after UI setup

        # Set initial layout direction
        self._apply_layout_direction_initially()

    def apply_theme(self):
        """Apply current theme to main window"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {get_color('background')};
                {"padding-right" if self.rtl_enabled else "padding-left"}: {self.SIDEBAR_WIDTH}px;
            }}
            QWidget {{
                color: {get_color('text')};
                font-family: 'Segoe UI', sans-serif;
            }}
        """)

    def apply_theme_to_all(self):
        """Force theme refresh on all components"""
        self.apply_theme()
        for widget in self.findChildren(QWidget):
            if hasattr(widget, 'apply_theme'):
                widget.apply_theme()

    def setup_window_properties(self):
        """Initialize window properties that don't depend on theme"""
        self.setWindowTitle(self.translator.t('window_title'))
        self.setGeometry(500, 100, 1000, 700)
        icon_path = Path(__file__).parent / "resources/window_icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def preload_views(self):
        # Pre-create all view widgets
        self.products_widget = ProductsWidget(self.translator, self.parts_db)
        self.statistics_widget = StatisticsWidget(self.translator)
        self.settings_widget = SettingsWidget(self.translator, self.update_language, self)
        self.help_widget = HelpWidget(self.translator)

    def setup_ui(self):
        self.header = HeaderWidget(self.translator)
        self.search_bar = SearchBarWidget(self.translator, self.parts_db)
        # Connect search signal
        self.search_bar.search_input.returnPressed.connect(self.on_search_entered)

        self.footer = FooterWidget(self.translator)
        copyright_widget = CopyrightWidget(self.translator)
        self.content = ContentWidget()
        self.sidebar = SidebarWidget(self.translator, {
            'products_button': self.show_products,
            'statistics_button': self.show_statistics,
            'settings_button': self.show_settings,
            'help_button': self.show_help,
            'exit_button': self.exit_app
        })

        content_area = QWidget()
        ca_layout = QHBoxLayout(content_area)
        ca_layout.setContentsMargins(self.PANEL_SPACING, self.PANEL_SPACING,
                                     self.PANEL_SPACING, self.PANEL_SPACING)
        ca_layout.setSpacing(self.PANEL_SPACING)
        ca_layout.addWidget(self.sidebar)
        ca_layout.addWidget(self.content, 1)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(content_area, 1)
        main_layout.addWidget(self.footer)
        main_layout.addWidget(copyright_widget)
        self.setCentralWidget(main_widget)

        self.content.add_view(self.products_widget)
        self.content.add_view(self.statistics_widget)
        self.content.add_view(self.settings_widget)
        self.content.add_view(self.help_widget)
        self.show_products()

    def on_search_entered(self):
        search_text = self.search_bar.search_input.text().strip()
        if search_text:
            self.show_products()  # Switch to the products view
            self.products_widget.highlight_product(search_text)

    def show_products(self):
        self.content.stack.setCurrentWidget(self.products_widget)

    def show_statistics(self):
        self.content.stack.setCurrentWidget(self.statistics_widget)

    def show_settings(self):
        self.content.stack.setCurrentWidget(self.settings_widget)

    def show_help(self):
        self.content.stack.setCurrentWidget(self.help_widget)

    def exit_app(self):
        self.close()

    def update_language(self, new_lang: str):
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            # Save settings
            is_rtl = (new_lang == 'he')
            self.settings_db.save_setting('rtl', str(is_rtl).lower())
            self.settings_db.save_setting('language', new_lang)

            # Update state
            self.current_language = new_lang
            self.rtl_enabled = is_rtl
            self.translator.set_language(new_lang)

            # Apply direction changes
            direction = Qt.RightToLeft if is_rtl else Qt.LeftToRight
            QApplication.setLayoutDirection(direction)
            self._apply_layout_direction_recursive(self, direction)

            # Refresh theme to update direction-dependent padding
            self.apply_theme_to_all()
            self._full_ui_refresh()

        except Exception as e:
            logging.error(f"Language update error: {str(e)}")
            QMessageBox.critical(self, "Error", self.translator.t('settings_save_error'))
        finally:
            QApplication.restoreOverrideCursor()

    def _apply_layout_direction_recursive(self, widget, direction):
        """Recursively set layout direction for all child widgets"""
        widget.setLayoutDirection(direction)
        for child in widget.findChildren(QWidget):
            self._apply_layout_direction_recursive(child, direction)

    # This method can be removed as it's redundant with _apply_layout_direction_recursive
    # def update_layout_direction(self, direction):
    #     """Recursively set layout direction for all child widgets."""
    #     for widget in self.findChildren(QWidget):
    #         widget.setLayoutDirection(direction)

    def t(self, key):
        return TRANSLATIONS.get(key, {}).get(self.current_language, key)

    def closeEvent(self, event):
        try:
            self._is_closing = True

            # Close any other resources if necessary (e.g., database connections)
            self.search_bar.deleteLater()
            self.content.deleteLater()
            self.sidebar.deleteLater()

            # Close database connections
            self.parts_db.close_connection()
            self.settings_db.close()

            # Process any pending events
            QApplication.sendPostedEvents()

            import gc
            gc.collect()  # Force garbage collection to clean up memory

            event.accept()

        except Exception as e:
            print(f"Shutdown error: {str(e)}")
            sys.exit(1)

    def _full_ui_refresh(self):
        """Refresh all UI components after language change"""
        self.sidebar.update_translations()
        self.header.update_translations()
        self.search_bar.update_translations()
        self.footer.update_translations()
        self.settings_widget.update_translations()
        self.products_widget.update_translations()
        self.statistics_widget.update_translations()
        self.help_widget.update_translations()

        # Force layout recalculation
        self.updateGeometry()
        QApplication.processEvents()

    def _apply_layout_direction_initially(self):
        """Set initial layout direction from settings"""
        direction = Qt.RightToLeft if self.rtl_enabled else Qt.LeftToRight
        QApplication.setLayoutDirection(direction)
        self.setLayoutDirection(direction)