import sys
import time

from PySide6.QtCore import QEventLoop, QTimer
from PySide6.QtWidgets import QApplication

sys.path.insert(0, r'c:\Users\Admin\Documents\VYOM_v3')
from ui.main_window import MainWindow

app = QApplication([])
window = MainWindow()
window.show()

loop = QEventLoop()
deadline = time.time() + 45


def check():
    if window.dashboard.recommendation_table.rowCount() > 0 or time.time() >= deadline:
        loop.quit()
    else:
        QTimer.singleShot(1000, check)

QTimer.singleShot(1000, check)
loop.exec()
print('visible', window.isVisible())
print('rows', window.dashboard.recommendation_table.rowCount())
app.quit()
