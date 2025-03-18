from shared_imports import *
from database.car_parts_db import CarPartsDB
class DatabaseWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, db, operation, *args, **kwargs):
        super().__init__()
        self.db = db
        self.operation = operation
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            if self.operation == "load":
                result = self.db.get_all_parts()
                self.finished.emit(result)
            elif self.operation == "add":
                success = self.db.add_part(**self.kwargs)
                self.finished.emit(success)
        except Exception as e:
            self.error.emit(str(e))