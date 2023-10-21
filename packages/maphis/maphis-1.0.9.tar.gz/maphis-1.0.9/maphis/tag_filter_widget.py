import typing
from typing import Optional

import PySide6
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout

from maphis.common.state import State
from maphis.common.storage import StorageUpdate, Storage
from maphis.common.utils import is_cursor_inside
from maphis.project.project import Project
from maphis.tags_widget import TagsPopupPanel
from maphis.tags.tag_chooser import TagsChooser


class TagFilterWidget(QWidget):
    active_tags_changed = Signal(list)

    def __init__(self, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self._project: typing.Optional[Project] = None

        self._container = QVBoxLayout()
        self._main_layout = QHBoxLayout()

        self._label = QLabel(text='Tag filter:')
        self._main_layout.addWidget(self._label)

        self.tag_chooser: TagsChooser = TagsChooser(self)
        self.tag_chooser.set_button_visible(True)
        self.tag_chooser.button.setText('Clear')
        self.tag_chooser.matching_photo_count_label.setVisible(False)

        self.tag_chooser.selection_changed.connect(self.active_tags_changed.emit)

        self._main_layout.addWidget(self.tag_chooser)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._container.addLayout(self._main_layout)

        self._lblPhotoCount = QLabel("")
        self._container.addWidget(self._lblPhotoCount)

        self.setLayout(self._container)

    def set_project(self, project: typing.Optional[Project]):
        self._project = project
        if self._project is None:
            return
        self._project.storage.storage_update.connect(self.handle_storage_update)
        self.tag_chooser.set_project(self._project)

    def handle_active_tags_changed(self, active_tags: typing.List[str]):
        self.tag_chooser.set_selected_tags(active_tags, emit_signal=False)
        self._update_photo_count_message()

    def handle_storage_update(self, _: StorageUpdate):
        self.tag_chooser.tag_list_widget.popup.populate(self._project)
        # self.handle_active_tags_changed(self._state.active_tags_filter)
        self._update_photo_count_message()

    def _update_photo_count_message(self):
        hidden_count = 1 # self._state.hidden_photos_count
        shown_count = 2 #self._state.storage.image_count - hidden_count
        self._lblPhotoCount.setText(f'Showing {shown_count} photo{"s" if shown_count != 1 else ""}{"" if hidden_count == 0 else f" ({hidden_count} hidden)"}.')

    def enterEvent(self, event:PySide6.QtCore.QEvent):
        super(TagFilterWidget, self).enterEvent(event)

    def leaveEvent(self, event:PySide6.QtCore.QEvent):
        super(TagFilterWidget, self).leaveEvent(event)
