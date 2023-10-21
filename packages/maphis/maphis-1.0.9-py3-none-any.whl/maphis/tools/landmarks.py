import csv
import importlib.resources
import importlib.resources
import json
import typing
from pathlib import Path
from typing import Optional, Union, Any, TypedDict

import PySide6.QtCore
from PySide6.QtCore import QPoint, QAbstractListModel, QObject, QModelIndex, QItemSelectionModel, QItemSelectionRange, \
    QRect, QMargins
from PySide6.QtGui import QIcon, QImage, Qt, QKeyEvent, QAction
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QListView, QWidget, QTreeView, \
    QHBoxLayout, QLabel, QComboBox, QPushButton, QVBoxLayout, QMenu, QSizePolicy
from openpyxl.workbook import Workbook

from maphis import MAPHIS_PATH
from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.tool import Tool, PaintCommand
from maphis.measurement.values import ureg
from maphis.project.annotation import KeypointAnnotation, AnnotationType, Keypoint
from maphis.project.landmark_delegate import KeypointDelegate, KeypointView, LandmarkGraphicsItem
from maphis.project.landmark_table_model import LandmarkTableModel


class _Landmark:
    def __init__(self, name: str, pos: QPoint, r: int, graphics_parent: typing.Optional[QGraphicsItem]=None):
        self.name: str = name
        self.r: int = r
        self.qg_item: QGraphicsEllipseItem = QGraphicsEllipseItem(0, 0, 2*r, 2*r, graphics_parent)
        self.qg_item.setPos(pos - QPoint(r, r))
        self.qg_item.setToolTip(self.name)

    @property
    def pos(self) -> QPoint:
        return self.qg_item.pos().toPoint() + QPoint(self.r, self.r)


_LM = TypedDict('_LM', {'name': str, 'color': typing.Tuple[int, int, int], 'deletable': bool})
_LandmarkCollection = TypedDict('_LandmarkCollection', {'collection_name': str,
                                                        'landmarks': typing.List[_LM]})


class LandmarkItemModel(QAbstractListModel):

    def __init__(self, photo: Photo, kp_ann: KeypointAnnotation, landmark_list: typing.Optional[typing.List[str]]=None,
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.photo: Photo = photo
        self.annotation: KeypointAnnotation = kp_ann

        self.annotation.new_annotation_data.connect(self._handle_new_annotation_data)
        self.annotation.modified_annotation_data.connect(self._handle_modified_annotation_data)
        self.annotation.deleted_annotation_data.connect(self._handle_deleted_annotation_data)

        self.landmark_list: typing.Optional[typing.List[str]] = landmark_list

    def _handle_new_annotation_data(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.rowCount() - 1, 0))

    def _handle_modified_annotation_data(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.rowCount() - 1, 0))

    def _handle_deleted_annotation_data(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.rowCount() - 1, 0))

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = PySide6.QtCore.QModelIndex()) -> int:
        return 1

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: Qt.ItemDataRole=Qt.ItemDataRole.DisplayRole) -> Any:
        kp = self.annotation.kps[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return kp.name
        return None

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = PySide6.QtCore.QModelIndex()) -> int:
        return len(self.annotation.kps)


