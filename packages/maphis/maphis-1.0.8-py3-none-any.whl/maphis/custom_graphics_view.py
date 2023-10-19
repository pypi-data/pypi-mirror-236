import time
import typing
from enum import IntEnum

import PySide6
import mouse
from PySide6.QtCore import Signal, QPointF, Qt, QEvent, QPoint
from PySide6.QtGui import QPainter, QWheelEvent, QResizeEvent, QMouseEvent, QKeyEvent
from PySide6.QtWidgets import QGraphicsView, QWidget, QSizePolicy, QScrollArea, QToolButton, QVBoxLayout, QHBoxLayout


class Side(IntEnum):
    Left = 0
    Right = 1


class SidePanel(QWidget):
    def __init__(self, side: Side, parent: QWidget):
        super().__init__(parent)

        self._side: Side = side

        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.panel_widget: QScrollArea = QScrollArea()
        self.panel_widget.setLayout(QVBoxLayout())
        self.panel_widget.layout().setContentsMargins(0, 0, 0, 0)

        self.toggle_button: QToolButton = QToolButton()
        self.toggle_button.setText('<' if self._side == Side.Left else '>')
        self.toggle_button.clicked.connect(self._handle_toggle_button_clicked)

        self._shown: bool = True

        if self._side == Side.Left:
            self.layout.addWidget(self.panel_widget)
            self.layout.addWidget(self.toggle_button)
        else:
            self.layout.addWidget(self.toggle_button)
            self.layout.addWidget(self.panel_widget)

        self.set_widget(None)

    def _handle_toggle_button_clicked(self):
        self._shown = not self._shown
        if self._shown:
            self.toggle_button.setText('<')
            self.panel_widget.show()
        else:
            self.toggle_button.setText('>')
            self.panel_widget.hide()

    def clear_panel(self):
        for i in range(self.panel_widget.layout().count()):
            widg = self.panel_widget.layout().itemAt(0).widget()
            self.panel_widget.layout().removeWidget(widg)
            widg.setVisible(False)

    def set_widget(self, widget: typing.Optional[QWidget]):
        self.clear_panel()
        if widget is not None:
            self.panel_widget.layout().addWidget(widget)
            self.show()
        else:
            self.hide()


