import typing
from typing import Optional

import PySide6.QtCore
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QButtonGroup, QSizePolicy

from maphis.common.photo import Photo
from maphis.common.storage import StorageUpdate
from maphis.project.project import Project
from maphis.tags_widget import TagsPopupPanel


class PhotoFilter(QObject):
    filter_updated = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.project: typing.Optional[Project] = None
        self.is_on: bool = False

    def initialize(self, project: Project):
        self.project = project

    def satisfies(self, photo: Photo) -> bool:
        return not self.is_on

    @property
    def group(self) -> str:
        return 'photo attributes'

    @property
    def representation(self) -> str:
        return ''

    @property
    def widget(self) -> typing.Optional[QWidget]:
        return None

    def clear_filter(self):
        pass

    def set_on(self, val: bool):
        self.is_on = val
        self.filter_updated.emit()

    def handle_storage_update(self, storage_update: StorageUpdate):
        pass


class TagFilter(PhotoFilter):
    def __init__(self):
        super().__init__()
        self._active_tags: typing.Set[str] = set()
        self._widget: TagsPopupPanel = TagsPopupPanel(in_group_box=False)
        self._widget.in_popup_mode = False
        self._widget.setVisible(True)
        self._widget.tags_selection_changed.connect(self._handle_tags_selection_changed)
        self._widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def initialize(self, project: Project):
        super().initialize(project)
        self._widget.populate(project)

    def satisfies(self, photo: Photo) -> bool:
        return (self.is_on and set(self._widget.get_active_tags()).issubset(photo.tags)) or not self.is_on

    @property
    def group(self) -> str:
        return 'Photo tags'

    @property
    def representation(self) -> str:
        return ' & '.join(self._widget.get_active_tags())

    @property
    def widget(self) -> typing.Optional[QWidget]:
        return self._widget

    @property
    def active_filter_tags(self) -> typing.List[str]:
        return self._widget.get_active_tags()

    def clear_filter(self):
        self._widget.clear_tags()

    def _handle_tags_selection_changed(self, tags: typing.List[str]):
        self._active_tags = set(tags)
        self.filter_updated.emit()

    def handle_storage_update(self, storage_update: StorageUpdate):
        self._widget.populate(self.project)
        self._active_tags.difference_update(storage_update.tags_removed)
        self._widget.update_tag_states(list(self._active_tags))


class HasScaleFilter(PhotoFilter):
    def __init__(self):
        super().__init__()
        self._widget = QWidget()
        self._widget.setLayout(QHBoxLayout())
        self._btnGroup: QButtonGroup = QButtonGroup()
        self._btnYes: QRadioButton = QRadioButton("Yes")
        self._btnNo: QRadioButton = QRadioButton("No")
        self._btnGroup.addButton(self._btnYes)
        self._btnGroup.addButton(self._btnNo)
        self._btnYes.setChecked(True)
        self._btnGroup.setExclusive(True)
        self._btnGroup.buttonClicked.connect(lambda _: self.filter_updated.emit())
        self._widget.layout().addWidget(self._btnYes)
        self._widget.layout().addWidget(self._btnNo)

    def initialize(self, project: Project):
        super().initialize(project)

    def satisfies(self, photo: Photo) -> bool:
        return (self.is_on and self._btnYes.isChecked() and photo.image_scale is not None or self._btnNo.isChecked() and photo.image_scale is None) or not self.is_on

    @property
    def group(self) -> str:
        return 'Is scale available?'

    @property
    def representation(self) -> str:
        return '*has scale*' if self._btnYes.isChecked() else '*no scale*'

    @property
    def widget(self) -> typing.Optional[QWidget]:
        return self._widget

    def clear_filter(self):
        super().clear_filter()


class HasSegmentationFilter(PhotoFilter):
    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self._widget: QWidget = QWidget()

    def initialize(self, project: Project):
        super().initialize(project)

    def satisfies(self, photo: Photo) -> bool:
        return super().satisfies(photo)

    @property
    def group(self) -> str:
        return super().group

    @property
    def representation(self) -> str:
        return super().representation

    @property
    def widget(self) -> typing.Optional[QWidget]:
        return super().widget

    def clear_filter(self):
        super().clear_filter()


class FilterCollection(QObject):
    filter_by = Signal(list)
    filters_updated = Signal()
    filter_added = Signal(PhotoFilter)
    filter_removed = Signal(PhotoFilter)
    filter_toggled = Signal(PhotoFilter, bool)
    refresh_views = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self._project: typing.Optional[Project] = None
        self._filters: typing.Dict[str, PhotoFilter] = {}

    def update(self):
        self.filter_by.emit(list(self._filters.values()))
        self.filters_updated.emit()

    def register_filter(self, filter: PhotoFilter):
        self._filters[filter.group] = filter

        filter.filter_updated.connect(self.update)
        self.filter_added.emit(filter)
        self.update()

    def unregister_filter(self, filter_group: str):
        if filter_group in self._filters:
            filter = self._filters[filter_group]
            filter.filter_updated.disconnect(self.update)
            del self._filters[filter_group]
            self.filter_removed.emit(filter)
            self.filter_by(list(self._filters.values()))

    def set_filter_enabled(self, filter_group: str, enabled: bool):
        if filter_group not in self._filters:
            return
        self._filters[filter_group].set_on(enabled)
        self.filter_toggled.emit(self._filters[filter_group], enabled)

    def set_project(self, project: Project):
        if self._project is not None:
            self._project.storage.storage_update.disconnect(self.handle_storage_update)
        self._project = project
        for f in self._filters.values():
            f.initialize(self._project)
        if self._project is not None:
            self._project.storage.storage_update.connect(self.handle_storage_update)

        self.refresh_views.emit()

    def handle_storage_update(self, storage_update: StorageUpdate):
        for f in self._filters.values():
            f.handle_storage_update(storage_update)

    def satisfies(self, photo: Photo) -> bool:
        return all([filter.satisfies(photo) for filter in self._filters.values()])
