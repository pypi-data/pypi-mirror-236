import typing

from PySide6.QtCore import QPoint, QObject
from PySide6.QtGui import QColor, Qt, QPen, QBrush, QPainter
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsSceneMouseEvent, \
    QGraphicsSceneHoverEvent, QWidget, QStyleOptionGraphicsItem

from maphis.common.photo import Photo
from maphis.project.annotation import KeypointAnnotation, AnnotationType, Keypoint
from maphis.project.annotation_delegate import AnnotationDelegate


class LandmarkGraphicsItem(QGraphicsEllipseItem):
    selected_pen = QPen(QColor(0, 100, 230), 2.5)
    normal_pen = QPen(QColor(0, 0, 0), 1.0)

    hovered_brush = QBrush(QColor(0, 210, 0, 100))
    normal_brush = QBrush(QColor(QColor(250, 192, 33, 100)))

    def __init__(self, lm: Keypoint, x: int, y: int, w: int, h: int, **kwargs) -> None:
        super().__init__(0, 0, w, h, **kwargs)
        self.lm: Keypoint = lm
        self.r = h // 2
        self.setTransformOriginPoint(self.r, self.r)
        self.setPos(x, y)
        self.name_item: QGraphicsSimpleTextItem = QGraphicsSimpleTextItem(lm.name, self)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.name_item.setPos(10, -10)
        self.name_item.setBrush(QColor(0, 0, 0))

        self.setPen(self.normal_pen)
        # self.setBrush(self.normal_brush)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.is_selected: bool = False
        self.normal_color: QColor = QColor.fromRgb(*self.lm.color, 100)
        self.setBrush(self.normal_color)

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setScale(1.2)
            self.setBrush(self.hovered_brush)
        else:
            self.setScale(1.0)
            self.setBrush(self.normal_color)
        self.is_selected = selected

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            pass
        return super().itemChange(change, value)

    def set_hovered(self, hovered: bool):
        if self.is_selected:
            return
        if hovered:
            self.setBrush(self.hovered_brush)
        else:
            self.setBrush(self.normal_color)

    def set_clicked(self, clicked: bool):
        pass

    def set_selected(self, selected: bool):
        self.setSelected(selected)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: typing.Optional[QWidget] = None) -> None:
        super().paint(painter, option, widget)
        painter.save()
        painter.drawPoint(QPoint(self.r, self.r))
        painter.restore()


