import copy
import dataclasses
import logging
import math
import re
import typing
from pathlib import Path

import PySide6
import cv2
import numpy as np
import pint

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, Signal, QPoint, QObject, QRect, QModelIndex
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton, QComboBox, QDoubleSpinBox, QDialog, \
    QDialogButtonBox, QVBoxLayout, QStyleOptionViewItem, QGroupBox, QMessageBox

from maphis import qimage2ndarray
from maphis.common.blocking_operation import BlockingOperation
from maphis.common.image_operation_binding import ImageOperation
from maphis.common.message_widget import MessageWidget
from maphis.common.photo import Photo, UpdateEvent, PhotoUpdate, PhotoUpdateType
from maphis.image_list_model import ImageListSortFilterProxyModel
from maphis.layers.photo_layer import PhotoLayer
from maphis.common.state import State
from maphis.common.storage import Storage, StorageUpdate
from maphis.common.utils import ScaleSetting, ScaleLineInfo, get_scale_marker_roi, get_reference_length, \
    get_scale_line_ends
from maphis.layers.visualization_layer import VisualizationLayer
from maphis.image_viewer import ImageViewer
from maphis.thumbnail_storage import ThumbnailDelegate, ThumbnailStorage_
from maphis.tools.ruler import Tool_Ruler
from maphis.measurement.values import ureg, ScalarValue


@dataclasses.dataclass
class ScaleExtractionResult:
    photo_idx: int
    image_scale: pint.Quantity
    reference_length: pint.Quantity
    px_length: pint.Quantity
    scale_line_p1: typing.Tuple[int, int]
    scale_line_p2: typing.Tuple[int, int]
    scale_marker: typing.Optional[np.ndarray]
    scale_marker_bbox: typing.Optional[typing.Tuple[int, int, int, int]]


@dataclasses.dataclass
class ScaleSettingTuple:
    old_scale_set: ScaleSetting
    new_scale_set: ScaleSetting


