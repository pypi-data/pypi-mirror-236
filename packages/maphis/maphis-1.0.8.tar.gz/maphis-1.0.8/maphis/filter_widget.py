import typing
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QLineEdit, QTextEdit, \
    QPushButton
from PySide6.QtCore import Signal, Slot, QPoint

from maphis.common.popup_widget import PopupWidget, PopupLocation
from maphis.photo_filter import PhotoFilter, FilterCollection


class FilterList(QLineEdit):
    hovered = PySide6.QtCore.Signal(QPoint)

    def __init__(self, placeholder: str, parent: typing.Optional[QWidget] = None):
        QLineEdit.__init__(self, parent)
        self.setReadOnly(True)
        self.setPlaceholderText(placeholder)
        # self.setAcceptRichText(True)
        self._filter_separator: str = ' & '

    def enterEvent(self, event: PySide6.QtGui.QEnterEvent):
        super().enterEvent(event)
        self.hovered.emit(event.pos())


class FilterWidget(QWidget):
    filter_by = Signal(list)

    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, f)

        self._filters: typing.Optional[FilterCollection] = None

        self._group_widgets: typing.Dict[str, QGroupBox] = {}

        self._container = QVBoxLayout()
        self._main_layout = QHBoxLayout()

        self._label = QLabel(text='Filters:')
        self._main_layout.addWidget(self._label)

        self._filter_list = FilterList('hover to select filters')
        self._main_layout.addWidget(self._filter_list)

        self._btnClear: QPushButton = QPushButton('Clear')
        self._btnClear.clicked.connect(self.clear_filters)
        self._main_layout.addWidget(self._btnClear)

        self._popup_filter_options: PopupWidget = PopupWidget(parent=self)
        self._popup_filter_options.setLayout(QVBoxLayout())
        self._popup_filter_options.setVisible(False)
        self._popup_filter_options.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)

        self._filter_list.hovered.connect(self.show_filter_popup)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._container.addLayout(self._main_layout)

        self.setLayout(self._container)

    def set_filters(self, filter_collection: FilterCollection):
        if self._filters is not None:
            self._filters.filter_added.disconnect(self.add_filter)
            self._filters.filter_toggled.disconnect(self.toggle_filter_group_box)
            self._filters.refresh_views.disconnect(self._rebuild_widgets)
        self._filters = filter_collection
        if self._filters is not None:
            self._filters.filter_added.connect(self.add_filter)
            self._filters.filter_toggled.connect(self.toggle_filter_group_box)
            self._filters.refresh_views.connect(self._rebuild_widgets)
            for filter in self._filters._filters.values():
                self.add_filter(filter)

    def _rebuild_widgets(self):
        for grp_box in self._group_widgets.values():
            grp_box.hide()
            self._popup_filter_options.layout().removeWidget(grp_box)
        self._group_widgets.clear()
        for filter in self._filters._filters.values():
            self.add_filter(filter)

    def toggle_filter_group_box(self, filter: PhotoFilter, enabled: bool):
        if filter.group not in self._group_widgets:
            return
        self._group_widgets[filter.group].setChecked(enabled)

    def show_filter_popup(self, pos: QPoint):
        p = self._popup_filter_options.rect().topRight()
        self._popup_filter_options.popup_location = PopupLocation.TopRight
        self._popup_filter_options.makePopup(self._filter_list, QPoint())
        self._popup_filter_options.show()
        self._popup_filter_options.adjustSize()
        for g in self._group_widgets.values():
            g.adjustSize()

    def add_filter(self, filter: PhotoFilter):
        if filter.group not in self._group_widgets:
            grp_box = QGroupBox(filter.group)
            grp_box.setCheckable(True)
            grp_box.setChecked(False)
            grp_box.setLayout(QVBoxLayout())
            grp_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self._group_widgets[filter.group] = grp_box

            def handle_group_box_toggled():
                def _toggle_filter(enabled: bool):
                    self._filters.set_filter_enabled(filter.group, enabled)
                return _toggle_filter

            grp_box.toggled.connect(handle_group_box_toggled())
            self._popup_filter_options.layout().addWidget(grp_box)

        filter.filter_updated.connect(self.update_filters)
        self._group_widgets[filter.group].layout().addWidget(filter.widget)
        self._group_widgets[filter.group].adjustSize()
        self._popup_filter_options.adjustSize()
        self._group_widgets[filter.group].setChecked(filter.is_on)


    def update_filters(self):
        filters: typing.List[PhotoFilter] = []
        self._filter_list.clear()
        filter_list_texts: typing.List[str] = []
        for filter in self._filters._filters.values():
            if filter.is_on and len(filter.representation) > 0:
                filter_list_texts.append(filter.representation)
        # for k, grp in self._group_widgets.items():
        #     if grp.isChecked():
        #         filters.append(self._filters[k])
        #         if len(filter_text := self._filters[k].representation) > 0:
        #             filter_list_texts.append(filter_text)
        self._filter_list.setText(self._filter_list._filter_separator.join(filter_list_texts))

        self.filter_by.emit(filters)

    def clear_filters(self):
        for grp in self._group_widgets.values():
            grp.setChecked(False)
