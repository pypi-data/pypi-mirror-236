import dataclasses
import functools
import typing
from enum import IntEnum
from typing import Union, Any, Optional

import PySide6.QtCore
from PySide6.QtCore import QAbstractItemModel, QModelIndex
from PySide6.QtGui import Qt, QPixmap, QColor

from maphis import MAPHIS_PATH
from maphis.common.photo import Photo
from maphis.project.annotation import AnnotationType, Annotation, KeypointAnnotation, Keypoint


class AnnotationTreeItemData:
    def __init__(self, data, parent):
        self.data: typing.Optional[typing.Union[Annotation, typing.Any]] = data
        self.parent: typing.Optional[QModelIndex] = parent


class ItemDataVariant(IntEnum):
    Annotation = 0
    AnnotationData = 1


class TreeItem:
    def __init__(self, data, parentItem=None):
        self.m_childItems = []
        self.m_itemData = data
        self.m_parentItem = parentItem

    def appendChild(self, child):
        self.m_childItems.append(child)

    def child(self, row):
        return self.m_childItems[row]

    def childCount(self):
        return len(self.m_childItems)

    def columnCount(self):
        return len(self.m_itemData)

    def data(self, column: int):
        if 0 <= column < len(self.m_itemData):
            return self.m_itemData[column]
        return None

    def row(self):
        if self.m_parentItem:
            return self.m_parentItem.m_childItems.index(self)
        return 0

    def parentItem(self):
        return self.m_parentItem


class AnnotationTreeItemModel(QAbstractItemModel):
    annotation_type_order: typing.List[AnnotationType] = list(AnnotationType)

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self.root_item: TreeItem = TreeItem(('Annotation',))
        self.items: typing.List[TreeItem] = []

        self._photo: typing.Optional[Photo] = None
        self._annotation_type: typing.Optional[AnnotationType] = None

        self._annotations_flattened: typing.List[Annotation] = []

        self._annotation_to_item: typing.Dict[Annotation, TreeItem] = {}

        self._landmark_icon = QPixmap(MAPHIS_PATH / 'tools/icons/landmarks.png').scaledToWidth(16, Qt.TransformationMode.SmoothTransformation)

    def set_photo(self, photo: Photo):
        self._photo = photo
        self._photo.new_annotation_added.connect(self._handle_new_annotation_added, Qt.ConnectionType.UniqueConnection)
        self._annotations_flattened = functools.reduce(list.__add__, [self._photo.annotations.get(ann_type, []) for ann_type in self.annotation_type_order], [])
        for annotation in self._annotations_flattened:
            annotation.new_annotation_data.connect(self._handle_new_annotation_data, Qt.ConnectionType.UniqueConnection)
            annotation.modified_annotation_data.connect(self._handle_modified_annotation_data)
            annotation.deleted_annotation_data.connect(self._handle_deleted_annotation_data)

            annotation_item = TreeItem((f'{annotation.ann_class} ({annotation.ann_instance_id})', annotation), self.root_item)
            self._annotation_to_item[annotation] = annotation_item

            self.root_item.appendChild(annotation_item)
            if isinstance(annotation, KeypointAnnotation):
                for kp in annotation.kps:
                    kp_item = TreeItem((kp.name, kp.x, kp.y, kp.v, kp.additional_data), annotation_item)
                    annotation_item.appendChild(kp_item)

    def _handle_new_annotation_data(self, ann: Annotation, _dict: typing.Dict[str, typing.Any]):
        ann_item = self._annotation_to_item[ann]
        kp: Keypoint = _dict['kp']
        child_item = TreeItem((kp.name, kp.x, kp.y, kp.v, kp.additional_data, kp), ann_item)
        ann_item.appendChild(child_item)
        parent = self.index(ann_item.row(), 0)

        self.insertRow(ann_item.childCount() - 1, parent)

        self.dataChanged.emit(self.index(0, 0, parent),
                              self.index(ann_item.childCount() - 1, 0, parent))
        self.layoutChanged.emit()

    def _handle_modified_annotation_data(self, ann: Annotation, _dict: typing.Dict[str, typing.Any]):
        ann_item = self._annotation_to_item[ann]
        parent = self.index(ann_item.row(), 0)

        child_item: TreeItem = ann_item.child(_dict['kp_index'])
        kp: Keypoint = _dict['kp']
        child_item.m_itemData = (kp.name, kp.x, kp.y, kp.v, kp.additional_data)

        self.dataChanged.emit(self.index(0, 0, parent),
                              self.index(ann_item.childCount() - 1, 0, parent))
        self.layoutChanged.emit()

    def _handle_deleted_annotation_data(self, ann: Annotation, _dict: typing.Dict[str, typing.Any]):
        ann_item = self._annotation_to_item[ann]
        parent = self.index(ann_item.row(), 0)

        child_item: TreeItem = ann_item.child(_dict['kp_index'])
        kp: Keypoint = _dict['kp']
        child_item.m_itemData = (kp.name, kp.x, kp.y, kp.v, kp.additional_data)

        self.dataChanged.emit(self.index(0, 0, parent),
                              self.index(ann_item.childCount() - 1, 0, parent))
        self.layoutChanged.emit()

    def _handle_new_annotation_added(self, ann_idx: int, ann: Annotation):
        ann.new_annotation_data.connect(self._handle_new_annotation_data, Qt.ConnectionType.UniqueConnection)
        ann.modified_annotation_data.connect(self._handle_modified_annotation_data)
        ann.deleted_annotation_data.connect(self._handle_deleted_annotation_data)

        ann_item = TreeItem((f'{ann.ann_class} ({ann.ann_instance_id})', ann), self.root_item)
        self._annotation_to_item[ann] = ann_item
        self.root_item.m_childItems.append(ann_item)

        parent = QModelIndex()

        self.insertRow(self.root_item.childCount() - 1, parent)

        self.dataChanged.emit(self.index(0, 0, parent),
                              self.index(self.root_item.childCount()- 1, 0, parent))
        self.layoutChanged.emit()

    def display_annotation_type(self, annotation_type: typing.Optional[AnnotationType]):
        self._annotation_type = annotation_type

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> int:
        return 1

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> int:
        if not parent.isValid():
            return sum([len(annotations) for annotations in self._photo.annotations.values()])
        item: TreeItem = parent.internalPointer()
        return item.childCount()

    def index(self, row: int, column: int, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = QModelIndex()) -> PySide6.QtCore.QModelIndex:
        if not parent.isValid():
            item = self.root_item
        else:
            item: TreeItem = parent.internalPointer()
        child_item: typing.Optional[TreeItem] = item.child(row)
        if child_item is None:
            return QModelIndex()
        return self.createIndex(row, column, child_item)

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()
        item: TreeItem = index.internalPointer()
        parent: TreeItem = item.parentItem()
        if parent == self.root_item:
            return QModelIndex()
        return self.createIndex(parent.row(), 0, parent)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        item: TreeItem = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            return item.data(0)
        if role == Qt.ItemDataRole.DecorationRole:
            if item.parentItem() == self.root_item:
                return self._landmark_icon
            else:
                visibility: int = item.data(3)
                if visibility < 0:  # either the landmark has not been placed yet or it is not present in the image
                    return QColor.fromString("gold")
                elif visibility == 0:
                    return QColor.fromString("sandybrown")
                else:
                    return QColor.fromString("greenyellow")
        return None