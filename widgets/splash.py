from shared_imports import *
from shared import SCRIPT_DIR

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        screen = QDesktopWidget().availableGeometry()
        sw, sh = screen.width(), screen.height()
        target_w, target_h = int(sw * 0.30), int(sh * 0.30)

        pix = QPixmap(str(SCRIPT_DIR / 'resources/intro.jpg'))
        if pix.isNull():
            raise FileNotFoundError("Splash image not found!")
        pix = pix.scaled(target_w, target_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.logo = QLabel(self)
        self.logo.setPixmap(pix)
        self.logo.setAlignment(Qt.AlignCenter)
        self.resize(pix.size())
        self.move((sw - pix.width()) // 2, (sh - pix.height()) // 2)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(8000)
        self.animation.setStartValue(1.0)
        self.animation.setKeyValueAt(0.3, 0.8)
        self.animation.setKeyValueAt(0.7, 0.85)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutSine)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.animation.start()
        self.timer.start(6000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.logo.pixmap())

    def closeEvent(self, event):
        try:
            self.animation.stop()
            self.timer.stop()
            self.logo.deleteLater()
            self.deleteLater()
            QApplication.processEvents()
        except Exception as e:
            print(f"Splash cleanup error: {str(e)}")
        super().closeEvent(event)