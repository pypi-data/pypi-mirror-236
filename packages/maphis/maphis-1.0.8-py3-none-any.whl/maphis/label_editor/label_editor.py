import logging
import shutil
import tempfile
import typing
from pathlib import Path
from typing import Optional, List

from PySide6.QtCore import Signal, QObject, QSize, QItemSelectionModel, QPoint, QModelIndex
from PySide6.QtGui import Qt, QImage, QPixmap, QColor, QAction
from PySide6.QtWidgets import QWidget, QToolButton, QGroupBox, QVBoxLayout, QGridLayout, QSizePolicy, QButtonGroup, \
    QAbstractButton, QRadioButton, QHBoxLayout, QSpacerItem, QLabel, QMenu

from maphis.common.edit_command_executor import EditCommandExecutor
from maphis.common.label_change import DoType, CommandEntry, CommandKind
from maphis.common.label_hierarchy import Node, LabelHierarchy
from maphis.common.label_image import LabelImgInfo
from maphis.common.label_tree_model import LabelTreeModel
from maphis.common.label_tree_view import LabelTreeView
from maphis.common.local_storage import Storage
from maphis.common.photo import Photo
from maphis.layers.photo_layer import PhotoLayer
from maphis.common.state import State, LabelConstraint
from maphis.common.tool import Tool
from maphis.common.undo_manager import UndoManager
from maphis.common.user_params import UserParamWidgetBinding
from maphis.layers.visualization_layer import VisualizationLayer
from maphis.image_viewer import ImageViewer
from maphis.label_editor.computation_widget import ComputationWidget
from maphis.layers.label_layer import LabelLayer
from maphis.label_editor.label_level_switch import LabelLevelSwitch
from maphis.label_editor.new_label_dialog import NewLabelDialog
from maphis.label_editor.ui_label_editor import Ui_LabelEditor

import PySide6
from PySide6.QtWidgets import QApplication

from maphis.project.annotation import AnnotationType
from maphis.project.annotation_delegate import AnnotationDelegate
from maphis.project.landmark_delegate import KeypointDelegate


class ToolEntry:
    def __init__(self, tool: Tool, toolbutton: QToolButton, param_widget: typing.Optional[QWidget]=None):
        self.tool = tool
        self.toolbutton = toolbutton
        self.param_widget = param_widget


