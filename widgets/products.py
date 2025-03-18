from shared_imports import *
from translator import Translator
from widgets.dialogs import FilterDialog, AddProductDialog, ItemDetailsDialog
from widgets.workers import DatabaseWorker
from themes import get_color


class ProductsWidget(QWidget):
    def __init__(self, translator, db):
        super().__init__()
        self._is_closing = False
        self.worker_thread = None
        self.translator = translator
        self.db = db
        self.setup_ui()
        self.table.cellDoubleClicked.connect(self.show_item_details)
        QTimer.singleShot(100, self.load_products)
        self.apply_theme()  # Apply theme on initialization

    def apply_theme(self):
        """Apply current theme to all elements"""
        # Base styles
        base_style = f"""
              QWidget {{
                  color: {get_color('text')};
                  font-family: 'Segoe UI';
                  font-size: 14px;
              }}
          """
        self.setStyleSheet(base_style)

        # Button styling
        btn_style = f"""
              QPushButton {{
                  background-color: {get_color('button')};
                  color: {get_color('text')};
                  border: 1px solid {get_color('border')};
                  border-radius: 4px;
                  padding: 10px 18px;  /* Increased padding */
                  margin: 3px;
                  font-size: 15px;     /* Larger font */
                  font-weight: bold;
              }}
              QPushButton:hover {{
                  background-color: {get_color('button_hover')};
                  border: 1px solid {get_color('button_hover')};
              }}
              QPushButton:pressed {{
                  background-color: {get_color('button_pressed')};
              }}
              QPushButton:disabled {{
                  background-color: {get_color('secondary')};
                  color: {get_color('border')};
              }}
          """

        for btn in [self.add_btn, self.select_toggle, self.remove_btn, self.filter_btn]:
            btn.setStyleSheet(btn_style)

        # Table styling with larger elements
        table_style = f"""
              QTableWidget {{
                  background-color: {get_color('background')};
                  alternate-background-color: {get_color('secondary')};
                  gridline-color: {get_color('border')};
                  border: 1px solid {get_color('border')};
                  border-radius: 4px;
                  font-size: 14px;  /* Larger text */
              }}
              QHeaderView::section {{
                  background-color: {get_color('header')};
                  color: {get_color('text')};
                  padding: 10px;    /* Increased padding */
                  border: none;
                  font-weight: bold;
                  font-size: 15px;  /* Larger header text */
              }}
              QTableWidget::item {{
                  padding: 8px;     /* Increased cell padding */
              }}
              QTableWidget::item:selected {{
                  background-color: {get_color('button_hover')};
                  color: {get_color('text')};
              }}
          """
        self.table.setStyleSheet(table_style)

        # Scrollbar styling
        scroll_style = f"""
              QScrollBar:vertical {{
                  background: {get_color('background')};
                  width: 14px;  /* Wider scrollbar */
                  margin: 0;
              }}
              QScrollBar::handle:vertical {{
                  background: {get_color('button')};
                  min-height: 20px;
                  border-radius: 7px;
              }}
              QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                  background: none;
              }}
          """
        self.table.verticalScrollBar().setStyleSheet(scroll_style)

    def show_item_details(self, row, column):
        id_item = self.table.item(row, 0)
        if not id_item:
            return
        try:
            part_id = int(id_item.text())
            # Fetch the full details for this part; assume get_part returns a tuple
            item = self.db.get_part(part_id)
            # Map your tuple to a dictionary for clarity
            details = {
                "ID": item[0],
                "Category": item[1],
                "Car": item[2],
                "Model": item[3],
                "Product Name": item[4],
                "Quantity": item[5],
                "Price": item[6]
            }
            dialog = ItemDetailsDialog(details, self.translator, self)
            dialog.exec_()  # Modal dialog; or dialog.show() for non-modal
        except Exception as e:
            print(f"Error opening details: {e}")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15,
                                       15)  # Add some padding around the widget
        main_layout.setSpacing(15)  # Increase spacing between elements

        # --- Button Panel ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Increase spacing between buttons

        # Buttons will be styled in apply_theme()
        self.add_btn = QPushButton(self.translator.t('add_product'))
        self.add_btn.clicked.connect(self.show_add_dialog)
        button_layout.addWidget(self.add_btn)

        self.select_toggle = QPushButton(self.translator.t('select_button'))
        self.select_toggle.setCheckable(True)
        self.select_toggle.toggled.connect(self.on_select_toggled)
        button_layout.addWidget(self.select_toggle)

        self.remove_btn = QPushButton(self.translator.t('remove'))
        self.remove_btn.clicked.connect(self.universal_remove)
        button_layout.addWidget(self.remove_btn)

        self.filter_btn = QPushButton(self.translator.t('filter_button'))
        self.filter_btn.clicked.connect(self.show_filter_dialog)
        button_layout.addWidget(self.filter_btn)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # --- Table Setup ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.update_headers()
        self.table.verticalHeader().setVisible(False)

        # Set row height to make cells larger
        self.table.verticalHeader().setDefaultSectionSize(40)  # Taller rows

        # Custom column widths instead of stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Set specific column widths for different types of data
        self.adjust_column_widths()

        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellChanged.connect(self.on_cell_changed)
        self.table.setAlternatingRowColors(
            True)  # Add alternating row colors for better readability
        main_layout.addWidget(self.table)

    def adjust_column_widths(self):
        """Set custom column widths based on data importance"""
        # Total width calculation (approximate)
        total_width = self.width() - 40  # Subtract scrollbar width and some padding

        # Column width distribution (percentages)
        # ID: 8%, Category: 12%, Car: 15%, Model: 15%, Name: 28%, Qty: 10%, Price: 12%
        col_widths = [8, 12, 15, 15, 28, 10, 12]

        # Apply the widths
        for i, width_percent in enumerate(col_widths):
            width = int(total_width * width_percent / 100)
            self.table.setColumnWidth(i, width)

    def resizeEvent(self, event):
        """Handle resize events to adjust column widths"""
        super().resizeEvent(event)
        self.adjust_column_widths()

    def highlight_product(self, search_text):
        """Scroll to and highlight matching product using theme colors"""
        search_text = search_text.lower()
        for row in range(self.table.rowCount()):
            product_item = self.table.item(row, 4)
            if product_item and search_text in product_item.text().lower():
                self.table.scrollToItem(product_item)
                self.table.blockSignals(True)
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor(get_color('button')))
                self.table.blockSignals(False)
                QTimer.singleShot(2000, lambda r=row: self.clear_highlight(r))

    def clear_highlight(self, row):
        """Clear highlight using theme background color"""
        self.table.blockSignals(True)
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setBackground(QColor(get_color('background')))
        self.table.blockSignals(False)

    def on_select_toggled(self, checked):
        """Handle the selection toggle button being checked or unchecked."""
        if checked:
            print("Select mode enabled")
            # Implement behavior for when select mode is enabled (e.g., allow multi-selection)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        else:
            print("Select mode disabled")
            # Implement behavior for when select mode is disabled
            self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)

    def update_headers(self):
        headers = [
            self.translator.t('id'),
            self.translator.t('category'),
            self.translator.t('car'),
            self.translator.t('model'),
            self.translator.t('product_name'),
            self.translator.t('quantity'),
            self.translator.t('price')
        ]
        self.table.setHorizontalHeaderLabels(headers)

    # (The rest of the methods remain unchanged...)

    def show_filter_dialog(self):
        dialog = FilterDialog(self.translator, self)
        if dialog.exec_() == QDialog.Accepted:
            filters = dialog.get_filters()
            self.filter_products(filters)

    def filter_products(self, filters):
        try:
            # Get all products from the database
            all_products = self.db.get_all_parts()
            filtered = []
            # Assuming column mapping: id:0, category:1, car:2, model:3, product_name:4, quantity:5, price:6
            for prod in all_products:
                category = prod[1] if prod[1] else ""
                name = prod[4] if prod[4] else ""
                price = float(prod[6])
                # Apply filters; if filter is provided and not matched, skip product.
                if filters["category"] and filters[
                    "category"].lower() not in category.lower():
                    continue
                if filters["name"] and filters["name"].lower() not in name.lower():
                    continue
                if filters["min_price"] is not None and price < filters["min_price"]:
                    continue
                if filters["max_price"] is not None and price > filters["max_price"]:
                    continue
                filtered.append(prod)

            # Update the table with filtered products
            self.table.blockSignals(True)
            self.table.clearContents()
            self.table.setRowCount(len(filtered))
            for row, prod in enumerate(filtered):
                # ID column (non-editable)
                id_item = QTableWidgetItem(str(prod[0]))
                id_item.setFlags(id_item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row, 0, id_item)
                # Columns 1-4: category, car, model, product name
                for col in range(1, 5):
                    text = str(prod[col]) if prod[col] not in [None, ""] else "-"
                    self.table.setItem(row, col, QTableWidgetItem(text))
                # Quantity (col 5)
                self.table.setItem(row, 5, QTableWidgetItem(str(prod[5])))
                # Price (col 6)
                self.table.setItem(row, 6, QTableWidgetItem(f"{float(prod[6]):.2f}"))
            self.table.blockSignals(False)
        except Exception as e:
            print("Error filtering products:", e)
            self.show_error("Failed to filter products")

    def load_products(self):
        if self._is_closing:
            return
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait(1000)

        # Clear existing data first
        self.table.blockSignals(True)
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.blockSignals(False)

        # Create and start worker thread
        self.worker_thread = DatabaseWorker(self.db, "load")
        self.worker_thread.finished.connect(self.handle_loaded_products)
        self.worker_thread.error.connect(self.show_error)
        self.worker_thread.start()

    def on_cell_changed(self, row, column):
        try:
            # Only allow cell edits for columns 1-6 (skip ID column)
            if not (0 <= row < self.table.rowCount() and 1 <= column < 7):
                return
            item = self.table.item(row, column)
            id_item = self.table.item(row, 0)
            if not item or not id_item:
                return
            try:
                part_id = int(id_item.text())
            except ValueError:
                self.show_error("Invalid product ID")
                return
            field_map = {
                1: 'category',
                2: 'car_name',
                3: 'model',
                4: 'product_name',
                5: 'quantity',
                6: 'price'
            }
            field = field_map.get(column)
            new_value = item.text().strip()
            # For product name, don't allow empty (if editing column 4)
            if field == 'product_name' and not new_value:
                self.show_error("Product name cannot be empty")
                self._revert_cell(row, column)
                return
            if field in ['quantity', 'price']:
                try:
                    new_value = int(new_value) if field == 'quantity' else round(
                        float(new_value), 2)
                    if new_value < 0:
                        raise ValueError
                except ValueError:
                    self.show_error("Invalid numeric value")
                    self._revert_cell(row, column)
                    return
            if self.db.update_part(part_id, **{field: new_value}):
                updated = self.db.get_part(part_id)
                if not updated:
                    raise ValueError("Product not found after update")
                self._refresh_row(row, updated)
                QMessageBox.information(self, "Success", "Update successful")
            else:
                raise RuntimeError("Database update failed")
        except Exception as e:
            print(f"Cell change error: {e}")
            self.show_error("Failed to save changes")
            self._revert_cell(row, column)
            self.load_products()

    def _refresh_row(self, row, data):
        self.table.blockSignals(True)
        try:
            for col in range(7):
                if col == 0:
                    val = str(data[0])
                elif col in [1, 2, 3, 4]:
                    val = str(data[col]) if data[col] else "-"
                elif col == 5:
                    val = str(int(data[5]))
                elif col == 6:
                    val = f"{float(data[6]):.2f}"
                else:
                    val = ""
                if self.table.item(row, col):
                    self.table.item(row, col).setText(val)
        finally:
            self.table.blockSignals(False)

    def _revert_cell(self, row, column):
        self.table.blockSignals(True)
        if self.table.item(row, column):
            self.table.item(row, column).setText(self.table.item(row, column).text())
        self.table.blockSignals(False)

    def show_add_dialog(self):
        try:
            dialog = AddProductDialog(self.translator, self)
            dialog.finished.connect(lambda: self.safe_load_data(dialog))
            dialog.show()
        except Exception as e:
            print(f"Dialog error: {e}")

    def safe_load_data(self, dialog):
        if dialog.result() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                QMetaObject.invokeMethod(self, "process_add_product", Qt.QueuedConnection,
                                         Q_ARG(dict, data))
            except Exception as e:
                print(f"Data processing error: {e}")

    @pyqtSlot(dict)
    def process_add_product(self, data):
        try:
            existing = self.db.get_part_by_name(data['product_name'])
            if existing:
                confirm = QMessageBox.question(
                    self,
                    self.translator.t('overwrite_title'),
                    self.translator.t('overwrite_message'),
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    success = self.db.update_part(existing[0], **data)
                    if not success:
                        raise Exception("Failed to update existing product")
                else:
                    return
            else:
                success = self.db.add_part(**data)
                if not success:
                    raise Exception("Failed to add new product")
            self.load_products()
        except Exception as e:
            print(f"Add product error: {e}")
            QMessageBox.critical(self, self.translator.t('error'),
                                 self.translator.t('save_error'))

    @pyqtSlot(object)
    def handle_loaded_products(self, products):
        try:
            scroll_bar = self.table.verticalScrollBar()
            scroll_pos = scroll_bar.value()

            self.table.blockSignals(True)
            self.table.setSortingEnabled(False)
            self.table.setRowCount(len(products))

            for row, prod in enumerate(products):
                # ID column (non-editable)
                id_item = QTableWidgetItem(str(prod[0]))
                id_item.setFlags(id_item.flags() ^ Qt.ItemIsEditable)
                id_item.setTextAlignment(Qt.AlignCenter)  # Center align ID
                self.table.setItem(row, 0, id_item)

                # Other columns
                for col in range(1, 5):
                    text = str(prod[col]) if prod[col] not in [None, ""] else "-"
                    item = QTableWidgetItem(text)
                    # Left align text fields
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table.setItem(row, col, item)

                # Quantity - center align
                qty_item = QTableWidgetItem(str(prod[5]))
                qty_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 5, qty_item)

                # Price - right align
                price_item = QTableWidgetItem(f"{float(prod[6]):.2f}")
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 6, price_item)

                if row % 10 == 0:
                    QApplication.processEvents()

            scroll_bar.setValue(scroll_pos)
            self.table.setSortingEnabled(True)

        except Exception as e:
            print(f"Load error: {e}")
            self.show_error("Failed to load products")
        finally:
            self.table.blockSignals(False)

    def universal_remove(self):
        # When the Select toggle is ON: remove the selected rows
        if self.select_toggle.isChecked():
            selected_rows = self.table.selectionModel().selectedRows()
            if not selected_rows:
                self.show_error("No rows selected.")
                return
            confirm = QMessageBox.question(
                self,
                self.translator.t('confirm_removal'),
                self.translator.t('confirm_remove_message'),
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm != QMessageBox.Yes:
                return
            for index in selected_rows:
                row = index.row()
                id_item = self.table.item(row, 0)
                if id_item:
                    try:
                        part_id = int(id_item.text())
                        self.db.delete_part(part_id)
                    except Exception as e:
                        print(f"Error deleting row {row}: {e}")
            self.load_products()
        else:
            # When not in selection mode: clear the current cell's content (but do nothing if it's the ID column)
            current_item = self.table.currentItem()
            if current_item:
                if current_item.column() == 0:
                    return  # Do not clear the ID column
                current_item.setText("")
                row = current_item.row()
                column = current_item.column()
                id_item = self.table.item(row, 0)
                if id_item:
                    try:
                        part_id = int(id_item.text())
                        field_map = {1: 'category', 2: 'car_name', 3: 'model',
                                     4: 'product_name', 5: 'quantity', 6: 'price'}
                        if column in field_map:
                            field = field_map[column]
                            new_value = "" if column in [1, 2, 3, 4] else 0
                            self.db.update_part(part_id, **{field: new_value})
                    except Exception as e:
                        print(f"Error updating cell: {e}")
                        self.load_products()

    def show_error(self, message):
        if self._is_closing:
            return
        QMessageBox.critical(self, self.translator.t('error'), message)

    def update_translations(self):
        # Remove layout direction changes from all widgets
        self.add_btn.setText(self.translator.t('add_product'))
        self.select_toggle.setText(self.translator.t('select_button'))
        self.remove_btn.setText(self.translator.t('remove'))
        self.filter_btn.setText(self.translator.t('filter_button'))
        self.update_headers()

    def closeEvent(self, event):
        try:
            self._is_closing = True
            # Add None check before accessing worker_thread
            if (self.worker_thread is not None and
                    self.worker_thread.isRunning()):
                self.worker_thread.quit()
                self.worker_thread.wait(1000)
        except Exception as e:
            print(f"Cleanup error: {e}")
        event.accept()

    def get_data(self):
        price = self.price_input.text()
        if not price.replace('.', '', 1).isdigit():
            raise ValueError("Invalid price format")


class ThemedNumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if editor:
            editor.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {get_color('input_bg')};
                    color: {get_color('text')};
                    border: 1px solid {get_color('border')};
                    font-size: 14px;
                    padding: 5px;
                }}
            """)
        return editor

    def paint(self, painter, option, index):
        option.backgroundColor = QColor(get_color('secondary'))
        super().paint(painter, option, index)