class Landmarks(Tool):
    def __init__(self, state: State):
        Tool.__init__(self, state)
        self._right_click_picks_label = False
        self._tool_id = -1
        self._tool_name = 'Landmarks'
        with importlib.resources.path("maphis.tools.icons", "landmarks.png") as path:
            self._tool_icon = QIcon(str(path))

        self.keypoint_annotations: typing.List[KeypointAnnotation] = []
        self.current_annotation: typing.Optional[KeypointAnnotation] = None

        self.keypoint_delegate: typing.Optional[KeypointDelegate] = None
        self.keypoint_view: typing.Optional[KeypointView] = None

        # self.grabbed_kp_item: typing.Optional[QGraphicsItem] = None
        # self.clicked_kp_item: typing.Optional[QGraphicsItem] = None
        self.kp_item_under_cursor: typing.Optional[LandmarkGraphicsItem] = None

        self.pressed: bool = False
        self.grabbing: bool = False
        self.landmark_grab_vec: QPoint = QPoint(0, 0)

        # PLACING predefined landmarks = 1, placing custom adhoc landmarks = 0 (no effect at the moment)
        self._landmark_mode: int = 1

        self.landmark_list_widget: QListView = self._setup_landmark_list_widget()
        self.landmarks_model: typing.Optional[LandmarkItemModel] = None

        self._setup_add_landmark_collection_widget()

        self._setup_tool_widget()

        self._setup_landmark_context_menu()

        self._load_landmark_definitions()

        self._landmark_to_place: typing.Optional[Keypoint] = None

    def _setup_add_landmark_collection_widget(self):
        self._add_lm_collection_widget = QWidget()
        self._add_lm_collection_widget.setLayout(QHBoxLayout())
        layout = self._add_lm_collection_widget.layout()

        layout.addWidget(QLabel("Landmark set: "))

        self._add_lm_collection_cmbLandmarkSets = QComboBox()
        layout.addWidget(self._add_lm_collection_cmbLandmarkSets)

        self._add_lm_collection_btnAdd = QPushButton("Add")
        layout.addWidget(self._add_lm_collection_btnAdd)
        self._add_lm_collection_btnAdd.clicked.connect(self._handle_add_landmark_collection_clicked)

    def _setup_landmark_list_widget(self) -> QListView:
        lv = QListView()
        return lv

    def _setup_annotation_list_widget(self):
        return QTreeView()

    def _setup_landmark_context_menu(self):
        self._lm_context_menu = QMenu()
        self._lm_context_menu.hide()
        actDelete = self._lm_context_menu.addAction("Delete")
        actRename = self._lm_context_menu.addAction("Rename")

        actDelete.triggered.connect(lambda _: self._btnDeleteLandmark.animateClick())

    @property
    def tool_name(self) -> str:
        return self._tool_name

    @property
    def cursor_image(self) -> Optional[typing.Union[QImage, Qt.CursorShape]]:
        return Qt.CursorShape.CrossCursor

    @property
    def active(self) -> bool:
        return False

    def activate(self, viz_layer_canvas: QGraphicsItem):
        super().activate(viz_layer_canvas)
        self.keypoint_delegate = self.annotation_delegates[AnnotationType.Keypoint]
        # self.state.annotation_selected.connect(self._load_annotation)

    def deactivate(self):
        self.show_announcement.emit(self, "")
        if self.keypoint_view is not None:
            for kpitem in self.keypoint_view._keypoint_gitems:
                kpitem.setCursor(Qt.CursorShape.ArrowCursor)
        # self.state.annotation_selected.disconnect(self._load_annotation)

    def switch_to_photo(self, photo: Photo):
        self.keypoint_annotations: typing.List[KeypointAnnotation] = photo.annotations.get(AnnotationType.Keypoint, list())

        if len(self.keypoint_annotations) > 0:
            annotation = self.keypoint_annotations[0]
        else:
            annotation = KeypointAnnotation('Landmarks', 0)
            photo.insert_new_annotation(AnnotationType.Keypoint, annotation)

        self._landmark_table.setModel(None)
        self._landmark_table_model.set_landmarks(annotation)
        self._landmark_table.setModel(self._landmark_table_model)
        self._landmark_table.setSelectionMode(QListView.SelectionMode.ExtendedSelection)

        sel_model = self._landmark_table.selectionModel()
        sel_model.selectionChanged.connect(self._handle_landmark_list_item_selection_changed, Qt.ConnectionType.UniqueConnection)

        if self.current_annotation is not None:
            self.current_annotation.deleted_annotation_data.disconnect(self._enable_or_disable_deleteAllLandmarks)
            self.current_annotation.new_annotation_data.disconnect(self._enable_or_disable_deleteAllLandmarks)

        self.current_annotation = annotation
        self.keypoint_view = self.keypoint_delegate.kp_views[self.current_annotation.ann_class][self.current_annotation.ann_instance_id]
        self._btnDeleteAllLandmarks.setEnabled(self._landmark_table_model.rowCount() > 0)

        self.current_annotation.deleted_annotation_data.connect(self._enable_or_disable_deleteAllLandmarks,
                                                                Qt.ConnectionType.UniqueConnection)
        self.current_annotation.new_annotation_data.connect(self._enable_or_disable_deleteAllLandmarks, Qt.ConnectionType.UniqueConnection)

        self._populate_cmbLandmarkList()

        if self._landmark_table_model.rowCount() > 0:
            index = self._landmark_table_model.index(0, 0)
            kp: Keypoint = index.data(Qt.ItemDataRole.UserRole)
            self.select_landmark(kp)
            # self._landmark_table.selectionModel().select(index, QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def _load_annotation(self, ann: typing.Optional[KeypointAnnotation]):
        self.current_annotation = ann
        if self.current_annotation is not None:
            self.landmarks_model = LandmarkItemModel(self.state.current_photo, self.current_annotation, None)
            self.landmark_list_widget.setModel(self.landmarks_model)
            self.landmark_list_widget.setMinimumHeight(self.viz_layer_canvas.scene().views()[0].viewport().height())

            self._landmark_to_place: typing.Optional[Keypoint] = self._get_next_landmark_to_place()

    def _get_next_landmark_to_place(self) -> typing.Optional[Keypoint]:
        if self.current_annotation is None:
            return None
        kp: typing.Optional[Keypoint] = next(filter(lambda kp: kp.v < 0, self.current_annotation.kps), None)
        self._announce_next_landmark_to_place(kp)
        return kp

    def _announce_next_landmark_to_place(self, kp: typing.Optional[Keypoint]):
        if kp is not None:
            self.show_announcement.emit(self, f'Place down the "{kp.name}" landmark.')
        else:
            self.show_announcement.emit(self, "")

    def _change_cursor(self, cursor: Qt.CursorShape):
        self._cursor = cursor
        self.cursor_changed.emit(self.tool_id)

    @property
    def viz_active(self):
        return True

    def viz_hover_move(self, new_pos: QPoint, old_pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        self.kp_item_under_cursor = self.keypoint_delegate.relay_mouse_hover(new_pos)
        if self.kp_item_under_cursor is not None:
            self.kp_item_under_cursor.setCursor(Qt.CursorShape.OpenHandCursor)
        return []

    def viz_left_press(self, pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        self.pressed = True
        self._landmark_table.selectionModel().clearSelection()
        kpitem = self.keypoint_delegate.relay_left_press(pos)
        if kpitem is not None:
            kp: Keypoint = kpitem.data(2)
            self.landmark_grab_vec = QPoint(kp.x, kp.y) - pos
            self.select_landmark(kp)
        else:
            self.landmark_grab_vec = QPoint(0, 0)
        return []

    def viz_left_release(self, pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        grabbing = self.grabbing
        self.grabbing = False
        pressed = self.pressed
        self.pressed = False
        self.landmark_grab_vec = QPoint(0, 0)
        if self.current_annotation is None:
            return []
        if not grabbing:
            if self.kp_item_under_cursor is None:
                lm: _LM = self._cmbLandmarkList.currentData()
                if lm is not None:
                    color = lm['color']
                else:
                    color = (250, 192, 33)
                self.current_annotation.add_keypoint(Keypoint(self._cmbLandmarkList.currentText(), pos.x(), pos.y(), 1,
                                                              color=color))
                self.kp_item_under_cursor = self.keypoint_delegate.get_hovered_item(pos)
                kp: Keypoint = self.kp_item_under_cursor.data(2)
                self.select_landmark(kp)
            else:
                kp = self.kp_item_under_cursor.data(2)
                self.select_landmark(kp)
        self.keypoint_delegate.relay_left_release(pos)
        # if self.kp_item_under_cursor is not None:
        #     kp = self.kp_item_under_cursor.data(2)
        #     self.select_landmark(kp)
        #     self.kp_item_under_cursor.setCursor(Qt.CursorShape.OpenHandCursor)

        return []

    def select_landmark(self, kp: Keypoint):
        kp_model_indices = self._landmark_table_model.match(self._landmark_table_model.index(0, 0),
                                                            Qt.ItemDataRole.UserRole, kp, 1, Qt.MatchFlag.MatchExactly)
        if len(kp_model_indices) > 0:
            kp_model_index: QModelIndex = kp_model_indices[0]
            if kp_model_index.isValid():
                self._landmark_table.selectionModel().select(kp_model_index,
                                                             QItemSelectionModel.SelectionFlag.ClearAndSelect)
            self._btnDeleteLandmark.setEnabled(True)
            self._cmbLandmarkList.setCurrentText(kp.name)
        else:
            self._btnDeleteLandmark.setEnabled(False)

    def viz_mouse_move(self, new_pos: QPoint, old_pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        if self.pressed:
            self.grabbing = True
        if self.kp_item_under_cursor is None:
            return []
        if self.grabbing:
            kp: Keypoint = self.kp_item_under_cursor.data(2)
            self.kp_item_under_cursor.setCursor(Qt.CursorShape.BlankCursor)
            new_pos = new_pos + self.landmark_grab_vec
            # correct the new_pos so that the landmarks are always within the image domain
            corrected_x = max(0, min(new_pos.x(), self.state.current_photo.image_size[0] - 1))
            corrected_y = max(0, min(new_pos.y(), self.state.current_photo.image_size[1] - 1))
            if corrected_x != kp.x or corrected_y != kp.y:
                kp.x = corrected_x
                kp.y = corrected_y
                self.current_annotation.update_keypoint(kp)
        return []

    def viz_right_release(self, pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        released = self.keypoint_delegate.relay_right_release(pos)
        if released is not None:
            kp = released.data(2)
            self.select_landmark(kp)
            view = self.viz_layer_canvas.scene().views()[0]
            menu_placement = view.mapToGlobal(view.mapFromScene(pos))
            self._lm_context_menu.move(menu_placement)
            self._lm_context_menu.show()
        return []

    def viz_mouse_double_click(self, pos: QPoint, canvas: QImage) -> typing.List[PaintCommand]:
        return []

    def key_press(self, ev: QKeyEvent):
        pass

    def key_release(self, ev: QKeyEvent):
        current_selected_landmark_name_idx = self._cmbLandmarkList.currentIndex()
        key = ev.key()

        if key == Qt.Key.Key_Q or key == Qt.Key.Key_E:
            if key == Qt.Key.Key_Q:
                new_index = max(0, current_selected_landmark_name_idx - 1)
            elif key == Qt.Key.Key_E:
                new_index = min(current_selected_landmark_name_idx + 1, self._cmbLandmarkList.count() - 1)
            else:
                new_index = current_selected_landmark_name_idx
            self._cmbLandmarkList.setCurrentIndex(new_index)
        elif key == Qt.Key.Key_Delete:
            self._btnDeleteLandmark.animateClick()

    def handle_graphics_view_changed(self):
        pass

    def left_side_panel_widget(self) -> typing.Optional[QWidget]:
        return None

    def _load_landmark_definitions(self):
        self._landmark_collections: typing.List[_LandmarkCollection] = []
        for lm_path in (MAPHIS_PATH / 'plugins/maphis/project_types').glob('*_landmarks.json'):
            with open(lm_path) as f:
                _lm_collection: _LandmarkCollection = json.load(f)
                self._landmark_collections.append(_lm_collection)

                self._add_lm_collection_cmbLandmarkSets.addItem(_lm_collection['collection_name'],
                                                                userData=_lm_collection)

                self._cmbLandmarkCollections.addItem(_lm_collection['collection_name'],
                                                     userData=_lm_collection)

    def _handle_add_landmark_collection_clicked(self):
        lm_collection: typing.Optional[_LandmarkCollection] = self._add_lm_collection_cmbLandmarkSets.currentData()
        if lm_collection is None:
            return
        annotation = KeypointAnnotation(lm_collection['collection_name'], -1)
        self.state.current_photo.insert_new_annotation(AnnotationType.Keypoint, annotation)
        for lm in lm_collection['landmarks']:
            annotation.add_keypoint(Keypoint(lm['name'], -1, -1, -1, lm['deletable']))
        self._load_annotation(annotation)

    def _setup_tool_widget(self):
        widget_layout = QVBoxLayout()
        self._tool_widget = QWidget()
        self._tool_widget.setLayout(widget_layout)

        layout = QHBoxLayout()

        # Widget section for choosing the current landmark class
        # It is a QComboBox, with the landmark names from the loaded landmark collection. Might be empty if the user
        # chose the <Empty collection> option. It is editable to allow renaming landmarks to custom names.

        self._cmbLandmarkList = QComboBox()
        self._cmbLandmarkList.setEditable(True)
        self._cmbLandmarkList.currentTextChanged.connect(self._rename_current_landmark)
        self._cmbLandmarkList.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self._cmbLandmarkList)

        # Widget section for loading landmark collection
        # It is a QComboBox, where the first option is an <Empty collection> and other options are loaded
        # from landmark collection files

        self._cmbLandmarkCollections = QComboBox()
        self._cmbLandmarkCollections.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._cmbLandmarkCollections.addItem("<Empty collection>", userData=None)
        self._cmbLandmarkCollections.currentIndexChanged.connect(lambda _: self._populate_cmbLandmarkList())
        layout.addWidget(self._cmbLandmarkCollections)

        widget_layout.addLayout(layout)

        # Widget section for displaying present landmarks for the current photo
        # It is a QTableView that uses as a model the LandmarkTableModel

        self._landmark_table = QListView()
        # self._landmark_table.activated.connect(self._handle_landmark_list_item_activated)
        self._landmark_table.pressed.connect(self._handle_landmark_list_item_pressed)

        self._landmark_table_model = LandmarkTableModel()
        self._landmark_table.setModel(self._landmark_table_model)

        widget_layout.addWidget(self._landmark_table)

        layout = QHBoxLayout()
        self._btnDeleteLandmark = QPushButton("Delete selected")
        self._btnDeleteLandmark.setEnabled(False)
        self._btnDeleteLandmark.clicked.connect(self._delete_selected_landmarks)
        layout.addWidget(self._btnDeleteLandmark)

        self._btnDeleteAllLandmarks = QPushButton("Delete all")
        self._btnDeleteAllLandmarks.clicked.connect(self._delete_all_landmarks)
        self._btnDeleteAllLandmarks.setEnabled(False)
        layout.addWidget(self._btnDeleteAllLandmarks)
        widget_layout.addLayout(layout)

        # layout = QHBoxLayout()
        # self._btnExportAll = QPushButton("Export landmarks from all photos")
        #
        # self._exportMenu = QMenu()
        # self._exportMenu.triggered.connect(self._export_landmarks)
        # action = self._exportMenu.addAction("to XLSX")
        # action.setData(0)
        #
        # action = self._exportMenu.addAction("to CSV")
        # action.setData(1)
        #
        # self._btnExportAll.setMenu(self._exportMenu)
        #
        # layout.addWidget(self._btnExportAll)
        # widget_layout.addLayout(layout)

    def _delete_selected_landmarks(self):
        selected_landmark_indexes = self._landmark_table.selectedIndexes()
        indexes_sorted_row_desc = sorted(self._landmark_table.selectedIndexes(), key=lambda k: k.row(), reverse=True)
        for lm_index in indexes_sorted_row_desc:
            # self.current_annotation.delete_keypoint(lm_index.data(Qt.ItemDataRole.UserRole))
            self._landmark_table_model.removeRow(lm_index.row(), lm_index.parent())

    def _delete_all_landmarks(self):
        self._landmark_table_model.removeRows(0, self._landmark_table_model.rowCount())

    def _populate_cmbLandmarkList(self):
        current_landmark_name: str = self._cmbLandmarkList.currentText()

        self._cmbLandmarkList.blockSignals(True)

        lm_collection: typing.Optional[_LandmarkCollection] = self._cmbLandmarkCollections.currentData()
        self._cmbLandmarkList.clear()

        if lm_collection is None:
            lm_names: typing.List[str] = []
        else:
            lm_names: typing.List[str] = [lm['name'] for lm in lm_collection['landmarks']]

        placed_lm_names = {kp.name for kp in self.keypoint_view.keypoint_to_gitem.keys()}
        placed_lm_names.difference_update(lm_names)

        lm_names.extend(sorted(placed_lm_names))

        for lm_name in lm_names:
            self._cmbLandmarkList.addItem(lm_name)

        if len(current_landmark_name) > 0:
            self._cmbLandmarkList.setCurrentText(current_landmark_name)
        self._cmbLandmarkList.blockSignals(False)

    def _rename_current_landmark(self, lm_name: str):
        for sel_idx in self._landmark_table.selectedIndexes():
            kp: Keypoint = sel_idx.data(Qt.ItemDataRole.UserRole)
            kp.name = lm_name
            self.current_annotation.update_keypoint(kp)

    def _handle_landmark_list_item_activated(self, index: QModelIndex, _: QModelIndex = QModelIndex()):
        lm: Keypoint = index.data(Qt.ItemDataRole.UserRole)
        kvs: typing.Dict[int, KeypointView] = self.keypoint_delegate.kp_views[self.current_annotation.ann_class]
        kv: KeypointView = kvs[self.current_annotation.ann_instance_id]
        kv.select_keypoint(lm, True)
        self._btnDeleteLandmark.setEnabled(index.isValid())

    def _handle_landmark_list_item_selection_changed(self, selected: QItemSelectionRange,
                                                     deselected: QItemSelectionRange):
        for des in deselected.indexes():
            kp = des.data(Qt.ItemDataRole.UserRole)
            self.keypoint_view.select_keypoint(kp, False)
        top, left, bottom, right = 9999, 9999, -1, -1
        for sel in self._landmark_table.selectedIndexes():
            kp = sel.data(Qt.ItemDataRole.UserRole)
            self.keypoint_view.select_keypoint(kp, True)
            kp_item = self.keypoint_view.keypoint_to_gitem[kp]
            brect = kp_item.sceneBoundingRect()

            top, left = min(top, brect.top()), min(left, brect.left())
            bottom, right = max(bottom, brect.bottom()), max(right, brect.right())
        if len(selected.indexes()) > 0:
            self._btnDeleteLandmark.setEnabled(True)
            self._landmark_table.scrollTo(selected.indexes()[0])
            if len(selected.indexes()) == 1:
                kp: Keypoint = selected.indexes()[0].data(Qt.ItemDataRole.UserRole)
                self._cmbLandmarkList.setCurrentText(kp.name)
        else:
            self._btnDeleteLandmark.setEnabled(False)
            return
        viewport_rect = self.viz_layer_canvas.scene().views()[0].rect()
        visualized_rect = self.viz_layer_canvas.scene().views()[0].mapToScene(viewport_rect).boundingRect()
        srect = QRect(left, top, right - left, bottom - top)
        srect = self.viz_layer_canvas.mapRectToScene(srect)
        if not visualized_rect.contains(srect):
            srect = srect.marginsAdded(QMargins(200, 200, 200, 200))
            srect = self.viz_layer_canvas.sceneBoundingRect().intersected(srect)
            self.viz_layer_canvas.scene().views()[0].fitInView(srect, Qt.AspectRatioMode.KeepAspectRatio)

    def _handle_landmark_list_item_pressed(self, index: QModelIndex):
        kp: Keypoint = index.data(Qt.ItemDataRole.UserRole)
        kp_item = self.keypoint_view.keypoint_to_gitem[kp]

        self._cmbLandmarkList.setCurrentText(kp.name)
        self.viz_layer_canvas.scene().views()[0].ensureVisible(kp_item)

    def _enable_or_disable_deleteAllLandmarks(self, _: KeypointAnnotation, _dict: typing.Dict[str, typing.Any]):
        self._btnDeleteAllLandmarks.setEnabled(len(self.current_annotation.kps) > 0)

    def _export_landmarks_csv(self, fpath: Path):
        with open(fpath, 'w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ['image_name', 'landmark_name', 'x (px)', 'y (px)', 'x (mm)', 'y (mm)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for photo in self.state.project.storage.images:
                lm_annotations: typing.List[KeypointAnnotation] = photo.get_annotations(AnnotationType.Keypoint)
                if len(lm_annotations) == 0:
                    continue
                for annotation in lm_annotations:
                    for kp in annotation.kps:
                        real_kp = get_landmark_in_real_units(kp, photo)
                        writer.writerow({'image_name': photo.image_name,
                                         'landmark_name': kp.name,
                                         'x (px)': kp.x,
                                         'y (px)': kp.y,
                                         'x (mm)': real_kp.x,
                                         'y (mm)': real_kp.y})

    def _export_landmarks_xlsx(self, fpath: Path):
        wb = Workbook()
        ws = wb.active

        ws.append(['image_name', 'landmark_name', 'x (px)', 'y (px)', 'x (mm)', 'y (mm)'])

        for photo in self.state.project.storage.images:
            lm_annotations: typing.List[KeypointAnnotation] = photo.get_annotations(AnnotationType.Keypoint)
            if len(lm_annotations) == 0:
                continue
            for annotation in lm_annotations:
                for kp in annotation.kps:
                    real_kp = get_landmark_in_real_units(kp, photo)
                    ws.append((photo.image_name, kp.name, kp.x, kp.y, real_kp.x, real_kp.y))
        wb.save(fpath)

    def _export_landmarks(self, action: QAction):
        if action.data() == 0:
            self._export_landmarks_xlsx(self.state.project.folder / 'landmarks.xlsx')
        else:
            self._export_landmarks_csv(self.state.project.folder / 'landmarks.csv')

    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        return self._tool_widget


def get_landmark_in_real_units(kp: Keypoint, photo: Photo) -> Keypoint:
    if photo.image_scale is None:
        return Keypoint(kp.name)
    return Keypoint(kp.name,
                    x=(ureg.Quantity(kp.x, 'pixel') / photo.image_scale).to('mm').magnitude,
                    y=(ureg.Quantity(kp.y, 'pixel') / photo.image_scale).to('mm').magnitude)