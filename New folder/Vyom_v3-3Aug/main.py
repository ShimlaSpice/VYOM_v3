import sys

from PySide6.QtWidgets import QApplication

from core.application import Application
from ui.main_window import MainWindow


def main() -> None:

    qt_app = QApplication(sys.argv)

    application = Application()

    application.initialize()

    window = MainWindow()

    window.show()

    qt_app.exec()

    application.shutdown()


if __name__ == "__main__":
    main()