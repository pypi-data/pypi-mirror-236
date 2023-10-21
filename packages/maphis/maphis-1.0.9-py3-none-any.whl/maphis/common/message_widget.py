from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QDialogButtonBox


class MessageWidget(QDialog):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, f)

        self.layout = QVBoxLayout()

        self.message: QLabel = QLabel()
        self.detailed_message: QTextBrowser = QTextBrowser()

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.button_box.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self.reject)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.detailed_message)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