class LabelEditor(QObject):
    approval_changed = Signal(Photo)
    unsaved_changes = Signal()

    def __init__(self, state: State, undo_action: QAction, redo_action: QAction, cmd_executor: EditCommandExecutor):
        QObject.__init__(self)
        self.widget = QWidget()
        self.ui = Ui_LabelEditor()
        self.ui.setupUi(self.widget)

        self.ui.toolBox.setVisible(False)

        self.temp_dir = Path(tempfile.mkdtemp())

        self.state = state

        self.state.storage_changed.connect(self.handle_storage_changed)

        self._tools: typing.List[Tool] = []

        self._tools_: typing.List[ToolEntry] = []

        self.tool_param_binding: UserParamWidgetBinding = UserParamWidgetBinding(self.state)

        self._setup_image_viewer()

        self._setup_label_level_switch()

        self._current_tool: typing.Optional[Tool] = None
        self._current_tool_widget: typing.Optional[QWidget] = None

        vbox = QVBoxLayout()

        self.col_count = 6

        self._setup_toolbox()

        # self._setup_new_label_dialog()
        self._new_label_dialog: typing.Optional[NewLabelDialog] = None
        self._setup_label_tree_widget()

        self._tool_param_widgets: typing.List[QWidget] = []

        #self.ui.tabSidebar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.ui.tabPlugins.setLayout(QVBoxLayout())

        self.undo_stack: List[List[CommandEntry]] = []
        self.redo_stack: List[List[CommandEntry]] = []

        self.cmd_executor: EditCommandExecutor = cmd_executor
        self.cmd_executor.label_approval_changed.connect(self.handle_approval_changed)
        self.cmd_executor.label_image_modified.connect(self.handle_label_image_changed)
        self.undo_manager: UndoManager = self.cmd_executor.undo_manager
        self.undo_manager.enable_undo_redo.connect(self.enable_undo_redo)

        self.undo_action = undo_action
        self.redo_action = redo_action

        self.ui.tbtnUndo.clicked.connect(self.handle_undo_clicked)
        self.ui.tbtnRedo.clicked.connect(self.handle_redo_clicked)

        self.enable_undo_action(False, '')
        self.enable_redo_action(False, '')

        self.undo_action.triggered.connect(self.handle_undo_clicked)
        self.redo_action.triggered.connect(self.handle_redo_clicked)

        self._setup_hovered_label_info()

        self.widget.setEnabled(False)

        self._label_types_btn_group = QButtonGroup()
        self._label_types_btn_group.setExclusive(True)
        self._label_types_btn_group.buttonClicked.connect(self.handle_label_type_button_clicked)
        self.ui.MaskGroup.setEnabled(True)

        self.region_computation_widget = ComputationWidget(self.state)
        self.measurements_computation_widget = ComputationWidget(self.state)

        QObject.connect(QApplication.instance(), PySide6.QtCore.SIGNAL("focusChanged(QWidget *, QWidget *)"), self.handle_focus_changed)

        self._annotation_delegates: typing.Dict[AnnotationType, AnnotationDelegate] = {
            AnnotationType.Keypoint: KeypointDelegate(self.viz_layer)
        }

    def handle_focus_changed(self, old, now):
        return

    def _setup_label_tree_widget(self):
        self._label_tree_model = LabelTreeModel(self.state)
        self._label_tree = LabelTreeView(self.state)
        self._label_tree.setModel(self._label_tree_model)
        self._label_tree.setEditTriggers(LabelTreeView.NoEditTriggers)
        self.state.new_label_constraint.connect(self._label_tree_model.set_constraint)
        self._label_tree.setIndentation(10)
        self._label_tree.setHeaderHidden(True)
        self.state.primary_label_changed.connect(self._handle_primary_label_changed)
        self._label_tree.label_color_change.connect(self._handle_label_color_changed)
        self._label_tree.label_color_change.connect(self._label_tree_model.handle_label_color_changed)
        self._label_tree.customContextMenuRequested.connect(self._show_label_context_menu)
        self._label_tree.label_dbl_click.connect(self.modify_label_node)

        self._label_context_menu: QMenu = QMenu()
        self._label_context_action_add = QAction('New child label')
        self._label_context_action_add.setData('add-label')
        self._label_context_action_add.triggered.connect(self._add_new_label)
        self._label_context_menu.addAction(self._label_context_action_add)
        self._label_context_action_remove_leaf = QAction('Remove label')
        self._label_context_action_remove_leaf.setData('remove-leaf')
        self._label_context_menu.addAction(self._label_context_action_remove_leaf)
        self._label_context_action_remove_subtree = QAction('Remove label and children')
        self._label_context_action_remove_subtree.setData('remove-subtree')
        self._label_context_menu.addAction(self._label_context_action_remove_subtree)

    def _setup_new_label_dialog(self):
        if self._new_label_dialog is not None:
            self._new_label_dialog.hide()
            self._new_label_dialog.deleteLater()
            self._new_label_dialog = None
        self._new_label_dialog = NewLabelDialog(self.state.label_hierarchy)
        self._new_label_dialog.modified_label.connect(self._handle_label_node_modified)
        self._new_label_dialog.add_new_label_requested.connect(self.handle_new_label_requested)
        self._new_label_dialog.hide()

    def _show_label_context_menu(self, pos: QPoint):
        index = self._label_tree.indexAt(pos)
        if index.isValid():
            node: Node = index.internalPointer()
            self._label_context_action_add.setData(node)
            if self.state.label_hierarchy.get_level(node.label) + 1 == len(self.state.label_hierarchy.hierarchy_levels):
                self._label_context_action_add.setVisible(False)
            else:
                self._label_context_action_add.setVisible(True)
            if len(node.children) > 0:
                self._label_context_action_remove_leaf.setVisible(False)
                if node.label > 0:
                    self._label_context_action_remove_subtree.setData(node)
                    self._label_context_action_remove_subtree.setVisible(True)
            else:
                self._label_context_action_remove_subtree.setVisible(False)
                if node.label > 0:
                    self._label_context_action_remove_leaf.setData(node)
                    self._label_context_action_remove_leaf.setVisible(True)
            self._label_context_menu.exec_(self._label_tree.viewport().mapToGlobal(pos))
        else:
            self._label_context_action_remove_leaf.setVisible(False)
            self._label_context_action_remove_subtree.setVisible(False)
            self._label_context_action_add.setVisible(True)
            self._label_context_action_add.setData(self.state.label_hierarchy[-1])
            self._label_context_menu.exec_(self._label_tree.viewport().mapToGlobal(pos))

    # Make sure toggling the visibility of the "hovered label" info does not affect the layout
    def _setup_hovered_label_info(self):
        for i in range(self.ui.layoutLabelInfo.count()):
            sp_retain = self.ui.layoutLabelInfo.itemAt(i).widget().sizePolicy()
            sp_retain.setRetainSizeWhenHidden(True)
            self.ui.layoutLabelInfo.itemAt(i).widget().setSizePolicy(sp_retain)
        self.ui.lblLabelIcon.setPixmap(QPixmap(24, 24)) # TODO: Use some named constant for this, and for the dimensions in "self.label_color_pixmap = QPixmap(24, 24)" in app.py

    def _setup_label_level_switch(self):
        self._label_switch = LabelLevelSwitch(self.state, self.widget)
        # self.state.label_hierarchy_changed.connect(self._label_switch.set_label_hierarchy)
        self.state.label_hierarchy_changed.connect(self.handle_label_hierarchy_changed)
        self._label_switch.approval_toggled.connect(self.toggle_approval_for)

        lay = QHBoxLayout()
        self.image_viewer.ui.controlBar.addWidget(self._label_switch)
        self.image_viewer.ui.controlBar.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))

    def handle_label_hierarchy_changed(self, lab_hier: LabelHierarchy):
        print('reacting to label hierarchy change')
        self._label_switch.set_label_hierarchy(lab_hier)
        self.adjust_level_approval_switch_width()

    def adjust_level_approval_switch_width(self):
        width = 0
        for idx in range(self.image_viewer.ui.controlBar.count()):
            widget = self.image_viewer.ui.controlBar.itemAt(idx).widget()
            if widget is None or isinstance(widget, LabelLevelSwitch):
                continue
            width += widget.width()
        width += self.image_viewer.ui.controlBar.count() * self.image_viewer.ui.controlBar.layout().spacing()
        width_to_set = int(0.95 * (self.image_viewer.width() - width))
        self._label_switch.setMaximumWidth(width_to_set)

    def _setup_image_viewer(self):
        for i in range(self.ui.toolBar.count()):
            item = self.ui.toolBar.itemAt(i)
            if item is None:
                continue
            self.ui.toolBar.removeItem(item)
        self.image_viewer = ImageViewer(self.state)
        self.ui.photo_view.insertWidget(0, self.image_viewer)
        self.image_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.photo_layer = PhotoLayer(self.state)
        self.image_viewer.add_layer(self.photo_layer)

        self.label_layer = LabelLayer(self.state)
        self.image_viewer.add_layer(self.label_layer)
        self.label_layer.label_img_modified.connect(self.handle_label_changed)
        self.label_layer.cycle_constraint.connect(self.cycle_constraint)
        self.ui.btnFilledStyle.clicked.connect(self.label_layer.show_mask)
        self.ui.btnFilledStyle.clicked.connect(lambda: self.ui.spinOutlineWidth.setEnabled(False))
        self.ui.btnOutlineStyle.clicked.connect(self.label_layer.show_outline)
        self.ui.btnOutlineStyle.clicked.connect(lambda: self.ui.spinOutlineWidth.setEnabled(True))

        self.ui.spinOutlineWidth.valueChanged.connect(self.label_layer.change_outline_width)

        self.ui.sliderOpacity.valueChanged.connect(lambda val: self.label_layer.setOpacity(val / 100.0))
        self.label_layer.setOpacity(self.ui.sliderOpacity.value() / 100.0)

        self.viz_layer = VisualizationLayer(self.state)
        self.image_viewer.add_layer(self.viz_layer)
        self.viz_layer.setOpacity(.75)

        self.image_viewer.ui.controlBar.addWidget(self.ui.tbtnUndo)
        self.image_viewer.ui.controlBar.addWidget(self.ui.tbtnRedo)

        self.image_viewer.ui.controlBar.addWidget(self.ui.MaskGroup)
        self.image_viewer.ui.controlBar.addWidget(self.ui.grpMaskStyle)
        # lay = QHBoxLayout()
        self._label_constraint_label: QLabel = QLabel()
        self._tool_announcement_label: QLabel = QLabel()
        # lay.addWidget(self._label_constraint_label)
        self.image_viewer.ui.announcement_layout.addWidget(self._label_constraint_label)
        self.image_viewer.ui.announcement_layout.addWidget(self._tool_announcement_label)
        self.widget.layout().removeItem(self.ui.toolBar)

        self.image_viewer.photo_switched.connect(self.set_photo)

    def register_tools(self, tools: typing.List[Tool]):
        for tool in tools:
            self.register_tool(tool)

    def register_tool(self, tool: Tool):
        toolbutton = QToolButton()
        toolbutton.setCheckable(True)
        toolbutton.setToolTip(tool.tool_name)
        if tool.tool_icon is not None:
            toolbutton.setIcon(tool.tool_icon)
            toolbutton.setIconSize(QSize(32, 32))
        row, col = len(self._tools) // self.col_count, len(self._tools) % self.col_count

        self._tools.append(tool)
        param_widget = tool.setting_widget if tool.setting_widget is not None else QWidget()
        param_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.tool_buttons_layout.addWidget(toolbutton, row, col)
        self._tools_button_group.addButton(toolbutton, tool.tool_id)
        self._tool_param_widgets.append(param_widget)
        self.tool_settings.layout().addWidget(self._tool_param_widgets[tool.tool_id])
        param_widget.setVisible(False)
        self._tools_.append(ToolEntry(tool, toolbutton, param_widget))
        tool.cursor_changed.connect(self._handle_tool_cursor_changed)

    def _setup_toolbox(self):
        self.tool_box = QWidget()

        self.tool_box_layout = QVBoxLayout()

        self.tool_box.setLayout(self.tool_box_layout)

        self.tool_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self._tools_button_group = QButtonGroup()
        self._tools_button_group.buttonToggled.connect(self.handle_tool_activated)
        self._tools_button_group.setExclusive(False)
        self.tool_buttons_widg = QWidget()
        self.tool_buttons_layout = QGridLayout()
        self.tool_buttons_widg.setLayout(self.tool_buttons_layout)
        self.tool_box_layout.addWidget(self.tool_buttons_widg)
        self.tool_box_layout.setAlignment(self.tool_buttons_widg, Qt.AlignTop)
        self.tool_buttons_layout.setSpacing(1)

        self.tool_settings = QGroupBox('Settings')
        self.tool_settings.setVisible(False)
        self.tool_settings_layout = QVBoxLayout()
        self.tool_settings.setLayout(self.tool_settings_layout)
        self.tool_settings.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.tool_box_layout.setAlignment(self.tool_settings, Qt.AlignTop)

        self.tool_box_layout.addWidget(self.tool_settings)

        self.tool_out_widget = QGroupBox()
        self.tool_out_widget.setVisible(False)
        self.tool_box_layout.addWidget(self.tool_out_widget)

    def set_photo(self, photo: Optional[Photo], reset_view: bool=False):
        if photo is None:
            self.disable()
            return
        else:
            self.enable()
        for ann_delegate in self._annotation_delegates.values():
            ann_delegate.set_photo(photo)
        if self._current_tool is not None:
            self._current_tool.reset_tool()
            self._current_tool.switch_to_photo(self.state.current_photo)
        label_level = photo.approved[self.state.current_label_name]
        label_hierarchy = self.state.storage.get_label_hierarchy(self.state.current_label_name)
        level_names = [level.name for level in label_hierarchy.hierarchy_levels]
        if label_level is not None:
            label_level_idx = level_names.index(label_level)
            if label_level_idx + 1 < len(level_names):
                unapproved_index = label_level_idx + 1
            else:
                unapproved_index = label_level_idx
        else:
            label_level_idx = -1
            unapproved_index = 0
        self._label_switch.get_level_button(unapproved_index).setChecked(True)
        for i in range(label_level_idx + 1):
            self._label_switch.mark_approved(i, True)
        for i in range(label_level_idx + 1, len(self._label_switch._buttons)):
            self._label_switch.mark_approved(i, False)

        enable_undo, enable_redo = self.undo_manager.current_undo_redo.has_commands()

        if enable_undo:
            undo_command = self.undo_manager.current_undo_redo.undo_stack[-1][0].source
        else:
            undo_command = ''

        if enable_redo:
            redo_command = self.undo_manager.current_undo_redo.redo_stack[-1][0].source
        else:
            redo_command = ''

        self.enable_undo_action(enable_undo, undo_command)
        self.enable_redo_action(enable_redo, redo_command)


    def enable_undo_redo(self, image_name: str, label_name: str, do_type: DoType, enable: bool, command_name: str):
        if image_name != self.state.current_photo.image_name: # or label_name != self.state.current_label_name:
            return
        if do_type == DoType.Undo:
            self.enable_undo_action(enable, command_name)
        else:
            self.enable_redo_action(enable, command_name)

    def _set_tool_announcement(self, tool: Tool, ann: str):
        self._tool_announcement_label.setText(ann)

    def handle_tool_activated(self, btn: QToolButton, checked: bool): #checked: bool, tool_id: int):
        print(f'{"activating" if checked else "deactivating"} tool id {self._tools_button_group.id(btn)}')
        tool_id = self._tools_button_group.id(btn)
        if checked:
            if self._current_tool is not None:
                self._current_tool.show_announcement.disconnect(self._set_tool_announcement)
                self._current_tool.deactivate()
                self.image_viewer.photo_view.view_changed.disconnect(self._current_tool.handle_graphics_view_changed)
            for btn_ in self._tools_button_group.buttons():
                if btn == btn_:
                    continue
                btn_.setChecked(False)
            self._current_tool = self._tools_[tool_id].tool
            self._current_tool.show_announcement.connect(self._set_tool_announcement)
            self._current_tool.set_annotation_delegates(self._annotation_delegates)
            self.image_viewer.photo_view.view_changed.connect(self._current_tool.handle_graphics_view_changed)
            self.tool_out_widget.setVisible(self._current_tool.set_out_widget(self.tool_out_widget))
            if self.state.colormap is not None:
                self._current_tool.color_map_changed(self.state.colormap)
            self.image_viewer.set_tool(self._current_tool)
            if self._current_tool.setting_widget is not None:
                self.tool_settings.setVisible(True)
                if self._current_tool_widget is not None:
                    self._current_tool_widget.setVisible(False)
                    self.tool_settings.layout().removeWidget(self._current_tool_widget)
                self._current_tool_widget = self._current_tool.setting_widget
                self.tool_settings.layout().addWidget(self._current_tool_widget)
                self.tool_settings.setVisible(True)
                self._current_tool_widget.setVisible(True)
            else:
                self.tool_settings.setVisible(False)
            self.image_viewer.photo_view.left_side_panel.set_widget(self._current_tool.left_side_panel_widget())
            self.image_viewer.photo_view.right_side_panel.set_widget(self._current_tool.right_side_panel_widget())
            self._current_tool.activate(self.viz_layer)
            self._current_tool.switch_to_photo(self.state.current_photo)
            self.image_viewer.photo_view.set_should_autoscroll(True)
            self.image_viewer.photo_view.set_autoscroll_with_left_button_released(self._current_tool.should_auto_scroll_with_left_button_released())
            self.image_viewer.photo_view.set_autoscroll_distance(self._current_tool.get_auto_scroll_distance())
        else:
            self._current_tool.deactivate()
            self._current_tool = None
            self.image_viewer.set_tool(None)
            self._tool_param_widgets[tool_id].setVisible(False)
            self.tool_settings.setVisible(False)
            self.tool_out_widget.setVisible(False)
            self.image_viewer.photo_view.set_should_autoscroll(False)
            self.image_viewer.photo_view.set_autoscroll_with_left_button_released(False)
        self.tool_settings.update()

    def handle_label_changed(self, command: Optional[CommandEntry]):
        if command is None:
            return
        command.image_name = self.state.current_photo.image_name
        commands = [command]

        command.old_approval = self.state.current_photo.approved[self.state.current_label_name]
        lab_hier = self.state.label_hierarchy
        current_level = self.state.current_label_level
        level_names = [level.name for level in lab_hier.hierarchy_levels]
        approval_level = -1 if self.state.current_photo.approved[self.state.current_label_name] is None else level_names.index(self.state.current_photo.approved[self.state.current_label_name])
        if current_level <= approval_level:
            self.remove_approval2(level_names[current_level])
        command.new_approval = self.state.current_photo.approved[self.state.current_label_name]
        self.cmd_executor.undo_manager.current_undo_redo.clear_redo()
        self.cmd_executor.do_commands(commands)

    def handle_label_image_changed(self, image_name: str, label_name: str):
        if image_name != self.state.current_photo.image_name and label_name != self.state.current_label_name:
            return

    def handle_undo_clicked(self):
        self.reset_tool()
        undo_stack = self.undo_manager.current_undo_redo.undo_stack
        if (cmd := undo_stack[-1][0]).command_kind == CommandKind.LabelImgChange:
            if cmd.label_name != self.state.current_label_name:
                btn: QRadioButton = next(filter(lambda btn: btn.objectName() == cmd.label_name, self._label_types_btn_group.buttons()))
                btn.animateClick() #(1)
                return
        commands = undo_stack.pop()
        self.cmd_executor.do_commands(commands)
        if len(undo_stack) == 0:
            self.undo_action.setText('Undo')
            self.enable_undo_action(False, '')
        else:
            self.undo_action.setText(f'Undo {undo_stack[-1][0].source}')
        self.redo_action.setText(f'Redo {commands[0].source}')

        self.label_layer.set_label_name(self.state.current_label_name)

    def enable_undo_action(self, enable: bool, command_name: str):
        self.undo_action.setEnabled(enable)
        if enable:
            self.undo_action.setText(f'Undo {command_name}')
            self.ui.tbtnUndo.setToolTip(f'Undo {command_name}')
        self.ui.tbtnUndo.setEnabled(enable)

    def enable_redo_action(self, enable: bool, command_name: str):
        self.redo_action.setEnabled(enable)
        if enable:
            self.undo_action.setText(f'Redo {command_name}')
            self.ui.tbtnRedo.setToolTip(f'Redo {command_name}')
        self.ui.tbtnRedo.setEnabled(enable)

    def handle_redo_clicked(self):
        self.reset_tool()
        redo_stack = self.undo_manager.current_undo_redo.redo_stack
        if (cmd := redo_stack[-1][0]).command_kind == CommandKind.LabelImgChange:
            if cmd.label_name != self.state.current_label_name:
                btn: QRadioButton = next(filter(lambda btn: btn.objectName() == cmd.label_name, self._label_types_btn_group.buttons()))
                btn.animateClick() #(1)
                return
        commands = redo_stack.pop()
        self.cmd_executor.do_commands(commands)
        if len(redo_stack) == 0:
            self.redo_action.setText('Redo')
            self.enable_redo_action(False, '')
        else:
            self.redo_action.setText(f'Redo {redo_stack[-1][0].source}')
        self.undo_action.setText(f'Undo {commands[0].source}')
        self.label_layer.set_label_name(self.state.current_label_name)

    def _handle_primary_label_changed(self, label: int, old_label: int):
        if self.state.storage is None:
            return
        if label > 0:
            lab_hier = self.state.label_hierarchy
            label_level = lab_hier.get_level(label)

            label_node = lab_hier[label]
            label_level_to_visualize = label_level if len(label_node.children) > 0 else len(lab_hier.hierarchy_levels) - 1
            old_label_level = lab_hier.get_level(old_label)
            if label_level_to_visualize != old_label_level or old_label == 0:
                self.visualize_label_level(label_level_to_visualize)
        if self.state.redraw_canvas:
            self.label_layer.handle_primary_label_changed()
        # TODO this `if` prevents the code below
        if self._current_tool is None:
            return
        self._current_tool.update_primary_label(label)
        self.viz_layer.set_tool(self._current_tool)

    def _handle_tool_cursor_changed(self, tool_id: int):
        pass
        # if self._current_tool.tool_id == tool_id:
        #     self.image_viewer.set_tool(self._tools[tool_id])

    def handle_label_level_changed(self, level: int):
        old_redraw = self.state.redraw_canvas
        self.state.redraw_canvas = False
        self.state.current_label_level = level
        self.label_layer.switch_label_level(level)
        self.state.redraw_canvas = old_redraw and True

    def visualize_label_level(self, level: int):
        self.state.current_label_level = level
        self.label_layer.switch_label_level(level)

    def handle_label_picked(self, label: int):
        level = self.state.label_hierarchy.get_level(label)
        if self.state.current_label_level != level:
            self._label_switch._buttons[level].animateClick(1)
        self.colormap_widget.handle_label_picked(label)

    def handle_storage_changed(self, storage: Storage, old_storage: typing.Optional[Storage]):
        self._label_tree_model.beginResetModel()
        self._label_tree_model.show_hierarchy_for(storage.default_label_image)
        for btn in self._label_types_btn_group.buttons():
            btn.setVisible(False)
            self.ui.MaskGroup.layout().removeWidget(btn)
            self._label_types_btn_group.removeButton(btn)
        self.ui.MaskGroup.update()
        for i, label_name in enumerate(sorted(storage.label_image_names)):
            btn = QRadioButton(label_name)#QPushButton(label_name)
            btn.setObjectName(label_name)
            btn.setCheckable(True)
            if label_name == self.state.storage.default_label_image:
                btn.setChecked(True)
            btn.setAutoExclusive(True)
            self.ui.MaskGroup.layout().addWidget(btn)
            self._label_types_btn_group.addButton(btn, i)
        self.state.current_label_name = self.state.storage.default_label_image
        self._update_editing_constraint_label()
        self.ui.MaskGroup.setEnabled(True)
        self._label_tree_model.endResetModel()
        self._label_tree.setModel(self._label_tree_model)
        self._label_tree.expandAll()
        self._label_tree.resizeColumnToContents(0)

        self.undo_manager.initialize(self.state.storage)
        self.image_viewer.set_storage(self.state.storage)
        self.adjust_level_approval_switch_width()

    def handle_label_type_button_clicked(self, btn: QAbstractButton):
        # TODO This is only a temporary fix for Issue #23
        if btn.text() == self.state.current_label_name:
            return
        label_image_info = self.state.project.label_images_info[btn.text()]
        self.switch_label_type(label_image_info)

    def switch_label_type(self, label_img_info: LabelImgInfo):
        label_name = label_img_info.name
        self.reset_tool()
        self._label_tree_model.beginResetModel()
        self._label_tree_model.show_hierarchy_for(label_name)
        old_redraw = self.state.redraw_canvas
        self.state.redraw_canvas = False
        self.state.current_label_name = label_name
        self._label_switch.set_label_hierarchy(
            self.state.storage.get_label_hierarchy(self.state.current_label_name)
        )
        self.adjust_level_approval_switch_width()

        approved_level = self.state.current_photo.approved[self.state.current_label_name]

        self.approve_level(approved_level)

        hide = set(self.state.current_photo.label_image_info.keys())
        hide.remove(label_name)
        if self.state.current_photo is None:
            logging.info(f'LE - state.current_photo is None, returning')
            return
        lbl_img = self.state.current_photo[label_name]
        self.state.label_img = lbl_img

        self.cmd_executor.enforce_within_mask(self.state.current_photo, self.state.current_label_name)

        self.label_layer.set_label_name(label_name)

        self.state.redraw_canvas = old_redraw and True
        self._label_tree_model.endResetModel()
        self._label_tree.expandAll()
        self._label_tree.resizeColumnToContents(0)
        index = self._label_tree_model.find_index(self.state.primary_label)
        self._label_tree.setModel(self._label_tree_model)
        self._label_tree.selectionModel().setCurrentIndex(index,
                                                          QItemSelectionModel.Select)
        self._label_tree._handle_index_activated(index)
        self._update_editing_constraint_label()

        enable_undo, enable_redo = self.undo_manager.current_undo_redo.has_commands()

        if enable_undo:
            undo_command = self.undo_manager.current_undo_redo.undo_stack[-1][0].source
        else:
            undo_command = ''

        if enable_redo:
            redo_command = self.undo_manager.current_undo_redo.redo_stack[-1][0].source
        else:
            redo_command = ''

        self.enable_undo_action(enable_undo, undo_command)
        self.enable_redo_action(enable_redo, redo_command)

        # TODO scenario - set a constraint and label in Labels, switch to Reflections, switch back to Labels, and I'm not able to draw withing 'Animal'
        # Ad above TODO - can't reproduce that scenario
        # This is to constrain the current label image to another label image (e.g. Reflections should be constrained withing 'specimen' region of 'Labels')

        # Check if the label image has to be constrained to some other Label, if not, then check if there is an existing
        # constraint from before

        if len(label_img_info.constrain_to) > 0:  # constrain to a different label image
            constraint_label_name = next(iter(label_img_info.constrain_to.keys()))
            constrain_hierarchy = self.state.project.label_images_info[constraint_label_name].label_hierarchy
            constrain_region_path = list(label_img_info.constrain_to.values())[0][0] # TODO for now
            constrain_region_node = constrain_hierarchy[constrain_region_path]

            constraint = LabelConstraint(constraint_label_name)
            constraint.label_node = constrain_region_node

            self.state.current_constraint = constraint
        elif self.state.current_constraint.constraint_label_name == self.state.current_label_name:
            if self.state.current_constraint.label_node is not None:
                index = self._label_tree_model.find_index(self.state.current_constraint.label_node.label).siblingAtColumn(1)
                self._label_tree.set_constraint(index)

    def _update_editing_constraint_label(self):
        if (lbl_info := self.state.storage.label_img_info[self.state.current_label_name]).constrain_to.__len__() > 0:
            # constr_lab_hier = self.state.storage.get_label_hierarchy(lbl_info.constrain_to)
            constraint_label_name: str = next(iter(lbl_info.constrain_to.keys()))
            constrain_label_info = self.state.project.label_images_info[constraint_label_name]
            constr_lab_hier = constrain_label_info.label_hierarchy
            constrain_to_region_code: str = lbl_info.constrain_to[constraint_label_name][0]
            constraint_node = constr_lab_hier.nodes_dict[constrain_to_region_code]
            self._label_constraint_label.setText(f'Editing constrained to {constraint_label_name} - {constraint_node.name}')
        else:
            self._label_constraint_label.setText("")

    def _toggle_approval_of_mask(self):
        lab_hier = self.state.storage.get_label_hierarchy(self.state.current_label_name)
        recent_approval = self.state.current_photo.approved[self.state.current_label_name]

        level_names = [level.name for level in lab_hier.hierarchy_levels]
        recent_approval_index = -1 if recent_approval is None else level_names.index(recent_approval)

        level_name = level_names[self.state.current_label_level]
        level_name_index = level_names.index(level_name)
        if level_name_index <= recent_approval_index:
            self.remove_approval_for(level_name)
        else:
            self.approve_level(level_name)
        self.approval_changed.emit(self.state.current_photo)

    def remove_approval_for(self, level_name: str):
        lab_hier = self.state.project.label_images_info[self.state.current_label_name].label_hierarchy
        level_names = [level.name for level in lab_hier.hierarchy_levels]

        index = level_names.index(level_name)
        for i in range(len(level_names)):
            self._label_switch.mark_approved(i, False)
        demote_to = None
        if index > 0:
            demote_to = level_names[index-1]
        self.approve_level(demote_to)

    def remove_approval2(self, level_name: str):
        if level_name is None or level_name == '':
            return
        lab_hier = self.state.project.label_images_info[self.state.current_label_name].label_hierarchy
        level_names = [level.name for level in lab_hier.hierarchy_levels]

        index = level_names.index(level_name)
        for i in range(len(level_names) - 1, index-1, -1):
            self._label_switch.mark_approved(i, False)
        demote_to = None
        if index > 0:
            demote_to = level_names[index-1]
        self.state.current_photo.approved[self.state.current_label_name] = demote_to
        self.approval_changed.emit(self.state.current_photo)

    def approve_level(self, level_name: str):
        lab_hier = self.state.project.label_images_info[self.state.current_label_name].label_hierarchy
        level_names = [level.name for level in lab_hier.hierarchy_levels]

        for i in range(len(level_names)):
            self._label_switch.mark_approved(i, False)
        self.state.current_photo.approved[self.state.current_label_name] = level_name
        lab_hier = self.state.storage.get_label_hierarchy(self.state.current_label_name)
        if level_name is not None and level_name != '':
            index = level_names.index(level_name)
            for i, name in enumerate(level_names[:index+1]):
                self._label_switch.mark_approved(i, True)
        else:
            for i in range(len(level_names)):
                self._label_switch.mark_approved(i, False)
        self.approval_changed.emit(self.state.current_photo)

    def toggle_approval_for(self, level_idx: int, approved: bool):
        lab_hier = self.state.project.label_images_info[self.state.current_label_name].label_hierarchy
        level_names = [level.name for level in lab_hier.hierarchy_levels]

        level_name = level_names[level_idx]
        if approved:
            self.approve_level(level_name)
        else:
            self.remove_approval2(level_name)

    def handle_approval_changed(self, image_name: str, label_name: str, approval: Optional[str]):
        approval = None if approval == '' else approval
        photo = self.state.storage.get_photo_by_name(image_name, load_image=False)
        if image_name == self.state.current_photo.image_name:
            self.approve_level(approval)
        else:
            photo.approved[label_name] = approval

    def reset_tool(self):
        if self._current_tool is not None:
            self._current_tool.reset_tool()
        self.viz_layer.reset()

    def release_resources(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _handle_label_color_changed(self, label: int, color: QColor):
        self.state.colormap[label] = color.toTuple()[:3]
        self.label_layer._recolor_image()

    def _handle_label_node_modified(self, label: int, name: str, color: QColor):
        code = self.state.label_hierarchy.code(label)
        label_node: Node = self.state.label_hierarchy.nodes_dict[code]
        label_node.name = name
        if color.isValid():
            label_node.color = color.toTuple()[:3]
            self.state.colormap[label] = label_node.color
            self.label_layer._recolor_image()
        index = self._label_tree_model.find_index(label)
        self._label_tree_model.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.DecorationRole])

    def modify_label_node(self, node: Node):
        self._setup_new_label_dialog()
        self._new_label_dialog.modify_label(node.label)

    def _add_new_label(self):
        self._setup_new_label_dialog()
        node: Node = self._label_context_action_add.data()
        self._new_label_dialog.add_new_label(node.label)

    def handle_new_label_requested(self, parent: int, name: str, color: QColor):
        if parent >= 0:
            parent_index = self._label_tree_model.find_index(parent)
            parent_node: Node = parent_index.internalPointer()
        else:
            parent_index = QModelIndex()
            parent_node: Node = self.state.label_hierarchy.nodes_flat[-1]

        added_label: Node = self.state.label_hierarchy.add_child_label(parent_node, name, color.toTuple()[:3])
        row = len(parent_node.children) - 1
        self._label_tree_model.beginInsertRows(parent_index, row, row)
        self._label_tree_model.insertRow(row, parent_index)
        self._label_tree_model.endInsertRows()
        new_index = self._label_tree_model.find_index(added_label.label)
        self._label_tree_model.dataChanged.emit(new_index, new_index)
        if parent_index.isValid():
            self._label_tree.expand(parent_index)

    def move_constraint_up(self, label: int):
        curr_constraint_node = self.state.current_constraint.label_node

        const_parent = curr_constraint_node.parent
        if const_parent == -1:
            self._label_tree._unset_constraint(set_constraint_button=False)
        else:
            index = self._label_tree_model.find_index(const_parent.label).siblingAtColumn(1)
            self._label_tree.set_constraint(index)

    def move_constraint_down(self, label: int):
        ancestors = list(reversed(self.state.label_hierarchy.get_ancestors(label)))
        ancestors.append(label)
        curr_const_level = self.state.label_hierarchy.get_level(self.state.current_constraint.label)
        if curr_const_level + 1 > self.state.label_hierarchy.get_level(label):
            return
        index = self._label_tree_model.find_index(ancestors[curr_const_level + 1]).siblingAtColumn(1)
        self._label_tree.set_constraint(index)

    def cycle_constraint(self, label: int, direction: int):
        ancestors = list(reversed(self.state.label_hierarchy.get_ancestors(label)))
        ancestors.append(label)
        ancestors.append(0)
        if self.state.current_constraint.label > 0:
            curr_const_level = self.state.label_hierarchy.get_level(self.state.current_constraint.label)
        else:
            curr_const_level = -1
        next_constraint = ancestors[(curr_const_level + direction) % len(ancestors)]
        if next_constraint == 0:
            self._label_tree._unset_constraint(set_constraint_button=False)
        else:
            index = self._label_tree_model.find_index(next_constraint).siblingAtColumn(1)
            self._label_tree.set_constraint(index)

    def disable(self):
        self.enable_undo_action(False, '')
        self.enable_redo_action(False, '')
        self.image_viewer.setEnabled(False)
        self._label_tree.setEnabled(False)
        self.region_computation_widget.setEnabled(False)
        self.tool_box.setEnabled(False)

    def enable(self):
        self.image_viewer.setEnabled(True)
        self._label_tree.setEnabled(True)
        self.region_computation_widget.setEnabled(True)
        self.tool_box.setEnabled(True)
