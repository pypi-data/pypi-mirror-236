import importlib.resources
import typing
from typing import Optional, List, Dict

from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QPixmap, Qt, QIcon
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QButtonGroup, QAbstractButton, QPushButton, QSizePolicy, \
    QVBoxLayout, QCheckBox, QLabel, QToolButton

from maphis.common.label_hierarchy import LabelHierarchy
from maphis.common.local_storage import Storage
from maphis.common.state import State


class LabelLevelSwitch(QGroupBox):
    label_level_switched = Signal(int)
    approval_toggled = Signal(int, bool)

    def __init__(self, state: State, parent: Optional[QWidget] = None):
        QGroupBox.__init__(self, parent)
        self.setTitle('Approved levels')
        self.state: State = state
        self.state.storage_changed.connect(self.handle_storage_changed)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._label_buttons_group = QButtonGroup(self)
        self._label_buttons_group.setExclusive(False)
        #self._label_buttons_group.setExclusive(True)
        #self._label_buttons_group.idClicked.connect(self.label_level_switched.emit)
        #self._label_buttons_group.buttonClicked.connect(self._handle_button_clicked)
        self._label_buttons_group.buttonClicked.connect(self._handle_button_toggled)

        stylesheet = "QCheckBox:unchecked { color: rgb(220, 150, 0); }\nQCheckBox:checked { color: rgb(0, 150, 0); }"
        self.setStyleSheet(stylesheet)

        self._buttons: List[QPushButton] = []

        self.selected_label_levels: Dict[str, int] = {}

        self.unapproved_stylesheet: str = QPushButton().styleSheet() + '; border: 1px solid orange'
        self.approved_stylesheet: str = QPushButton().styleSheet() + '; border: 1px solid green'

        #with importlib.resources.open_binary("maphis.resources", "check.png") as icon_io:
        #    bytes = icon_io.read()
        #    pixmap = QPixmap()
        #    if not pixmap.loadFromData(bytes, len(bytes), "PNG"):
        #        print("NOT GOOD")
        #    self._check_icon = QIcon()

        with importlib.resources.path("maphis.resources", "check.png") as path:
            self.check_icon = QIcon(str(path))

        with importlib.resources.path("maphis.resources", "question.png") as path:
            self.question_icon = QIcon(str(path))

    def _handle_button_clicked(self, btn: QAbstractButton):
        self.label_level_switched.emit(self._label_buttons_group.id(btn))
        self.selected_label_levels[self.state.current_label_name] = self._label_buttons_group.id(btn)

    def _handle_button_toggled(self, btn: QAbstractButton):
        self.approval_toggled.emit(self._label_buttons_group.id(btn), btn.isChecked())

    def handle_storage_changed(self, storage: Storage, old_storage: typing.Optional[Storage]):
        self.selected_label_levels.clear()
        for label_name in storage.label_image_names:
            self.selected_label_levels[label_name] = 0

    def set_label_hierarchy(self, lab_hier: LabelHierarchy):
        for btn in self._buttons:
            btn.setVisible(False)
            self._label_buttons_group.removeButton(btn)
            self.layout.removeWidget(btn)
            btn.deleteLater()
        self._buttons.clear()
        for i, level in enumerate(self.state.label_hierarchy.hierarchy_levels):
            #btn = QToolButton()
            name = level.name
            btn = QCheckBox()
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setText(name)
            btn.setObjectName(f'btnLevel_{name}')
            btn.setCheckable(True)
            #btn.setIcon(self.question_icon)
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip(name)
            # if i == 0:
            #     btn.setChecked(True)
            self.layout.addWidget(btn)
            self._label_buttons_group.addButton(btn, i)
            self._buttons.append(btn)
        self.setMaximumWidth(self.maximumWidth())
        self.setEnabled(True)
        self.update()

    def return_to_level_for(self, label_name: str):
        level = self.selected_label_levels[label_name]
        if len(self._buttons) > 1:
            self._buttons[level].animateClick(1)
        else:
            self._handle_button_clicked(self._buttons[level])

    #def get_level_button(self, level_name: str) -> Optional[QAbstractButton]:
    #    return self._label_buttons_group.findChild(QPushButton, f'btnLevel_{level_name}')

    def get_level_button(self, idx: int):
        return self._label_buttons_group.button(idx)

    def mark_approved(self, idx: int, approved: bool):
        #self._label_buttons_group.button(idx).setStyleSheet(self.approved_stylesheet if approved else self.unapproved_stylesheet)
        btn = self._label_buttons_group.button(idx)
        btn.setChecked(approved)
        #if approved:
        #    btn.setIcon(self.check_icon)
        #else:
        #    btn.setIcon(self.question_icon)
    
    def setMaximumWidth(self, maxw: int) -> None:
        if len(self._buttons) > 0:
            left, top, right, bottom = self.layout.getContentsMargins()
            usable_width = maxw - left - right - ((2 * (len(self._buttons) - 1)) + 2) * self.layout.spacing()
            width_per_item = (usable_width / len(self._buttons)) - 32
            metrics = self._buttons[0].fontMetrics()
            for btn, level in zip(self._buttons, self.state.label_hierarchy.hierarchy_levels):
                elided_text = metrics.elidedText(level.name, Qt.TextElideMode.ElideRight, width_per_item)
                btn.setText(elided_text)
        super(LabelLevelSwitch, self).setMaximumWidth(maxw)
