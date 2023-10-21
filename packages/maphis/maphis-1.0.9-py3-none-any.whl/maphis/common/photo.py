from __future__ import annotations

import abc
import dataclasses
import datetime
import time
import typing
from enum import IntEnum
from pathlib import Path
from typing import Dict, Optional

import PySide6
import cv2
import numpy as np
import pint
from PIL import Image
from PySide6.QtCore import QObject, QDateTime, Signal
from PySide6.QtGui import QImage
from skimage import io

from maphis.measurement.values import ScalarValue
from maphis.measurement.region_property import RegionProperty
from maphis.common.label_image import LabelImg, LabelImgInfo
from maphis.common.utils import ScaleSetting
from maphis.project.annotation import Annotation, AnnotationType


class UpdateContext(IntEnum):
    Photo = 0,
    LabelImg = 1,
    Measurements = 2,
    Storage = 3,


class PhotoUpdateType(IntEnum):
    Resize = 0,
    Rotate90CW = 1,
    Rotate90CCW = 2,
    ScaleSet = 3,
    TagsUpdated = 4,


@dataclasses.dataclass
class PhotoUpdate:
    photo: Photo
    update_type: PhotoUpdateType
    data: typing.Dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    tags_added: typing.List[str] = dataclasses.field(default_factory=list)
    tags_removed: typing.List[str] = dataclasses.field(default_factory=list)


class LabelImageUpdateType(IntEnum):
    PropertyAdded = 0,
    PropertyUpdate = 1,
    PropertyRemoved = 2
    PropertiesInvalid = 3
    PropertiesValid = 4
    RegionsChanged = 5


@dataclasses.dataclass
class LabelImageUpdate:
    label_img: LabelImg
    update_type: LabelImageUpdateType
    properties_added: typing.List[RegionProperty] = dataclasses.field(default_factory=list)
    properties_removed: typing.List[RegionProperty] = dataclasses.field(default_factory=list)
    properties_updated: typing.List[RegionProperty] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UpdateEvent:
    photo: 'Photo'
    update_context: UpdateContext
    update_obj: PhotoUpdate | LabelImageUpdate


class Subscriber(QObject):
    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = None):
        super().__init__(parent)

    # def notify(self, img_name: str, ctx: UpdateContext, data: Optional[Dict[str, typing.Any]] = None):
    def notify(self, event: UpdateEvent):
        pass

    # def notify(self, event: UpdateEvent):
    #     pass


class Photo(QObject):
    """
    A base class representing a single photo. Provides access to the RGB/Grayscale pixel data for a photo as well as
    access to label images (`LabelImg`) associated with this Photo.
    This class acts only as the interface defining what the classes subclassing this class should implement.
    """

    AnnotationIndex = int

    new_annotation_added = Signal(AnnotationIndex, Annotation)
    annotation_deleted = Signal(AnnotationIndex, Annotation)

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

    @property
    @abc.abstractmethod
    def _subscriber(self) -> Subscriber:
        pass

    @property
    @abc.abstractmethod
    def image_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def image_path(self) -> Path:
        pass

    @image_path.setter
    @abc.abstractmethod
    def image_path(self, path: Path):
        return Path()

    @property
    @abc.abstractmethod
    def image(self) -> np.ndarray:
        """Returns the pixel data for the photo. Beware that the order of sizes returned by the property `image_size`
        (width, height) is different from the size stored in the `shape` (height, width, channels) tuple of the
        returned pixel data.

        Returns:
            the pixel data
        """
        pass

    @property
    @abc.abstractmethod
    def image_size(self) -> typing.Tuple[int, int]:
        """Returns the image size (width, height).

        Returns:
            the image size in (width, height) order.
        """
        pass

    @abc.abstractmethod
    def __getitem__(self, label_name: str) -> LabelImg:
        """Returns the `LabelImg` instance stored under `label_name`.

        Args:
            label_name (str): The name under which the `LabelImg` is stored

        Returns:
            a `LabelImg` instance

        Raises:
            KeyError: If no `LabelImg` is stored under `label_name`
        """
        pass

    @property
    @abc.abstractmethod
    def label_images_(self) -> Dict[str, LabelImg]:
        pass

    @property
    @abc.abstractmethod
    def label_image_info(self) -> Dict[str, LabelImgInfo]:
        """Returns a dict `label_name` -> `LabelImgInfo`.

        Returns:
            dictionary mapping label names to `LabelImgInfo` objects
        """
        pass

    @property
    def image_scale(self) -> Optional[pint.Quantity]:
        """Return image scale as `pint.Quantity` if set, otherwise `None`.

        Returns:
            the image scale if set, otherwise `None`.

        """
        return None

    @image_scale.setter
    def image_scale(self, scale: Optional[pint.Quantity]):
        """Sets the image scale.

        Args:
            scale (Optional[pint.Quantity]): optional image scale
        """
        pass

    @property
    def scale_setting(self) -> Optional[ScaleSetting]:
        return None

    @scale_setting.setter
    def scale_setting(self, setting: Optional[ScaleSetting]):
        pass

    # TODO rename this to 'approvals'
    @property
    def approved(self) -> Dict[str, Optional[str]]:
        pass

    @abc.abstractmethod
    def has_segmentation_for(self, label_name: str) -> bool:
        return False

    @abc.abstractmethod
    def rotate(self, ccw: bool):
        pass

    @abc.abstractmethod
    def resize(self, factor: float):
        pass

    @abc.abstractmethod
    def save(self):
        pass

    @property
    @abc.abstractmethod
    def has_unsaved_changes(self) -> bool:
        pass

    @property
    def tags(self) -> typing.Set[str]:
        return set()

    @tags.setter
    def tags(self, _tags: typing.Set[str]):
        pass

    def add_tag(self, tag: str):
        pass

    def remove_tag(self, tag: str):
        pass

    def toggle_tag(self, tag: str, enabled: bool):
        pass

    @property
    def thumbnail(self) -> typing.Optional[QImage]:
        return QImage()

    @thumbnail.setter
    def thumbnail(self, thumb: typing.Optional[QImage]):
        pass

    @property
    def import_time(self) -> QDateTime:
        return None

    @import_time.setter
    def import_time(self, _time: QDateTime):
        pass

    @property
    def annotations(self) -> typing.Dict[AnnotationType, typing.List[Annotation]]:
        return {}

    def get_annotations(self, ann_type: AnnotationType) -> typing.List[Annotation]:
        return []

    def insert_new_annotation(self, ann_type: AnnotationType, annotation: Annotation):
        pass

    def __hash__(self) -> int:
        return hash(self.image_path)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other)


# TODO move this in 'maphis.common' or use a function from the package nd2qimage
def nd2qimage(nd: np.ndarray) -> QImage:
    if nd.ndim == 3:
        # assume RGB888
        return QImage(nd.data, nd.shape[1], nd.shape[0], nd.strides[0], QImage.Format_RGB888)
    return QImage()