class KeypointView:
    def __init__(self, keypoint_ann: KeypointAnnotation, layer: QGraphicsItem, color: QColor):
        self._layer: QGraphicsItem = layer
        self.ann: KeypointAnnotation = keypoint_ann
        self.ann.new_annotation_data.connect(self._handle_new_keypoint_added)
        self.ann.modified_annotation_data.connect(self._handle_update_keypoint)
        self.ann.deleted_annotation_data.connect(self._handle_deleted_keypoint)
        self._keypoint_gitems: typing.List[LandmarkGraphicsItem] = []
        self.keypoint_to_gitem: typing.Dict[Keypoint, LandmarkGraphicsItem] = {}
        self.color: QColor = color
        self.hovered_color: QColor = QColor(0, 210, 0)
        self.is_visible: bool = True

        self._init()

    def _handle_new_keypoint_added(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self._create_kp_gitem(_dict['kp'])

    def _handle_update_keypoint(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        kp_idx = _dict['kp_index']
        kp: Keypoint = _dict['kp']
        gitem = self._keypoint_gitems[kp_idx]
        gitem.setPos(kp.x-5, kp.y-5)
        gitem.setVisible(kp.v >= 0)
        gitem.name_item.setText(kp.name)

    def _handle_deleted_keypoint(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        kp_idx = _dict['kp_index']
        for i in range(kp_idx + 1, len(self._keypoint_gitems)):
            self._keypoint_gitems[i].setData(0, i - 1)
        gitem = self._keypoint_gitems.pop(kp_idx)
        gitem.hide()
        gitem.setParentItem(None)
        del self.keypoint_to_gitem[_dict['kp']]

    def _create_kp_gitem(self, kp: Keypoint):
        idx = len(self._keypoint_gitems)
        gitem = LandmarkGraphicsItem(kp, kp.x-5, kp.y-5, 10, 10, parent=self._layer)
        gitem.setData(0, idx)
        gitem.setData(1, kp.name)
        gitem.setData(2, kp)
        gitem.setData(3, self.ann)
        # gitem.setToolTip(f'{kp.name} ({self.ann.instance_name})')
        # gitem.setCursor(Qt.CursorShape.OpenHandCursor)
        gitem.setVisible(kp.v >= 0)
        gitem.setZValue(999)
        self._keypoint_gitems.append(gitem)
        self.keypoint_to_gitem[kp] = gitem

    def _init(self):
        for kp in self.ann.kps:
            self._create_kp_gitem(kp)

    def destroy_view(self):
        for gitem in self._keypoint_gitems:
            gitem.hide()
            gitem.setParentItem(None)

    def hover(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        for _gitem in self._keypoint_gitems:
            _gitem.set_hovered(False)
        for gitem in self._keypoint_gitems:
            _pos = gitem.mapFromParent(pos)
            kp: Keypoint = gitem.data(2)
            if kp.v >= 0 and gitem.contains(_pos):
                gitem.set_hovered(True)
                return gitem

    def left_press(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        pressed = self.hover(pos)
        if pressed is not None:
            pressed.setCursor(Qt.CursorShape.ClosedHandCursor)
        return pressed

    def left_release(self, pos: QPoint):
        released = self.hover(pos)
        if released is not None:
            released.setCursor(Qt.CursorShape.OpenHandCursor)
        return released

    def right_press(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        return self.hover(pos)

    def right_release(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        return self.hover(pos)

    def set_visible(self, visible: bool):
        self.is_visible = visible
        for gitem in self._keypoint_gitems:
            gitem_visible = gitem.data(2).v >= 0
            gitem.setVisible(gitem_visible and visible)
            gitem.setZValue(999)

    def select_keypoint(self, kp: typing.Optional[Keypoint], select: bool):
        # for gitem in self._keypoint_gitems:
        #     gitem.set_selected(False)
        if kp not in self.keypoint_to_gitem or kp is None:
            return
        self.keypoint_to_gitem[kp].set_selected(select)


class KeypointDelegate(AnnotationDelegate):
    def __init__(self, layer: QGraphicsItem, parent: typing.Optional[QObject]=None):
        super().__init__(layer, parent)

        self._layer: QGraphicsItem = layer

        self.photo: typing.Optional[Photo] = None
        self.kp_views: typing.Dict[str, typing.Dict[int, KeypointView]] = {}

    def set_photo(self, photo: typing.Optional[Photo]):
        if self.photo is not None:
            self.photo.new_annotation_added.disconnect(self._handle_new_annotation_added)
        self.photo = photo

        for ann_class, ann_instance_dicts in self.kp_views.items():
            for ann_view in ann_instance_dicts.values():
                ann_view.destroy_view()
        self.kp_views.clear()

        if self.photo is not None:
            self.photo.new_annotation_added.connect(self._handle_new_annotation_added)
            kp_anns: typing.List[KeypointAnnotation] = photo.get_annotations(AnnotationType.Keypoint)
            if len(kp_anns) > 0:
                for i, kp_ann in enumerate(kp_anns):
                    self._handle_new_annotation_added(i, kp_ann)

    def _handle_new_annotation_added(self, idx: int, kp_ann: KeypointAnnotation):
        ann_class = kp_ann.ann_class
        ann_class_views: typing.Dict[int, KeypointView] = self.kp_views.setdefault(ann_class, dict())
        ann_class_views[kp_ann.ann_instance_id] = KeypointView(kp_ann, self._layer, color=QColor(250, 192, 33))

    def set_annotation_visible(self, annotation_name: str, instance_name: str='', visible: bool=True):
        if annotation_name not in self.kp_views.keys():
            return
        for kp_view in self.kp_views[annotation_name].values():
            if instance_name == '' or kp_view.ann.instance_name == instance_name:
                kp_view.set_visible(visible)

    def relay_mouse_hover(self, pos: QPoint) -> typing.Optional[LandmarkGraphicsItem]:
        for kpv_dics in self.kp_views.values():
            for kpv in kpv_dics.values():
                if kpv.is_visible:
                    if (gitem := kpv.hover(pos)) is not None:
                        return gitem

    def relay_left_press(self, pos: QPoint) -> typing.Optional[LandmarkGraphicsItem]:
        for kpv_dics in self.kp_views.values():
            for kpv in kpv_dics.values():
                if kpv.is_visible:
                    if (gitem := kpv.left_press(pos)) is not None:
                        return gitem

    def relay_left_release(self, pos: QPoint) -> typing.Optional[LandmarkGraphicsItem]:
        for kpv_dics in self.kp_views.values():
            for kpv in kpv_dics.values():
                if kpv.is_visible:
                    if (gitem := kpv.left_release(pos)) is not None:
                        return gitem

    def relay_right_press(self, pos: QPoint) -> typing.Optional[LandmarkGraphicsItem]:
        for kpv_dics in self.kp_views.values():
            for kpv in kpv_dics.values():
                if kpv.is_visible:
                    if (gitem := kpv.right_press(pos)) is not None:
                        return gitem

    def relay_right_release(self, pos: QPoint) -> typing.Optional[LandmarkGraphicsItem]:
        for kpv_dics in self.kp_views.values():
            for kpv in kpv_dics.values():
                if kpv.is_visible:
                    if (gitem := kpv.right_release(pos)) is not None:
                        return gitem

    def get_hovered_item(self, pos: QPoint) -> typing.Optional[QGraphicsItem]:
        return self.relay_mouse_hover(pos)