class ScaleSettingWidget(QWidget):
    scale_set = Signal(list)
    accepted = Signal(list)
    cancelled = Signal()

    def __init__(self, state: State, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self.state = state
        # self._state = self.state
        self.photo: typing.Optional[Photo] = None
        # self._storage: typing.Optional[Storage] = None
        self.photo_model: typing.Optional[ImageListSortFilterProxyModel] = None

        self.units = ureg
        self.line_length: typing.Optional[pint.Quantity] = None
        self.scale: typing.Optional[pint.Quantity] = None

        self.ref_length_units: typing.List[pint.Unit] = [
            ureg['nanometer'].units,
            ureg['micrometer'].units,
            ureg['millimeter'].units,
            ureg['centimeter'].units,
            ureg['decimeter'].units
        ]

        self._scale_not_found_photo_names: typing.List[str] = []

        self._setup_controls()
        self._setup_viewer()

        self.image_op: ImageOperation = ImageOperation(self)

        self.scale_settings: typing.Dict[Path, ScaleSettingTuple] = {}
        self.setWindowTitle('Set scale')
        self.setWindowModality(Qt.ApplicationModal)

    def _setup_controls(self):
        self._layout = QHBoxLayout()

        self._ref_label = QLabel("Reference length: ")

        self._spboxReference_mm = QSpinBox()
        self._spboxReference_mm.setMinimum(1)
        self._spboxReference_mm.setMaximum(9999)
        self._spboxReference_mm.setMaximumWidth(150)
        self._spboxReference_mm.setAlignment(Qt.AlignLeft)
        self._spboxReference_mm.valueChanged.connect(self._new_reference_length)

        self._cmbUnits = QComboBox()
        self._cmbResUnits = QComboBox()
        default_idx = 0
        # for i, prefix in enumerate(list(SIPrefix)):
        #     unit = Unit(BaseUnit.m, prefix=prefix, dim=1)
        #     self._cmbUnits.addItem(str(unit), unit)
        #     self._cmbResUnits.addItem(str(unit), unit)
        #     if prefix == SIPrefix.m:
        #         default_idx = i
        for i, unit in enumerate(self.ref_length_units):
            self._cmbUnits.addItem(f'{unit:~P}', unit)
            self._cmbResUnits.addItem(f'{unit:~P}', unit)
            if unit == ureg('millimeter'):
                default_idx = i
        self._cmbUnits.setCurrentIndex(default_idx)
        self._cmbUnits.currentIndexChanged.connect(self._handle_reference_unit_changed)

        self._lblPixels = QLabel(f'Line length: {0 * ureg["pixel"]}')
        self._lblResolution = QLabel('Scale:')

        self._lblScaleValue = QLabel()

        self._groupAutoScaleExtraction = QGroupBox("Automatic scale extraction from markers")
        self._groupAutoScaleExtraction.setLayout(QHBoxLayout())

        self._btnExtractScalesAllPhotos = QPushButton(text="Apply to all selected photos")
        self._btnExtractScalesAllPhotos.clicked.connect(lambda _: self.extract_scale_for_all())

        self._btnExtractScalesCurrentPhoto = QPushButton(text="Apply to this photo")
        self._btnExtractScalesCurrentPhoto.clicked.connect(lambda _: self.extract_scale_for_current())

        self._groupAutoScaleExtraction.layout().addWidget(self._btnExtractScalesCurrentPhoto)
        self._groupAutoScaleExtraction.layout().addWidget(self._btnExtractScalesAllPhotos)

        self._btnSetManually = QPushButton(text="Enter scale numerically")
        self._btnSetManually.clicked.connect(self._get_scale_from_user)

        self._btnAcceptAll = QPushButton(text="Accept changes for all selected photos")
        self._btnAcceptAll.clicked.connect(self.accept_changes_all)
        self._btnAcceptAll.setEnabled(True)

        self._btnAcceptCurrent = QPushButton(text="Accept changes for this photo")
        self._btnAcceptCurrent.clicked.connect(self.accept_changes_current)
        self._btnAcceptCurrent.setEnabled(True)

        self._btnResolutionGlobal = QPushButton()
        self._btnResolutionGlobal.setText("Assign scale value to all selected photos")
        self._btnResolutionGlobal.clicked.connect(self._set_global_resolution)
        self._btnResolutionGlobal.setEnabled(True)

        self._btnCancel = QPushButton(text="Cancel")
        self._btnCancel.clicked.connect(self.cancelled.emit)
        self._btnCancel.setEnabled(True)

        self._groupScaleInfo = QGroupBox("Scale info")
        self._groupScaleInfo.setLayout(QHBoxLayout())

        self._groupScaleInfo.layout().setSpacing(2)
        self._groupScaleInfo.layout().addWidget(self._ref_label)
        self._groupScaleInfo.layout().addWidget(self._spboxReference_mm)
        self._groupScaleInfo.layout().addWidget(self._cmbUnits)
        _lay: QHBoxLayout = self._groupScaleInfo.layout()
        _lay.addSpacing(20)
        self._groupScaleInfo.layout().addWidget(self._lblPixels)
        _lay.addSpacing(20)
        self._groupScaleInfo.layout().addWidget(self._lblResolution)
        self._groupScaleInfo.layout().addWidget(self._lblScaleValue)
        self._groupScaleInfo.layout().addWidget(self._btnSetManually)
        self._groupScaleInfo.layout().addWidget(self._btnResolutionGlobal)

        self._layout.setSpacing(5)
        self._layout.addWidget(self._groupScaleInfo)
        self._layout.addWidget(self._groupAutoScaleExtraction)
        self._layout.addStretch()
        self._layout.addWidget(self._btnAcceptCurrent)
        self._layout.addWidget(self._btnAcceptAll)
        # self._layout.addWidget(self._btnResolutionGlobal)
        self._layout.addWidget(self._btnCancel)

    def _setup_viewer(self):
        self.image_viewer = ImageViewer(self.state)

        self.image_viewer.first_photo_requested.connect(self._fetch_first_photo)
        self.image_viewer.prev_photo_requested.connect(self._fetch_prev_photo)
        self.image_viewer.next_photo_requested.connect(self._fetch_next_photo)
        self.image_viewer.last_photo_requested.connect(self._fetch_last_photo)
        self.image_viewer.ui.tbtnRotateCW.hide()
        self.image_viewer.ui.tbtnRotateCCW.hide()

        self.image_viewer.rotate_cw_requested.connect(lambda: self.image_op.rotate(clockwise=True))
        self.image_viewer.rotate_ccw_requested.connect(lambda: self.image_op.rotate(clockwise=False))

        self.image_viewer.photo_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.image_viewer.photo_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.image_viewer.photo_switched.connect(self.set_photo)

        self.image_viewer.add_layer(PhotoLayer(self.state))
        self.viz_layer = VisualizationLayer()
        self.viz_layer.initialize()
        self.viz_layer.setOpacity(.90)

        self.image_viewer.add_layer(self.viz_layer)

        self.image_viewer.hide()

        self.ruler_tool: Tool_Ruler = Tool_Ruler(self.state)
        self.ruler_tool.show_real_units(False)
        self.ruler_tool.current_value.connect(self.compute_resolution)

        self.ruler_tools: typing.List[Tool_Ruler] = []

        self.image_viewer.set_tool(self.ruler_tool)
        self.image_viewer.ui.controlBar.addItem(self._layout)
        self.setLayout(self.image_viewer.layout())

    def _fetch_photo(self, idx):
        photo = self.photo_model.fetch_photo(idx)

        if photo is None:
            return

        scale_set = self.scale_settings[photo.image_path]

        self.setWindowTitle(f'{photo.image_name} - Set scale')

        self.image_viewer.set_photo(photo, reset_view=True, reset_tool=False)

    def _fetch_first_photo(self):
        self._fetch_photo(0)

    def _fetch_prev_photo(self):
        paths = self.photo_model.image_paths
        curr_idx_int = paths.index(self.state.current_photo.image_path)
        self._fetch_photo(curr_idx_int - 1)

    def _fetch_next_photo(self):
        paths = self.photo_model.image_paths
        curr_idx_int = paths.index(self.state.current_photo.image_path)
        self._fetch_photo(curr_idx_int + 1)

    def _fetch_last_photo(self):
        self._fetch_photo(self.photo_model.rowCount(QModelIndex()) - 1)

    def _new_reference_length(self, value: int):
        self.compute_resolution(self.scale_settings[self.photo.image_path].new_scale_set.scale_line.length)

    def _set_global_resolution(self):
        idx = self.photo_model.image_storage.image_names.index(self.state.current_photo.image_name)
        photo_ = self.photo_model.image_storage.get_photo_by_idx(idx, load_image=False)

        scale_setting = self.scale_settings[photo_.image_path].new_scale_set

        for img_path, scale_tup in self.scale_settings.items():
            if img_path == photo_.image_path:
                continue
            scale_tup.new_scale_set.scale = scale_setting.scale
            scale_tup.new_scale_set.scale_line = None #ScaleLineInfo((0, 0), (0, 0), Value(0, self.ruler_tool._px_unit))
            scale_tup.new_scale_set.reference_length = None

    def accept_changes_current(self):
        self.accepted.emit([self.state.current_photo])

    def accept_changes_all(self):
        self.accepted.emit(self.photo_model.image_storage.images)

    def compute_resolution(self, pixels: typing.Optional[pint.Quantity]):
        if pixels is None:
            self.unset_line()
            return
        self.line_length = pixels
        self._lblPixels.setText(f'Line length: {pixels:~P}')

        if pixels.magnitude > 0:
            self._cmbUnits.setEnabled(True)
            self._spboxReference_mm.setEnabled(True)
        else:
            self.unset_line()
            return

        idx = self.photo_model.image_storage.image_names.index(self.state.current_photo.image_name)
        photo = self.photo_model.image_storage.get_photo_by_idx(idx, load_image=False)
        # ref_length = Value(self._spboxReference_mm.value(), self._cmbUnits.itemData(self._cmbUnits.currentIndex()))
        ref_length: pint.Quantity = self._spboxReference_mm.value() * self._cmbUnits.currentData()
        res = pixels / ref_length
        self.scale = res
        scale_setting = self.scale_settings[photo.image_path]
        scale_setting.new_scale_set.scale = res
        if pixels.magnitude == 0:
            scale_setting.new_scale_set.scale = None
        if scale_setting.new_scale_set.scale_line is None:
            if len(self.ruler_tool.endpoints) >= 2:
                scale_setting.new_scale_set.scale_line = ScaleLineInfo(
                    p1=self.ruler_tool.endpoints[0].toTuple(),
                    p2=self.ruler_tool.endpoints[1].toTuple(),
                    length=pixels
                )
            else:
                scale_setting.new_scale_set.scale_line = ScaleLineInfo(
                    p1=(0, 0),
                    p2=(0, 0),
                    length=0 * ureg('pixel')
                    # length=Value(0, self.ruler_tool._px_unit)
                )
        scale_setting.new_scale_set.scale_line.length = pixels
        scale_setting.new_scale_set.reference_length = ref_length
        self.ruler_tool.set_scale(res)

        if len(self.ruler_tool.endpoints) > 1:
            scale_setting.new_scale_set.scale_line.p1 = self.ruler_tool.endpoints[0].toTuple()
            scale_setting.new_scale_set.scale_line.p2 = self.ruler_tool.endpoints[1].toTuple()

        self._set_lbl_scale_value_text(str(scale_setting.new_scale_set.scale))
        self._btnAcceptAll.setEnabled(True)
        self._btnResolutionGlobal.setEnabled(True)
        self.set_line(scale_setting.new_scale_set.scale_line, scale_setting.new_scale_set.reference_length)

    def set_photo(self, photo: Photo):
        self.photo = photo

        self.image_op.init(photo)
        self.state.current_photo = photo

        if photo is None:
            return

        scale_setting = self.scale_settings[photo.image_path].new_scale_set
        self.ruler_tool.set_scale(scale_setting.scale)
        scale_line = scale_setting.scale_line
        self.unset_line()
        if scale_line is not None:
            self.set_line(scale_line, scale_setting.reference_length)
        else:
            self.unset_line()
            # self.ruler_tool.reset_tool()
            # self._lblPixels.setText('Line length: no line drawn')
            # # if there is not scale line yet, disable referene length spinner and units combobox
            # # self.set_line_length(Value(0, self.state.units.units['px']))
            # self._spboxReference_mm.setEnabled(False)
            # self._cmbUnits.setEnabled(False)
        if scale_setting.scale is not None and scale_setting.scale.magnitude > 0:
            # self._lblResolution.setText(f'Scale: {scale_setting.scale}')
            # self._lblScaleValue.setText(str(scale_setting.scale))
            self._set_lbl_scale_value_text(str(scale_setting.scale))
        else:
            self._set_lbl_scale_value_text('not set')
        self.setWindowTitle(f'{photo.image_name} - Set scale')
        self.image_viewer.set_tool(self.ruler_tool, reset_current=False)
        self.viz_layer.paint_commands = self.ruler_tool.viz_commands
        self.viz_layer.update()

    def set_line_length(self, length: pint.Quantity):
        self.line_length = length
        if length.magnitude > 0:
            self._cmbUnits.setEnabled(True)
            self._spboxReference_mm.setEnabled(True)
        self._lblPixels.setText(f'Line length: {self.line_length:~P}')
        if self.photo.scale_setting.reference_length is not None:
            self._spboxReference_mm.setValue(self.photo.scale_setting.reference_length.magnitude)
        else:
            if length.magnitude > 0 and self.photo.image_scale is not None and self.photo.image_scale.magnitude > 0:
                self._spboxReference_mm.setValue(round(length.magnitude / self.photo.image_scale.magnitude))
        self.compute_resolution(self.line_length)

    def _handle_reference_unit_changed(self, idx: int):
        self.compute_resolution(self.scale_settings[self.photo.image_path].new_scale_set.scale_line.length)
        self._set_lbl_scale_value_text(str(self.scale_settings[self.photo.image_path].new_scale_set.scale))

    # def initialize(self, storage: Storage):
    #     logging.info(f'Scale setting: initializing storage {storage.location}')
    #     self.image_viewer.set_storage(storage)
    #     if self._storage is not None:
    #         self._storage.update_photo.disconnect(self._handle_update_photo)
    #     self._storage = storage
    #     self._storage.update_photo.connect(self._handle_update_photo)
    #     self._storage.storage_update.connect(self._handle_storage_update)
    #     self.scale_settings.clear()
    #     self.ruler_tool.reset_tool()
    #     for idx in range(self._storage.image_count):
    #         photo = self._storage.get_photo_by_idx(idx, load_image=False)
    #         self.scale_settings[photo.image_path] = ScaleSettingTuple(
    #             old_scale_set=photo.scale_setting,
    #             new_scale_set=copy.deepcopy(photo.scale_setting)
    #         )

    def initialize(self, photo_model: ImageListSortFilterProxyModel):
        self.image_viewer.set_storage(photo_model.image_storage)
        # if self.photo_model is not None:
        #     if (storage := self.photo_model.image_storage) is not None:
        #         storage.update_photo.disconnect(self._handle_update_photo)
        if self._storage is not None:
            self._storage.update_photo.connect(self._handle_update_photo, Qt.ConnectionType.UniqueConnection)
            self._storage.update_photo.disconnect(self._handle_update_photo)
        self.photo_model = photo_model
        self._storage = self.photo_model.image_storage
        self._storage.update_photo.connect(self._handle_update_photo)
        self._storage.storage_update.connect(self._handle_storage_update)
        self.scale_settings.clear()
        self.ruler_tool.reset_tool()
        for idx in range(self._storage.image_count):
            photo = self._storage.get_photo_by_idx(idx, load_image=False)
            self.scale_settings[photo.image_path] = ScaleSettingTuple(
                old_scale_set=photo.scale_setting,
                new_scale_set=copy.deepcopy(photo.scale_setting)
            )
        total = self.photo_model.source_model.rowCount()
        shown = self.photo_model.rowCount()
        hidden = total - shown
        self.image_viewer.ui.lblMessage.setText(f'Browsing {shown} photo{"s" if shown != 1 else ""}{"" if hidden == 0 else f" ({hidden} hidden)"}.')

    @property
    def _storage(self) -> typing.Optional[Storage]:
        return None if self.photo_model is None else self.photo_model.image_storage

    @_storage.setter
    def _storage(self, storage: typing.Optional[Storage]):
        self.state.storage = storage

    def _handle_update_photo(self, update: UpdateEvent):
        if self.photo is None or update.photo.image_name != self.photo.image_name:
            return
        scale_setting = self.scale_settings[update.photo.image_path].new_scale_set
        self.ruler_tool.set_scale(scale_setting.scale)
        scale_line = scale_setting.scale_line
        if (ref_length := scale_setting.reference_length) is not None:
            self._spboxReference_mm.setValue(ref_length.magnitude)
            # self._cmbUnits.setCurrentIndex(list(SIPrefix).index(ref_length.unit.prefix))
            index = self.ref_length_units.index(ref_length.units)
            self._cmbUnits.setCurrentIndex(index)
        event_obj: PhotoUpdate = update.update_obj
        if scale_line is not None: #and 'operation' in data:
            if event_obj.update_type in {PhotoUpdateType.Rotate90CCW, PhotoUpdateType.Rotate90CW}:
                scale_line.rotate(event_obj.update_type == PhotoUpdateType.Rotate90CCW,
                                  (round(0.5 * update.photo.image_size[1]),
                                    round(0.5 * update.photo.image_size[0])))
            self.set_line(scale_line, scale_setting.reference_length)
        else:
            self.unset_line()
        self.viz_layer.paint_commands = self.ruler_tool.viz_commands
        self.viz_layer.update()

    def _handle_storage_update(self, update: StorageUpdate):
        for photo_name in update.photos_included:
            photo = self._storage.get_photo_by_name(photo_name, load_image=False)
            self.scale_settings[photo.image_path] = ScaleSettingTuple(
                old_scale_set=photo.scale_setting,
                new_scale_set=copy.deepcopy(photo.scale_setting)
            )

    def _set_unit_to_cmbUnits(self, unit: pint.Unit):
        self._cmbUnits.setCurrentIndex(self.ref_length_units.index(unit))

    def set_line(self, scale_line: ScaleLineInfo, ref_length: pint.Quantity):
        scale_setting = self.scale_settings[self.photo.image_path].new_scale_set
        self._spboxReference_mm.setEnabled(True)
        self._spboxReference_mm.blockSignals(True)
        self._spboxReference_mm.setValue(ref_length.magnitude)
        self._spboxReference_mm.blockSignals(False)
        self._cmbUnits.setEnabled(True)
        self._set_unit_to_cmbUnits(ref_length.units)
        self.ruler_tool.set_line(QPoint(*scale_line.p1), QPoint(*scale_line.p2), reset_others=True)
        self._set_lbl_scale_value_text(str(scale_line.length / ref_length))
        self._lblPixels.setText(f'Line length: {scale_line.length:~P}')
        self.viz_layer.paint_commands = self.ruler_tool.viz_commands
        self.viz_layer.update()

    def unset_line(self):
        self._spboxReference_mm.setEnabled(False)
        self._cmbUnits.setEnabled(False)
        self._lblPixels.setText('Line length: no line drawn')
        self._set_lbl_scale_value_text('not set')
        self.ruler_tool.reset_tool()

    def _get_scale_from_user(self):
        dialog = QDialog()
        dialog.setWindowTitle("Enter scale numerically")
        spbox = QDoubleSpinBox()
        spbox.setRange(0, 999)
        spbox.setSpecialValueText('0 (invalid value)')
        if self.scale_settings[self.photo.image_path].new_scale_set.scale is not None:
            spbox.setValue(self.scale_settings[self.photo.image_path].new_scale_set.scale.magnitude)

        cmbUnits = QComboBox()
        scale_setting = self.scale_settings[self.photo.image_path].new_scale_set
        default_idx = 0
        # for i, prefix in enumerate(list(SIPrefix)):
        for i, ref_unit in enumerate(self.ref_length_units):
            # unit = self.units.units['px'] / Unit(BaseUnit.m, prefix=prefix, dim=1)
            unit = ureg['pixel'] / ref_unit
            cmbUnits.addItem(str(unit), unit)
            if scale_setting.scale is not None and scale_setting.scale.units == unit:
                default_idx = i

        cmbUnits.setCurrentIndex(default_idx)

        diag_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        diag_buttons.accepted.connect(dialog.accept)
        diag_buttons.rejected.connect(dialog.reject)

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Scale: '))
        hbox.addWidget(spbox)
        hbox.addWidget(cmbUnits)

        vbox.addLayout(hbox)
        vbox.addWidget(diag_buttons)

        dialog.setLayout(vbox)

        if dialog.exec_() == QDialog.Accepted:
            # scale_setting.scale = Value(spbox.value(), cmbUnits.currentData())
            scale_setting.scale = spbox.value() * cmbUnits.currentData()
            scale_setting.scale_line = None
            scale_setting.reference_length = None
            self.unset_line()
            self._set_lbl_scale_value_text(str(scale_setting.scale))

    def extract_scale_for_current(self, parent: QWidget=None):
        self._scale_not_found_photo_names.clear()
        idxs = [self.state.storage.image_names.index(self.state.current_photo.image_name)]
        block_op = BlockingOperation(self.state.storage, idxs,
                                     operation=self._scale_extraction_operation,
                                     result_handler=self._scale_extraction_result_processing,
                                     parent=self if parent is None else parent)
        block_op.start()

    def extract_scale_for_all(self, parent: QWidget=None):
        # Extract for all photos that are shown.
        proxy_indexes = [self.photo_model.index(i, 0) for i in range(self.photo_model.rowCount())]
        source_indexes = [self.photo_model.mapToSource(index).row() for index in proxy_indexes]
        self._scale_not_found_photo_names.clear()
        block_op = BlockingOperation(self.photo_model.image_storage, source_indexes,
                                     operation=self._scale_extraction_operation,
                                     result_handler=self._scale_extraction_result_processing,
                                     parent=self if parent is None else parent)
        block_op.start()

    def extract_scale_for_photo(self, photo: Photo, parent: QWidget=None):
        idx = self.photo_model.image_storage.image_names.index(photo.image_name)
        block_op = BlockingOperation(self.photo_model.image_storage, [idx],
                                     operation=self._scale_extraction_operation,
                                     result_handler=self._scale_extraction_result_processing,
                                     parent=self if parent is None else parent)
        block_op.start()

    def _scale_extraction_operation(self, storage: Storage, idx: int) -> typing.Optional[ScaleExtractionResult]:
        dig_re = re.compile(r'([0-9]+)\s*([a-zA-Z]m)')
        unit_store = ureg

        img_path = storage.image_paths[idx]
        image = cv2.imread(str(img_path))
        scale_marker, (left, top, width, height) = get_scale_marker_roi(image)
        ref_length, scale_rotated = get_reference_length(scale_marker)
        p1x, p1y, p2x, p2y = get_scale_line_ends(scale_marker)
        if p1x < 0:
            return None
        if len(ref_length) > 0:
            match = dig_re.match(ref_length)
            length = int(match.groups()[0])
            unit_str = match.groups()[1]
            unit = ureg(unit_str)
            ref_length = length * unit
            px_length = ScalarValue(round(math.sqrt(((p1x - p2x) * (p1x - p2x) + (p1y - p2y) * (p1y - p2y)))) * ureg['pixel'])
            image_scale = px_length / ref_length
        else:
            ref_length = None
            image_scale = None
            px_length = None
        p1x_, p1y_, p2x_, p2y_ = get_scale_line_ends(scale_rotated)
        scale_rotated = cv2.cvtColor(scale_rotated, cv2.COLOR_GRAY2RGB)
        scale_rotated = cv2.line(scale_rotated, (p1x_, p1y_ - 10), (p1x_, p1y_ + 10), [0, 255, 0], thickness=2)
        scale_rotated = cv2.line(scale_rotated, (p2x_, p1y_ - 10), (p2x_, p1y_ + 10), [0, 255, 0], thickness=2)
        scale_rotated = cv2.resize(scale_rotated, (154, 26), interpolation=cv2.INTER_LINEAR)
        scale_marker = scale_rotated

        return ScaleExtractionResult(idx, image_scale, ref_length, px_length,
                                     (p1x+left, p1y+top),
                                     (p2x+left, p2y+top),
                                     scale_marker,
                                     (left, top, width, height))

    def _scale_extraction_result_processing(self, storage: Storage, idx: int,
                                            result: typing.Optional[ScaleExtractionResult],
                                            finished: bool):
        if result is None or result.reference_length is None:
            self._scale_not_found_photo_names.append(storage.get_photo_by_idx(idx, load_image=False).image_name)
        else:
            path = storage.image_paths[idx]
            sc_info = self.scale_settings[path].new_scale_set
            sc_info.scale = result.image_scale
            if sc_info.scale_line is None:
                # sc_info.scale_line = ScaleLineInfo(p1=(-1, -1), p2=(-1, -1), length=Value(0, self.units.units['px']))
                sc_info.scale_line = ScaleLineInfo(p1=(-1, -1), p2=(-1, -1), length=0 * ureg['pixel'])
            sc_info.reference_length = result.reference_length
            sc_info.scale_line.p1 = result.scale_line_p1
            sc_info.scale_line.p2 = result.scale_line_p2
            sc_info.scale_line.length = float(np.sqrt(np.sum(np.square(np.array(sc_info.scale_line.p1) - np.array(sc_info.scale_line.p2))))) * ureg['pixel']
            sc_info.scale_marker_bbox = tuple([int(v) for v in result.scale_marker_bbox]) if result.scale_marker_bbox is not None else None
            sc_info.scale_marker_img = QPixmap.fromImage(qimage2ndarray.array2qimage(result.scale_marker))

            if self.state.current_photo is not None and path == self.state.current_photo.image_path:
                self.set_line(sc_info.scale_line, sc_info.reference_length)

            self._btnAcceptAll.setEnabled(True)

        if finished and len(self._scale_not_found_photo_names) > 0:
            # msg_box = QMessageBox()
            # msg_box.setStandardButtons(QMessageBox.StandardButton.Close)
            # msg_box.setWindowTitle('Scale extraction results')
            # msg_box.setText('Could not find scale values for these photos:')
            # msg_box.setDetailedText('\n'.join(self._scale_not_found_photo_names))
            # msg_box.exec_()

            msg = MessageWidget()
            msg.setWindowTitle('Scale extraction results')
            msg.message.setText('Could not find scale value for these photos:')
            msg.detailed_message.setText('\n'.join(self._scale_not_found_photo_names))
            msg.exec_()


    def closeEvent(self, event:PySide6.QtGui.QCloseEvent):
        super().closeEvent(event)
        self.cancelled.emit()

    def _set_lbl_scale_value_text(self, text: str):
        self._lblScaleValue.setText(text)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.image_viewer.show_whole_image()


class ScaleItemDelegate(ThumbnailDelegate):
    def __init__(self, thumbnails: ThumbnailStorage_, scale_set_widget: ScaleSettingWidget,
                 parent: QObject = None):
        super().__init__(thumbnails, parent)
        self.scale_set_widget = scale_set_widget

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        super().paint(painter, option, index)
        path = index.data(Qt.UserRole + 8)
        scale_marker: typing.Optional[QPixmap] = self.scale_set_widget.scale_settings[path].new_scale_set.scale_marker_img  # TODO replace 7 with a named constant
        thumbnail: QImage = index.data(Qt.UserRole + 3)
        rect: QRect = option.rect
        if scale_marker is None:
            return
        scale_rect = QRect(rect.center().x() - 0.5 * scale_marker.width(), rect.bottom() - 32 - scale_marker.height(),
                           scale_marker.width(), scale_marker.height())
        painter.save()
        painter.setRenderHint(painter.SmoothPixmapTransform, True)
        painter.drawPixmap(scale_rect, scale_marker)
        painter.restore()
