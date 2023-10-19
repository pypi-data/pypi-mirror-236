import typing
from dataclasses import dataclass
from typing import Dict

import PySide6
import numpy as np
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QTransform

from maphis.common.label_hierarchy import LabelHierarchy, Node
from maphis.common.label_image import LabelImg
from maphis.common.local_storage import Storage
from maphis.common.photo import Photo
from maphis.common.storage import StorageUpdate
from maphis.common.units import UnitStore
from maphis.image_list_model import ImageListSortFilterProxyModel
from maphis.label_editor.new_label_dialog import NewLabelDialog
from maphis.project.annotation import Annotation, Keypoint
from maphis.project.project import Project


class LabelConstraint(QObject):
    constraint_changed = Signal('LabelConstraint')

    def __init__(self, label_name: str, parent: typing.Optional[PySide6.QtCore.QObject] = None):
        super().__init__(parent)

        self.label_name: str = label_name
        self._constraint_label_name: typing.Optional[str] = label_name
        self.label_level: int = 0
        self._label_node: typing.Optional[Node] = None
        self.primary_label: int = 0

    @property
    def constraint_label_name(self) -> typing.Optional[str]:
        return self._constraint_label_name

    @constraint_label_name.setter
    def constraint_label_name(self, lab_name: typing.Optional[str]):
        self._constraint_label_name = lab_name
        # self.constraint_changed.emit(self)

    @property
    def label_node(self) -> typing.Optional[Node]:
        return self._label_node

    @label_node.setter
    def label_node(self, label_node: typing.Optional[Node]):
        self._label_node = label_node
        # self.constraint_changed.emit(self)

    @property
    def label(self) -> int:
        return 0 if self._label_node is None else self._label_node.label


class LabelState:
    def __init__(self, label_name: str):
        self._label_name: str = label_name
        self.current_label: int = 0
        self.current_level: int = 0
        self.constraint: LabelConstraint = LabelConstraint(self._label_name)

    @property
    def label_name(self) -> str:
        return self._label_name


