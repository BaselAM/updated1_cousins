from shared_imports import *
class ItemDetailsDialog(QDialog):
    def __init__(self, item_data, translator, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.translator = translator
        self.setWindowTitle("Item Details")  # You can translate this too
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Assuming item_data is a dict with your fields
        for key, value in self.item_data.items():
            layout.addWidget(QLabel(f"{key}: {value}"))
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)


class FilterDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Filter Products")
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                border: 1px solid #1abc9c;
                padding: 4px;
            }
            QDialogButtonBox QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #3498db;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #1c638d;
            }
        """)
        layout = QFormLayout(self)
        self.category_input = QLineEdit()
        self.name_input = QLineEdit()
        self.min_price_input = QLineEdit()
        self.min_price_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2, self))
        self.max_price_input = QLineEdit()
        self.max_price_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2, self))
        layout.addRow("Category:", self.category_input)
        layout.addRow("Product Name:", self.name_input)
        layout.addRow("Min Price:", self.min_price_input)
        layout.addRow("Max Price:", self.max_price_input)
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_filters(self):
        return {
            "category": self.category_input.text().strip(),
            "name": self.name_input.text().strip(),
            "min_price": float(
                self.min_price_input.text()) if self.min_price_input.text() else None,
            "max_price": float(
                self.max_price_input.text()) if self.max_price_input.text() else None
        }



class AddProductDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)  # Prevent memory leaks
        self.translator = translator
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.translator.t('add_product'))
        # Apply dark theme styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                border: 1px solid #1abc9c;
                padding: 4px;
            }
            QDialogButtonBox QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #3498db;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #1c638d;
            }
        """)

        layout = QFormLayout(self)

        self.category_input = QLineEdit()
        self.car_name_input = QLineEdit()
        self.model_input = QLineEdit()
        self.product_name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(QIntValidator(0, 999999, self))
        self.price_input = QLineEdit()
        self.price_input.setValidator(QDoubleValidator(0.0, 999999.99, 2, self))

        layout.addRow(self.translator.t('category'), self.category_input)
        layout.addRow(self.translator.t('car'), self.car_name_input)
        layout.addRow(self.translator.t('model'), self.model_input)
        layout.addRow(self.translator.t('product_name'), self.product_name_input)
        layout.addRow(self.translator.t('quantity'), self.quantity_input)
        layout.addRow(self.translator.t('price'), self.price_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def validate_and_accept(self):
        if not self.product_name_input.text().strip():
            QMessageBox.warning(
                self,
                self.translator.t('error'),
                self.translator.t('required_field')
            )
            return
        self.accept()

    def get_data(self):
        return {
            'category': self.category_input.text().strip(),
            'car_name': self.car_name_input.text().strip(),
            'model': self.model_input.text().strip(),
            'product_name': self.product_name_input.text().strip(),
            'quantity': int(
                self.quantity_input.text()) if self.quantity_input.text() else 0,
            'price': float(self.price_input.text()) if self.price_input.text() else 0.0
        }

    def closeEvent(self, event):
        """Cleanup resources"""
        self.deleteLater()
        super().closeEvent(event)