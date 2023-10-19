import typing
from typing import Optional

import PySide6.QtCore
from PySide6.QtCore import QAbstractListModel, QModelIndex
from PySide6.QtGui import Qt

from maphis.project.annotation import KeypointAnnotation, Keypoint


class LandmarkTableModel(QAbstractListModel):
    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self.lm_annotation: typing.Optional[KeypointAnnotation] = None

    def set_landmarks(self, ann: typing.Optional[KeypointAnnotation]):
        if self.lm_annotation is not None:
            self.lm_annotation.new_annotation_data.disconnect(self._new_annotation_data)
            self.lm_annotation.modified_annotation_data.disconnect(self._modified_annotation_data)
            self.lm_annotation.deleted_annotation_data.disconnect(self._deleted_annotation_data)

        self.lm_annotation = ann

        self.lm_annotation.new_annotation_data.connect(self._new_annotation_data)
        self.lm_annotation.modified_annotation_data.connect(self._modified_annotation_data)
        self.lm_annotation.deleted_annotation_data.connect(self._deleted_annotation_data)

        self._update()

    def rowCount(self, parent: typing.Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> int:
        if self.lm_annotation is None:
            return 0
        return len(self.lm_annotation.kps)

    def columnCount(self, parent: typing.Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> int:
        return 1

    def data(self, index: typing.Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            kp: Keypoint = self.lm_annotation.kps[index.row()]
            return f'{self.lm_annotation.kps[index.row()].name} ({kp.x}, {kp.y})'
        elif role == Qt.ItemDataRole.UserRole:
            return self.lm_annotation.kps[index.row()]
        return None

    def _update(self):
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.rowCount() - 1, 0))
        self.layoutChanged.emit()

    def _new_annotation_data(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self.insertRow(len(self.lm_annotation.kps) - 1)
        self._update()

    def _modified_annotation_data(self, ann: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self._update()

    def _deleted_annotation_data(self, ann: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self._update()

    def removeRows(self, row: int, count: int, parent: typing.Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        kps_to_remove: typing.List[Keypoint] = []
        for r in range(row, row + count):
            kps_to_remove.append(self.lm_annotation.kps[r])
        for kp in kps_to_remove:
            self.lm_annotation.delete_keypoint(kp)
        self.endRemoveRows()
        return True