class State(QObject):
    colormap_changed = Signal(Dict[int, typing.Tuple[int, int, int]])
    storage_changed = Signal(Storage, Storage)
    photo_changed = Signal(Photo)
    photo_index_changed = Signal(int)
    label_img_changed = Signal(LabelImg)
    label_hierarchy_changed = Signal(LabelHierarchy)
    label_constraint_changed = Signal(LabelConstraint)
    update_used_label_list = Signal()
    new_label_constraint = Signal(LabelConstraint)
    primary_label_changed = Signal(int, int)
    tags_filter_changed = Signal(list)
    annotation_selected = Signal(Annotation)
    keypoint_selected = Signal(Annotation, Keypoint)

    def __init__(self, parent: QObject = None):
        from maphis.common.tool import Tool
        QObject.__init__(self, parent=parent)
        self._project: typing.Optional[Project] = None
        self._storage: typing.Optional[Storage] = None
        self.image_list_model: typing.Optional[ImageListSortFilterProxyModel] = None
        self._current_photo: typing.Optional[Photo] = None
        self._current_photo_idx: int = -1
        self._current_label_img: typing.Optional[LabelImg] = None
        self._primary_label: int = 0
        self._secondary_label: int = 0
        self._label_hierarchy: typing.Optional[LabelHierarchy] = None
        # self.current_label_level: int = 0
        self._current_label_name: str = ''
        self._label_constraint: LabelConstraint = None
        self.redraw_canvas: bool = True
        self._constraint_label: int = 0
        self.constraints: Dict[str, LabelConstraint] = {}
        self.label_states: Dict[str, LabelState] = {}
        self.units: UnitStore = UnitStore()
        #self.viz_layer: typing.Optional[VisualizationLayer] = None
        # self.key_modifier: typing.Optional[Qt.Key] = None
        self.current_tool: typing.Optional[Tool] = None
        self.current_view_transform: QTransform = QTransform()

        self._active_tags_filter: typing.List[str] = []
        self._hidden_photos_count: int = 0
        self.plugin_store: typing.Optional['PluginStore'] = None

    @property
    def colormap(self) -> typing.Optional[Dict[int, typing.Tuple[int, int, int]]]:
        if self._storage is None:
            return None
        return self.storage.get_label_hierarchy(self.current_label_name).colormap

    @property
    def project(self) -> Project:
        return self._project

    @project.setter
    def project(self, project: Project):
        self._project = project
        self.storage = self._project.storage

    @property
    def storage(self) -> Storage:
        return self._storage

    @storage.setter
    def storage(self, storage: Storage):
        old_storage = self._storage
        self._storage = storage
        # This if should not be necessary
        #if self._storage.label_hierarchy is None:
        #    self._storage.label_hierarchy = self._label_hierarchy
        self.constraints.clear()
        if self._storage is None:
            return
        for label_name in self._storage.label_image_names:
            lab_state = LabelState(label_name)
            # constr = LabelConstraint(label_name)
            # self.constraints[label_name] = constr
            self.label_states[label_name] = lab_state
        self._current_label_name = self._storage.default_label_image
        self.label_hierarchy = self._storage.get_label_hierarchy(self.current_label_name)
        if self.label_hierarchy is not None:
            self.current_label_level = len(self.label_hierarchy.hierarchy_levels) - 1
        self.storage_changed.emit(self._storage, old_storage)
        self._storage.storage_update.connect(self._handle_storage_update)

    @property
    def current_photo(self) -> Photo:
        return self._current_photo

    @current_photo.setter
    def current_photo(self, photo: Photo):
        self._current_photo = photo
        self.photo_changed.emit(self._current_photo)

    @property
    def current_photo_index(self) -> int:
        return self._current_photo_idx

    @current_photo_index.setter
    def current_photo_index(self, idx: int):
        self._current_photo_idx = idx
        self.current_photo = self.storage.get_photo_by_idx(self._current_photo_idx)
        self.photo_index_changed.emit(self._current_photo_idx)

    @property
    def label_img(self) -> LabelImg:
        return self._current_label_img

    @label_img.setter
    def label_img(self, _label_img: LabelImg):
        self._current_label_img = _label_img
        if self.colormap is not None:
            #ulabels = set(list(np.unique(self._current_photo.regions_image.label_img)))
            ulabels = set(list(np.unique(self._current_photo[self.current_label_name].label_image)))
            # TODO REMOVE
            #self.colormap._used_labels = ulabels
            self.update_used_label_list.emit()
        self.label_img_changed.emit(self._current_label_img)

    @property
    def primary_label(self) -> int:
        # return self.constraints[self.current_label_name].primary_label
        return self.label_states[self.current_label_name].current_label

    @primary_label.setter
    def primary_label(self, label: int):
        # self.constraints[self.current_label_name].primary_label = label
        # Check if the chosen label is present in the current label hierarchy
        code = self.label_hierarchy.code(label)
        if code in self.label_hierarchy.nodes_dict:
            old_label = self.label_states[self.current_label_name].current_label
            self.label_states[self.current_label_name].current_label = label
            self.primary_label_changed.emit(label, old_label)

    @property
    def secondary_label(self) -> int:
        return self._secondary_label

    @secondary_label.setter
    def secondary_label(self, label: int):
        self._secondary_label = label

    @property
    def label_hierarchy(self) -> LabelHierarchy:
        if self.storage is None or self.project is None:
            return None
        # return self.storage.get_label_hierarchy(self.current_label_name)
        return self.project.label_images_info[self.current_label_name].label_hierarchy

    @label_hierarchy.setter
    def label_hierarchy(self, lab_hier: LabelHierarchy):
        self._label_hierarchy = lab_hier
        if self._storage is not None:
            self._storage.label_hierarchy = lab_hier
        self.label_hierarchy_changed.emit(self._label_hierarchy)

    @property
    def current_label_name(self) -> str:
        return self._current_label_name

    @current_label_name.setter
    def current_label_name(self, lab_name: str):
        self._current_label_name = lab_name
        if self._current_label_name != '':
            self._label_constraint = self.label_states[lab_name].constraint
            lbl_info = self.storage.label_img_info[self._current_label_name]
            if lbl_info.can_be_constrained:
                if len(lbl_info.constrain_to) > 0:
                    constrain_label_name, regions = next(iter(lbl_info.constrain_to.items()))
                    # self.current_constraint.label_name = constrain_label_name
                    constr_lab_hier = self.project.label_images_info[constrain_label_name].label_hierarchy
                    # self.current_constraint.label_node = constr_lab_hier[regions[0]]
                    new_constraint = LabelConstraint(constrain_label_name)
                    new_constraint.label_node = constr_lab_hier[regions[0]]
                    self.current_constraint = new_constraint
                    # self.constraint_label = self.current_constraint.label_node.label
                    # self.current_constraint.label_node = self
                # else:
                #     # TODO maybe restore the latest constraint for the particular image:label combination?
                #     self.current_constraint.label_name = None
                #     self.current_constraint.label_node = None
                #     self.current_constraint.label_level = -1
                # elif lbl_info.can_constrain_to is not None:
                #     self.current_constraint.label_name = lbl_info.can_constrain_to[0]
            # TODO maybe emit a signal

    @property
    def current_constraint(self) -> LabelConstraint:
        return self.label_states[self.current_label_name].constraint

    @current_constraint.setter
    def current_constraint(self, constraint: LabelConstraint):
        self.label_states[self.current_label_name].constraint = constraint
        self.new_label_constraint.emit(self.current_constraint)

    @property
    def constraint_label(self) -> int:
        return self.current_constraint.label

    @constraint_label.setter
    def constraint_label(self, label: int):
        pass
        # self._constraint_label = label
        # self.current_constraint.label_node = self.label_hierarchy[label]
        # #print('emitting')
        # if self.storage.image_count > 0 and self.current_photo is not None:
        #     self.new_label_constraint.emit(self.current_constraint.label_node.label)

    @property
    def label_can_be_constrained(self) -> bool:
        if self.storage is None:
            return False
        return self.storage.label_img_info[self.current_label_name].can_be_constrained

    def set_label_constraint(self, label_name: typing.Optional[str], emit: bool = False):
        if label_name == '':
            return
        if label_name is None or label_name == 'None':
            self.current_constraint.label_name = None
            self.set_level_constraint(-1, emit)
        else:
            self.current_constraint.label_name = label_name
            self.set_level_constraint(self.current_label_level - 1, emit)

    def set_level_constraint(self, label_level: int, emit: bool = False):
        self.current_constraint.label_level = label_level
        if emit:
            self.label_constraint_changed.emit(self.current_constraint)

    @property
    def current_label_level(self) -> int:
        return self.label_states[self.current_label_name].current_level

    @current_label_level.setter
    def current_label_level(self, level: int):
        if len(self.label_states) == 0:
            return
        self.label_states[self.current_label_name].current_level = level

    @property
    def active_tags_filter(self) -> typing.List[str]:
        return self._active_tags_filter

    @active_tags_filter.setter
    def active_tags_filter(self, tags: typing.Iterable[str]):
        self._active_tags_filter = list(sorted(tags))
        self._update_hidden_photos_count()
        self.tags_filter_changed.emit(self._active_tags_filter)

    def set_active_tags_filter(self, tags: typing.Iterable[str]):
        self.active_tags_filter = tags

    def add_filtering_tag(self, tag: str):
        self._active_tags_filter.append(tag)
        self._active_tags_filter = list(sorted(set(self._active_tags_filter)))
        self._update_hidden_photos_count()
        self.tags_filter_changed.emit(self._active_tags_filter)

    def remove_filtering_tag(self, tag: str):
        if tag not in self._active_tags_filter:
            return
        self._active_tags_filter.remove(tag)
        self._update_hidden_photos_count()
        self.tags_filter_changed.emit(self._active_tags_filter)

    def toggle_filtering_tag(self, tag: str, active: bool):
        if active:
            self._active_tags_filter.append(tag)
            self._active_tags_filter = sorted(self._active_tags_filter)
        else:
            self._active_tags_filter.remove(tag)
        self._update_hidden_photos_count()
        self.tags_filter_changed.emit(self._active_tags_filter)

    def clear_tag_filter(self):
        self._active_tags_filter.clear()
        self._update_hidden_photos_count()
        self.tags_filter_changed.emit(self._active_tags_filter)

    def _update_hidden_photos_count(self):
        shown_photos = self.storage.photos_satisfying_tags(set(self._active_tags_filter))
        self._hidden_photos_count = self.storage.image_count - len(shown_photos)

    def _handle_storage_update(self, update: StorageUpdate):
        for tag in update.tags_removed:
            self.remove_filtering_tag(tag)

    @property
    def hidden_photos_count(self) -> int:
        return self._hidden_photos_count

    def reset_state(self):
        self._project = None
        self.storage = None
        self.current_photo = None
        self.current_label_name = ''
        self.constraints = {}
        self.label_states = {}
