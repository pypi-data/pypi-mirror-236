import typing

from PySide6.QtCore import QPoint, QObject
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QGraphicsItem

from maphis.common.common import Info
from maphis.common.photo import Photo
from maphis.measurement.values import MatrixValue, VectorValue, ScalarValue
from maphis.project.annotation import Annotation


class AnnotationDelegate(QObject):
    def __init__(self, layer: QGraphicsItem, parent: typing.Optional[QObject]=None):
        super().__init__(parent)
        self.info = Info(self.__class__.__name__, key='.'.join(self.__module__.split('.')[:-1]))

    def set_photo(self, photo: typing.Optional[Photo]):
        pass

    def set_annotation(self, annotation: typing.Optional[Annotation]):
        pass

    @property
    def graphics_items(self) -> typing.List[QGraphicsItem]:
        return []

    def add_value(self, val: typing.Union[ScalarValue, VectorValue, MatrixValue]):
        pass

    def get_hovered_item(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        return None

    def key_press(self, ev: QKeyEvent):
        pass

    def key_release(self, ev: QKeyEvent):
        pass

    def hide_annotation(self, annotation_name: str):
        pass

    def relay_hover(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        return None
