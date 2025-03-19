from shared_imports import *
from translator import Translator
from themes import set_theme, get_color, \
    THEMES  # Import THEMES to access theme names directly


class SettingsWidget(QWidget):
    def __init__(self, translator, on_save, gui, parent=None):
        super().__init__(parent)
        self.translator = translator
        self.gui = gui
        self.on_save_callback = on_save

        # Define theme mappings consistently
        self.theme_names = ["classic", "dark", "light"]

        # Use English display names instead of translation keys to avoid missing translations
        self.theme_display_names = ["Classic", "Dark", "Light"]

        self.setup_ui()
        self.load_initial_settings()
        self.apply_theme()

        # Store initial settings to revert if needed
        self.initial_settings = self.get_current_settings()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        scroll_layout.setSpacing(25)

        self.language_group = self._create_language_group(content)
        self.appearance_group = self._create_appearance_group(content)
        self.technical_group = self._create_technical_group(content)
        self.inventory_group = self._create_inventory_group(content)

        scroll_layout.addWidget(self.language_group)
        scroll_layout.addWidget(self.appearance_group)
        scroll_layout.addWidget(self.technical_group)
        scroll_layout.addWidget(self.inventory_group)
        scroll_layout.addStretch()

        content.setLayout(scroll_layout)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Buttons
        btn_box = QWidget()
        btn_box.setFixedHeight(60)
        btn_layout = QHBoxLayout(btn_box)
        btn_layout.setContentsMargins(0, 10, 0, 10)
        btn_layout.setSpacing(15)

        self.save_btn = QPushButton(self.translator.t('save'))
        self.cancel_btn = QPushButton(self.translator.t('cancel'))

        # Apply button styles after creation
        self.save_btn.setFixedSize(120, 40)  # Slightly wider
        self.cancel_btn.setFixedSize(120, 40)  # Slightly wider

        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.cancel_changes)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        main_layout.addWidget(btn_box)

    # The main issue is in how theme changes are applied and how the cancel button works
    # Here's a fixed version of the critical functions in settings.py:

    def save_settings(self):
        """Save all settings with validation and error handling"""
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            # Validate low stock threshold
            low_stock = self.low_stock_threshold_input.text().strip()
            if not low_stock.isdigit() or int(low_stock) < 0:
                low_stock = "10"
                self.low_stock_threshold_input.setText(low_stock)

            # Get current settings
            settings = {
                'theme': self.theme_names[self.theme_combo.currentIndex()],
                'language': self.language_combo.currentData(),
                'low_stock_threshold': low_stock,
                'default_currency': self.default_currency_combo.currentText().lower(),
                'auto_restock': str(self.auto_restock_checkbox.isChecked()),
                'backup_interval': str(self.db_backup_interval.currentIndex()),
                'measurement_units': str(self.units_combo.currentIndex())
            }

            # Save to database first
            for key, value in settings.items():
                self.gui.settings_db.save_setting(key, value)

            # Update initial settings to match saved values
            self.initial_settings = self.get_current_settings()

            # Apply language change via callback - wrap in try/except
            try:
                if settings['language'] != self.translator.language:
                    self.on_save_callback(settings['language'])
            except Exception as lang_error:
                print(f"Error applying language change: {str(lang_error)}")

            # Apply theme change - wrap in try/except
            try:
                set_theme(settings['theme'])
                # Only call apply_theme_to_all if it exists
                if hasattr(self.gui, 'apply_theme_to_all') and callable(
                        self.gui.apply_theme_to_all):
                    self.gui.apply_theme_to_all()
                else:
                    # Fallback - apply theme to current widget only
                    self.apply_theme()
            except Exception as theme_error:
                print(f"Error applying theme change: {str(theme_error)}")

            QMessageBox.information(
                self,
                self.translator.t('success'),
                self.translator.t('settings_saved'),
                buttons=QMessageBox.Ok
            )

        except Exception as e:
            print(f"Settings save error: {str(e)}")
            QMessageBox.critical(
                self,
                self.translator.t('error'),
                f"{self.translator.t('settings_save_error')}\n{str(e)}",
                buttons=QMessageBox.Ok
            )
        finally:
            QApplication.restoreOverrideCursor()

    def cancel_changes(self):
        """Revert to the initial settings and go back to previous view"""
        try:
            # Safe navigation to previous view
            if hasattr(self.gui, 'content') and hasattr(self.gui.content, 'stack'):
                self.gui.content.stack.setCurrentIndex(0)
            elif hasattr(self.gui, 'content_stack'):  # In your updated GUI structure
                self.gui.content_stack.setCurrentWidget(self.gui.home_page)

            # Reload settings from database - prepare for next time
            self.load_initial_settings()
        except Exception as e:
            print(f"Cancel settings error: {str(e)}")
            # If navigation fails, just reload settings
            self.load_initial_settings()

    def _apply_theme_change(self, theme_name):
        """Apply theme change - now with better error handling"""
        try:
            # Apply the theme
            set_theme(theme_name)

            # Apply theme to GUI if method exists
            if hasattr(self.gui, 'apply_theme_to_all') and callable(
                    self.gui.apply_theme_to_all):
                self.gui.apply_theme_to_all()
            elif hasattr(self.gui, 'apply_theme') and callable(self.gui.apply_theme):
                self.gui.apply_theme()

            # Always apply theme to self
            self.apply_theme()
        except Exception as e:
            print(f"Theme change error: {str(e)}")

    def _create_appearance_group(self, parent):
        group = QGroupBox(self.translator.t('appearance'), parent)
        # Style will be applied in apply_theme()

        layout = QFormLayout()
        self.color_theme_label = QLabel(self.translator.t('color_theme'))
        self.theme_combo = QComboBox()

        # Use direct theme display names instead of translations
        self.theme_combo.addItems(self.theme_display_names)

        layout.addRow(self.color_theme_label, self.theme_combo)
        group.setLayout(layout)
        return group


    def apply_theme(self):
        """Apply theme to all settings widget components"""
        # Get current theme name from the selected index
        current_theme = self.theme_names[self.theme_combo.currentIndex()]

        # Get current theme colors
        text_color = get_color('text')
        title_color = get_color(
            'text')  # Fallback to text color if title color not available
        border_color = get_color('border')
        primary_color = get_color('primary')
        input_bg = get_color('input_bg')
        button_color = get_color('button')
        button_hover = get_color('button_hover')
        button_pressed = get_color('button_pressed')
        success_color = get_color('success')
        warning_color = get_color('warning')

        # Get shadow color safely with a fallback
        try:
            shadow_color = get_color('shadow')
        except:
            shadow_color = "#00000033"  # Light shadow as fallback

        # Enhanced styles for light theme specifically
        is_light_theme = current_theme == "light"
        box_shadow = f"0px 2px 4px {shadow_color}" if is_light_theme else "none"
        input_shadow = f"inset 0px 1px 2px {shadow_color}" if is_light_theme else "none"

        # Base style for widget
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {primary_color};
                color: {text_color};
                font-size: 16px;
            }}

            /* Group boxes - now with dynamic title color */
            QGroupBox {{
                border: 2px solid {border_color};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 25px;
                background-color: {primary_color};
                box-shadow: {box_shadow};
            }}

            QGroupBox::title {{
                color: {title_color};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                background-color: {primary_color};
            }}

            /* Buttons with enhanced definition */
            QPushButton {{
                background-color: {button_color};
                color: {text_color};
                border: {'1px' if is_light_theme else '2px'} solid {border_color};
                border-radius: 6px;
                padding: 12px 24px;
                min-width: 120px;
                font-weight: bold;
                box-shadow: {box_shadow};
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_pressed};
                box-shadow: {'inset 0px 1px 2px ' + shadow_color if is_light_theme else 'none'};
            }}

            /* Input fields with improved definition */
            QLineEdit, QComboBox, QSpinBox {{
                background-color: {input_bg};
                color: {text_color};
                border: {'1px' if is_light_theme else '2px'} solid {border_color};
                border-radius: 4px;
                padding: 8px 12px;
                min-height: 36px;
                box-shadow: {input_shadow};
            }}

            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}

            QComboBox::down-arrow {{
                image: url(resources/arrow_down.png);
                width: 12px;
                height: 12px;
            }}

            /* Scroll area */
            QScrollArea {{
                border: none;
                background: transparent;
            }}

            /* Checkbox styling */
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {border_color};
                border-radius: 3px;
                background-color: {input_bg};
            }}

            QCheckBox::indicator:checked {{
                background-color: {success_color};
                border-color: {success_color};
                image: url(resources/check.png);
            }}
        """)

        # Special button styling with improved definition
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {success_color};
                border-color: {success_color};
                color: {'white' if is_light_theme else text_color};
                box-shadow: {box_shadow};
            }}
            QPushButton:hover {{
                background-color: {QColor(success_color).darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(success_color).darker(120).name()};
                box-shadow: {'inset 0px 1px 2px ' + shadow_color if is_light_theme else 'none'};
            }}
        """)

        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {warning_color};
                border-color: {warning_color};
                color: {'white' if is_light_theme else text_color};
                box-shadow: {box_shadow};
            }}
            QPushButton:hover {{
                background-color: {QColor(warning_color).darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(warning_color).darker(120).name()};
                box-shadow: {'inset 0px 1px 2px ' + shadow_color if is_light_theme else 'none'};
            }}
        """)

        # Apply specific styles to each group box
        group_style = f"""
            QGroupBox {{
                border: {'1px' if is_light_theme else '2px'} solid {border_color};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 25px;
                background-color: {primary_color};
                box-shadow: {box_shadow};
            }}

            QGroupBox::title {{
                color: {title_color};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                background-color: {primary_color};
            }}
        """

        for group in [self.language_group, self.appearance_group,
                      self.technical_group, self.inventory_group]:
            group.setStyleSheet(group_style)

        # Force refresh
        self.update()
        QApplication.processEvents()

    def get_current_settings(self):
        """Get the current settings values from UI components"""
        return {
            'theme': self.theme_names[self.theme_combo.currentIndex()],
            'language': self.language_combo.currentData(),
            'low_stock_threshold': self.low_stock_threshold_input.text().strip(),
            'default_currency': self.default_currency_combo.currentText().lower(),
            'auto_restock': self.auto_restock_checkbox.isChecked(),
            'backup_interval': self.db_backup_interval.currentIndex(),
            'measurement_units': self.units_combo.currentIndex()
        }

    def load_initial_settings(self):
        # Load theme
        saved_theme = self.gui.settings_db.get_setting('theme', 'classic')
        try:
            theme_index = self.theme_names.index(saved_theme)
        except ValueError:
            # Fallback if theme name is not recognized
            theme_index = 0

        self.theme_combo.setCurrentIndex(theme_index)

        # Load other settings...
        low_stock = self.gui.settings_db.get_setting('low_stock_threshold', '10')
        self.low_stock_threshold_input.setText(low_stock)
        is_rtl = self.gui.settings_db.get_setting('rtl', 'false') == 'true'
        self.language_combo.setCurrentIndex(1 if is_rtl else 0)

        # Store initial settings after loading
        self.initial_settings = self.get_current_settings()


    def _create_language_group(self, parent):
        group = QGroupBox(self.translator.t('language_settings'), parent)
        layout = QFormLayout()
        self.interface_lang_label = QLabel(self.translator.t('interface_language'))
        self.language_combo = QComboBox()
        self.language_combo.addItem(self.translator.t('english'), "en")
        self.language_combo.addItem(self.translator.t('hebrew'), "he")
        index = 0 if self.translator.language == 'en' else 1
        self.language_combo.setCurrentIndex(index)
        layout.addRow(self.interface_lang_label, self.language_combo)
        group.setLayout(layout)
        return group

    def _create_technical_group(self, parent):
        group = QGroupBox(self.translator.t('technical_settings'), parent)
        main_layout = QVBoxLayout()
        db_group = QGroupBox(self.translator.t('auto_backup'))
        db_layout = QFormLayout(db_group)
        self.db_backup_interval = QComboBox()
        self.db_backup_interval.addItems([self.translator.t('daily'),
                                          self.translator.t('weekly'),
                                          self.translator.t('monthly')])
        db_layout.addRow(QLabel(self.translator.t('auto_backup')),
                         self.db_backup_interval)
        db_group.setLayout(db_layout)
        units_group = QGroupBox(self.translator.t('measurement_units'))
        units_layout = QFormLayout(units_group)
        self.units_combo = QComboBox()
        self.units_combo.addItems([self.translator.t('metric_system'),
                                   self.translator.t('imperial_system')])
        units_layout.addRow(QLabel(self.translator.t('measurement_units')),
                            self.units_combo)
        units_group.setLayout(units_layout)
        self.invoice_template_btn = QPushButton(
            self.translator.t('select_invoice_template'))
        self.invoice_template_btn.setFixedHeight(40)
        self.invoice_template_btn.clicked.connect(
            lambda: print("Invoice template selection dialog (placeholder)"))
        main_layout.addWidget(db_group)
        main_layout.addWidget(units_group)
        main_layout.addWidget(self.invoice_template_btn)
        main_layout.addStretch()
        group.setLayout(main_layout)
        return group

    def update_translations(self):
        # Update all groups using the translator
        self.language_group.setTitle(self.translator.t('language_settings'))
        self.interface_lang_label.setText(self.translator.t('interface_language'))
        self.language_combo.setItemText(0, self.translator.t('english'))
        self.language_combo.setItemText(1, self.translator.t('hebrew'))

        self.appearance_group.setTitle(self.translator.t('appearance'))
        self.color_theme_label.setText(self.translator.t('color_theme'))

        # We're not translating theme names anymore, using English display names directly
        # No need to update theme_combo translations

        self.technical_group.setTitle(self.translator.t('technical_settings'))
        self.db_backup_interval.setItemText(0, self.translator.t('daily'))
        self.db_backup_interval.setItemText(1, self.translator.t('weekly'))
        self.db_backup_interval.setItemText(2, self.translator.t('monthly'))
        self.units_combo.setItemText(0, self.translator.t('metric_system'))
        self.units_combo.setItemText(1, self.translator.t('imperial_system'))
        self.invoice_template_btn.setText(self.translator.t('select_invoice_template'))

        self.inventory_group.setTitle(self.translator.t('inventory_settings'))
        self.low_stock_threshold_label.setText(self.translator.t('low_stock_threshold'))
        self.default_currency_label.setText(self.translator.t('default_currency'))
        self.auto_restock_label.setText(self.translator.t('enable_auto_restock'))

        self.save_btn.setText(self.translator.t('save'))
        self.cancel_btn.setText(self.translator.t('cancel'))

        new_direction = Qt.RightToLeft if self.translator.language == 'he' else Qt.LeftToRight
        self.setLayoutDirection(new_direction)
        for child in self.findChildren(QWidget):
            child.setLayoutDirection(new_direction)
        self.updateGeometry()
        self._update_labels()
        self._update_combo_boxes()

        # Then handle layout direction and reapply theme
        self._apply_layout_direction()
        self.apply_theme()  # Re-apply theme after translations

    def _update_labels(self):
        """Update all labels and group titles"""
        # Group boxes
        self.language_group.setTitle(self.translator.t('language_settings'))
        self.appearance_group.setTitle(self.translator.t('appearance'))
        self.technical_group.setTitle(self.translator.t('technical_settings'))
        self.inventory_group.setTitle(self.translator.t('inventory_settings'))

        # Labels
        self.interface_lang_label.setText(self.translator.t('interface_language'))
        self.color_theme_label.setText(self.translator.t('color_theme'))
        self.low_stock_threshold_label.setText(self.translator.t('low_stock_threshold'))
        self.default_currency_label.setText(self.translator.t('default_currency'))
        self.auto_restock_label.setText(self.translator.t('enable_auto_restock'))
        self.invoice_template_btn.setText(self.translator.t('select_invoice_template'))

        # Buttons
        self.save_btn.setText(self.translator.t('save'))
        self.cancel_btn.setText(self.translator.t('cancel'))

    def _apply_layout_direction(self):
        direction = Qt.RightToLeft if self.translator.language == 'he' else Qt.LeftToRight
        self.setLayoutDirection(direction)
        # Force layout refresh
        self.layout().update()
        self.layout().activate()
        for child in self.findChildren(QWidget):
            child.setLayoutDirection(direction)
            if hasattr(child, 'layout') and callable(child.layout) and child.layout():
                child.layout().update()
        self.updateGeometry()

    def _create_inventory_group(self, parent):
        # Inventory settings group
        group = QGroupBox(self.translator.t('inventory_settings'), parent)
        # Style will be applied in apply_theme()

        layout = QFormLayout()

        # Low stock threshold
        self.low_stock_threshold_label = QLabel(self.translator.t('low_stock_threshold'))
        self.low_stock_threshold_input = QLineEdit()
        self.low_stock_threshold_input.setValidator(QIntValidator(0, 10000, self))
        layout.addRow(self.low_stock_threshold_label, self.low_stock_threshold_input)

        # Default currency with translations
        self.default_currency_label = QLabel(self.translator.t('default_currency'))
        self.default_currency_combo = QComboBox()
        currencies = [
            self.translator.t('usd'),
            self.translator.t('eur'),
            self.translator.t('gbp'),
            self.translator.t('ils')
        ]
        self.default_currency_combo.addItems(currencies)
        layout.addRow(self.default_currency_label, self.default_currency_combo)

        # Auto-restock toggle
        self.auto_restock_label = QLabel(self.translator.t('enable_auto_restock'))
        self.auto_restock_checkbox = QCheckBox()
        self.auto_restock_checkbox.setChecked(True)
        layout.addRow(self.auto_restock_label, self.auto_restock_checkbox)

        group.setLayout(layout)
        return group

    def _update_combo_boxes(self):
        """Update all combo box items with translations"""
        # Language combo
        self.language_combo.setItemText(0, self.translator.t('english'))
        self.language_combo.setItemText(1, self.translator.t('hebrew'))

        # We no longer translate theme names, using direct English display names
        # NOT translating theme combo items anymore

        # Backup interval combo
        self.db_backup_interval.setItemText(0, self.translator.t('daily'))
        self.db_backup_interval.setItemText(1, self.translator.t('weekly'))
        self.db_backup_interval.setItemText(2, self.translator.t('monthly'))

        # Units combo
        self.units_combo.setItemText(0, self.translator.t('metric_system'))
        self.units_combo.setItemText(1, self.translator.t('imperial_system'))

