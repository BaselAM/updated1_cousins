# # main.py
# import sys
# from pathlib import Path
# from PyQt5.QtCore import Qt, QTimer, QCoreApplication
# from PyQt5.QtWidgets import QApplication
#
# from shared import SCRIPT_DIR
# from shared_imports import *
# from widgets.splash import SplashScreen
# from gui import GUI
# from database.settings_db import SettingsDB
# from database.car_parts_db import CarPartsDB
# from translator import Translator
#
# if __name__ == "__main__":
#     QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
#     app = QApplication(sys.argv)
#
#     try:
#         # Validate resources
#         for fname in ["resources/intro.jpg", "resources/car-icon.jpg", "resources/search_icon.png"]:
#             if not (SCRIPT_DIR / fname).exists():
#                 raise FileNotFoundError(f"Missing file: {SCRIPT_DIR / fname}")
#
#         splash = SplashScreen()
#         splash.show()
#
#         gui = GUI()
#
#         timer = QTimer()
#         timer.setSingleShot(True)
#         timer.timeout.connect(lambda: (splash.close(), gui.show()))
#         timer.start(2000)
#
#         exit_code = app.exec_()
#
#         # Proper shutdown sequence
#         del gui
#         del splash
#         QApplication.processEvents()
#
#         sys.exit(exit_code)
#
#     except Exception as e:
#         print(f"Fatal error: {str(e)}")
#         sys.exit(1)
#



import sys
from pathlib import Path
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication

from shared import SCRIPT_DIR
from shared_imports import *
from widgets.splash import SplashScreen
from gui import GUI
from database.settings_db import SettingsDB
from database.car_parts_db import CarPartsDB
from translator import Translator
from widgets.login_widget import LoginWidget

# Global variables to hold references.
login_widget = None
main_gui = None

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    app = QApplication(sys.argv)

    try:
        # Validate resources.
        for fname in ["resources/intro.jpg", "resources/car-icon.jpg", "resources/search_icon.png"]:
            if not (SCRIPT_DIR / fname).exists():
                raise FileNotFoundError(f"Missing file: {SCRIPT_DIR / fname}")

        splash = SplashScreen()
        splash.show()

        # Pre-create the main GUI, but hide it until login is successful.
        main_gui = GUI()
        main_gui.hide()

        # Create the login widget (which now matches your GUI theme).
        login_widget = LoginWidget()
        login_widget.hide()  # start hidden

        # When login is successful, close the login widget and show the main GUI.
        def on_login():
            login_widget.close()
            main_gui.show()

        login_widget.login_successful.connect(on_login)

        # After the splash, show the login widget.
        def show_login():
            splash.close()
            login_widget.show()

        QTimer.singleShot(2000, show_login)

        exit_code = app.exec_()
        sys.exit(exit_code)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