class CustomGraphicsView(QGraphicsView):

    view_changed = Signal()
    rubber_band_started = Signal()
    mouse_move = Signal(QPointF)
    view_dragging = Signal(bool, QPoint)
    double_shift = Signal()
    escape_pressed = Signal()
    space_pressed = Signal()
    tab_pressed = Signal()

    def __init__(self, parent: QWidget = None):
        self.left_side_panel: typing.Optional[SidePanel] = None
        self.right_side_panel: typing.Optional[SidePanel] = None
        QGraphicsView.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setInteractive(True)

        self.verticalScrollBar().valueChanged.connect(lambda _: self.view_changed.emit())
        self.horizontalScrollBar().valueChanged.connect(lambda _: self.view_changed.emit())
        self.time_of_first_shift = -1
        self._allow_zoom: bool = True

        self._autoscroll_with_left_btn_released: bool = False
        self._autoscroll_distance: int = 64
        self._autoscroll_enabled: bool = False

        self.hb = QHBoxLayout(self)
        self.hb.setContentsMargins(0, 0, 0, 0)
        self.left_side_panel: typing.Optional[SidePanel] = SidePanel(Side.Left, None)
        self.right_side_panel: typing.Optional[SidePanel] = SidePanel(Side.Right, None)
        self.hb.addWidget(self.left_side_panel)
        self.hb.addStretch()
        self.hb.addWidget(self.right_side_panel)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & Qt.ControlModifier != Qt.KeyboardModifier.NoModifier:
            # self.state.key_modifier = Qt.Key_Control
            QGraphicsView.wheelEvent(self, event)
            return
        else:
            pass
            # self.state.key_modifier = None
        if event.modifiers() & Qt.ShiftModifier != Qt.KeyboardModifier.NoModifier:
            QGraphicsView.wheelEvent(self, event)
            return

        delta = 1
        if event.angleDelta().y() < 0:
            delta = -1

        m = self.transform()
        m11 = m.m11() * (1 + delta * 0.05)
        m31 = 0
        m22 = m.m22() * (1 + delta * 0.05)
        m32 = 0

        m.setMatrix(m11, m.m12(), m.m13(), m.m21(), m22, m.m23(),
                    m.m31() + m31, m.m32() + m32, m.m33())
        self.setTransform(m, False)
        srect = self.sceneRect()
        rrect = self.mapToScene(self.rect()).boundingRect()
        if delta < 0 and rrect.height() > srect.height() and rrect.width() > srect.width():
            self.fitInView(srect, Qt.KeepAspectRatio)
        self.scene().update()
        self.view_changed.emit()

    def resizeEvent(self, event: QResizeEvent):
        self.view_changed.emit()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.viewport().setCursor(Qt.ClosedHandCursor)
            self.original_event = event
            handmade_event = QMouseEvent(QEvent.MouseButtonPress, QPointF(event.pos()), Qt.LeftButton, event.buttons(),
                                         Qt.KeyboardModifiers())
            self.view_dragging.emit(True, self.mapToScene(event.pos()))
            self.mousePressEvent(handmade_event)
            return None
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            pass
        elif event.button() == Qt.MouseButton.LeftButton:
            pass
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.viewport().setCursor(Qt.OpenHandCursor)
            handmade_event = QMouseEvent(QEvent.MouseButtonRelease, QPointF(event.pos()), Qt.MouseButton.LeftButton,
                                         event.buttons(), Qt.KeyboardModifiers())
            self.mouseReleaseEvent(handmade_event)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.view_dragging.emit(False, self.mapToScene(event.pos()))
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouse_move.emit(self.mapToScene(event.pos()))
        QGraphicsView.mouseMoveEvent(self, event)

        # Auto scrolling near viewport edges.
        if (event.buttons() & Qt.MouseButton.LeftButton) and self._autoscroll_enabled:
            auto_scroll_edge_width = min(self._autoscroll_distance, self.width() / 3, self.height() / 3)
            # Auto scroll left.
            displacement = int(auto_scroll_edge_width - event.pos().x())
            if self.horizontalScrollBar().value() > 0 and displacement > 0:
                mouse.move(displacement, 0, False)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - displacement)
            # Auto scroll up.
            displacement = int(auto_scroll_edge_width - event.pos().y())
            if self.verticalScrollBar().value() > 0 and displacement > 0:
                mouse.move(0, displacement, False)
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - displacement)
            # Auto scroll right.
            displacement = int(self.viewport().width() - auto_scroll_edge_width - event.pos().x())
            if self.horizontalScrollBar().value() < self.horizontalScrollBar().maximum() and displacement < 0:
                mouse.move(displacement, 0, False)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - displacement)
            # Auto scroll down.
            displacement = int(self.viewport().height() - auto_scroll_edge_width - event.pos().y())
            if self.verticalScrollBar().value() < self.verticalScrollBar().maximum() and displacement < 0:
                mouse.move(0, displacement, False)
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - displacement)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Control:
            # self.setDragMode(QGraphicsView.ScrollHandDrag)
            pass
        elif event.key() == Qt.Key.Key_Shift:
            self.rubber_band_started.emit()
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)
        QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Control or event.key() == Qt.Key.Key_Shift:
            # self.setDragMode(QGraphicsView.NoDrag)
            if self.time_of_first_shift < 0:
                self.time_of_first_shift = time.time() * 1000
            else:
                if 1000 * time.time() - self.time_of_first_shift < 500:
                    self.double_shift.emit()
                    self._allow_zoom = False
                self.time_of_first_shift = -1
        if event.key() == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
            self._allow_zoom = True
        elif event.key() == Qt.Key.Key_Space:
            self.space_pressed.emit()
        elif event.key() == Qt.Key.Key_Tab:
            self.tab_pressed.emit()
        QGraphicsView.keyReleaseEvent(self, event)

    def should_autoscroll_with_left_button_released(self) -> bool:
        return self._autoscroll_with_left_btn_released

    def set_autoscroll_with_left_button_released(self, autoscroll: bool):
        self._autoscroll_with_left_btn_released = autoscroll

    def autoscroll_distance(self) -> int:
        return self._autoscroll_distance

    def set_autoscroll_distance(self, distance: int):
        self._autoscroll_distance = distance

    def should_autoscroll(self) -> bool:
        return self._autoscroll_enabled

    def set_should_autoscroll(self, enabled: bool):
        self._autoscroll_enabled = enabled

    def viewportEvent(self, event: PySide6.QtCore.QEvent) -> bool:
        if self.left_side_panel is not None:
            self.left_side_panel.setMaximumWidth(round(0.1 * self.viewport().width()))
            self.right_side_panel.setMaximumWidth(round(0.1 * self.viewport().width()))
        return super().viewportEvent(event)

    # def allow_zoom(self, allow: bool):
    #     self._allow_zoom = allow
    #     self.horizontalScrollBar().setEnabled(allow)
    #     self.verticalScrollBar().setEnabled(allow)
