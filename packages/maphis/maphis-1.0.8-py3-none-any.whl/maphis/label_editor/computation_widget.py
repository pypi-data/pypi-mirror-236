import typing
from typing import Optional, Union

from PySide6.QtCore import Signal, QSortFilterProxyModel, Qt, QItemSelection
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu, QSizePolicy

from maphis.common.param_widget import ParamWidget
from maphis.common.plugin import PropertyComputation, RegionComputation
from maphis.common.state import State
from maphis.common.user_params import UserParamWidgetBinding, create_params_widget
from maphis.label_editor.ui_computation import Ui_Computations
from maphis.plugin_manager_ import RegionCompsListModel, ProcessType


class ComputationWidget(QWidget):
    apply_computation = Signal(RegionComputation, ProcessType)

    def __init__(self, state: State, parent: Optional[QWidget] = None):
        QWidget.__init__(self, parent)
        self.settings_group_shown:bool = True
        self.restrict_group_shown: bool = True
        self._current_colormap_model = None
        self.ui = Ui_Computations()
        self.ui.setupUi(self)
        self.ui.grpRegionSettings.setLayout(QVBoxLayout())
        self.ui.grpRegionSettings.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        # self.ui.scrollSettings.setLayout(QVBoxLayout())

        self.ui.btnRegApply.setEnabled(False)
        self.ui.btnRegApplyAll.setEnabled(False)

        self.state = state
        # self.state.update_used_label_list.connect(self._update_region_restrict_model)

        self.computations_model = RegionCompsListModel()

        self.current_computation_idx: int = -1

        self.ui.cmbRegComps.setModel(self.computations_model)
        self.ui.cmbRegComps.currentIndexChanged.connect(self._handle_computation_selected)

        self._comp_param_widget: typing.Optional[ParamWidget] = None
        self._current_reg_comp: Optional[RegionComputation] = None
        self._param_binding: Optional[UserParamWidgetBinding] = UserParamWidgetBinding(self.state)

        self.ui.btnRegApply.clicked.connect(self.handle_apply_clicked)
        self.ui.btnRegApplyAll.clicked.connect(self.handle_apply_all_clicked)

        self._btnRegApplyAllMenu = QMenu()
        self.action_applyToUnsegmented = QAction('Apply to all unsegmented')
        self.action_applyToUnsegmented.triggered.connect(self.handle_apply_all_unseg_clicked)
        self._btnRegApplyAllMenu.addAction(self.action_applyToUnsegmented)
        self.ui.btnRegApplyAll.setMenu(self._btnRegApplyAllMenu)

        # self.ui.btnRegApplyAllUnseg.clicked.connect(self.handle_apply_all_unseg_clicked)

        self.region_restrict_model = QSortFilterProxyModel()
        # FIXME set a correct color model
        #self.region_restrict_model.setSourceModel(self.state.colormap)
        self.ui.regRestrictView.setModel(self.region_restrict_model)
        self.region_restrict_model.setFilterRole(Qt.UserRole + 3)
        self.region_restrict_model.setFilterFixedString('used')

        self.selected_regions = []

        self.region_sel_model: QItemSelection = self.ui.regRestrictView.selectionModel()
        self.region_sel_model.selectionChanged.connect(self._handle_label_selection_changed)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        self.adjustSize()
        # self.setMaximumWidth(150)

    def handle_apply_clicked(self, chkd: bool):
        if self.current_computation_idx < 0 or self.current_computation_idx >= len(self.computations_model.region_comps):
            return
        self.apply_computation.emit(self.computations_model.region_comps[self.current_computation_idx],
                                    ProcessType.SELECTED_PHOTOS)

    def handle_apply_all_clicked(self, chkd: bool):
        if self.current_computation_idx < 0 or self.current_computation_idx >= len(self.computations_model.region_comps):
            return
        self.apply_computation.emit(self.computations_model.region_comps[self.current_computation_idx],
                                           ProcessType.ALL_PHOTOS)

    def handle_apply_all_unseg_clicked(self, chkd: bool):
        if self.current_computation_idx < 0 or self.current_computation_idx >= len(self.computations_model.region_comps):
            return
        self.apply_computation.emit(self.computations_model.region_comps[self.current_computation_idx],
                                    ProcessType.ALL_UNSEGMENTED)

    def register_computation(self, computation: Union[RegionComputation, PropertyComputation]):
        self.computations_model.add_computation(computation)
        if self.current_computation_idx < 0:
            self.ui.cmbRegComps.setCurrentIndex(0)
        self.ui.btnRegApply.setEnabled(True)
        self.ui.btnRegApplyAll.setEnabled(True)

    def _handle_computation_selected(self, idx: int):
        self.current_computation_idx = idx
        computation = self.computations_model.region_comps[self.current_computation_idx]
        self.ui.lblCompDesc.setText(computation.info.description)
        self.ui.grpRegDesc
        # self.ui.lblCompDesc.setText(computation.info.description)

        if self._comp_param_widget is not None:
            self.ui.grpRegionSettings.layout().removeWidget(self._comp_param_widget.widget)
            # self.ui.scrollSettings.layout().removeWidget(self._comp_param_widget)
            self._param_binding.param_widget = None
            self._param_binding.user_params = dict()
            self._comp_param_widget.widget.hide()
            self._comp_param_widget = None
        if len(computation.user_params) > 0:
            # self._comp_param_widget = create_params_widget(computation.user_params, self.state)
            self._comp_param_widget = ParamWidget(computation.user_params)
            # self._param_binding.bind(computation.user_params, self._comp_param_widget)
            self.ui.grpRegionSettings.layout().addWidget(self._comp_param_widget.widget)
            # self.ui.scrollSettings.layout().addWidget(self._comp_param_widget)
            self.ui.grpRegionSettings.setVisible(self.settings_group_shown and True)
            # self.ui.scrollSettings.setVisible(self.settings_group_shown and True)
        else:
            self.ui.grpRegionSettings.setVisible(False)
            # self.ui.scrollSettings.setVisible(False)
        # self.ui.grpRegRestrict.setVisible(self.restrict_group_shown and computation.region_restricted)
        self.ui.grpRegRestrict.setVisible(False)
        # self.ui.pgRegionRestriction.setVisible(self.restrict_group_shown and computation.region_restricted)
        # self.ui.scrollRegionRestrictions.update()
        # self.ui.pgRegionRestriction.update()
        self.ui.grpRegionSettings.update()
        if computation.region_restricted:
            self.region_restrict_model.setSourceModel(self._current_colormap_model)
            self.region_restrict_model.setFilterFixedString('used')
            self.ui.regRestrictView.setModel(self.region_restrict_model)
        else:
            self.region_restrict_model.setFilterFixedString('')
        self.ui.regRestrictView.setVisible(self.restrict_group_shown and computation.region_restricted)

    def _handle_label_selection_changed(self, selection: QItemSelection):
        indexes = self.region_sel_model.selectedIndexes()
        self.selected_regions.clear()

        for index in indexes:
            self.selected_regions.append(self.region_restrict_model.data(index, Qt.UserRole))

    def _update_region_restrict_model(self):
        self.region_restrict_model.setSourceModel(self._current_colormap_model)
        self.ui.regRestrictView.update()

    def set_restrict_group_shown(self, shown: bool):
        self.restrict_group_shown = shown
        # self.ui.pgRegionRestriction.setHidden(not shown)
        self.ui.grpRegRestrict.setHidden(not shown)

    def set_settings_group_shown(self, shown: bool):
        self.settings_group_shown = shown
        self.ui.grpRegionSettings.setHidden(not shown)
        # self.ui.pgSettings.setHidden(not shown)
        # if not shown:
        #     self.ui.toolBox.removeItem(1)