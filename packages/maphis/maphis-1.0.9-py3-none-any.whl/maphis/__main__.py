import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from maphis.app import MAPHIS
from maphis.plugins import PLUGINS_FOLDER


def run():
    app = QApplication([])
    print(f'plugins folder is {PLUGINS_FOLDER}')
    window = MAPHIS()
    app.focusChanged.connect(window.handle_focus_changed)
    QTimer.singleShot(100, window.showMaximized)
    sys.exit(app.exec())


if __name__ == '__main__':
    run()