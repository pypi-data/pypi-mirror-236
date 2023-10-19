import datetime
import functools
import os
import stat
from pathlib import Path
from typing import Dict

import typing

import cv2
import numpy as np
import pint
from PIL import Image
from PySide6.QtCore import QDateTime, QObject
from PySide6.QtGui import QImage
from skimage import io

from maphis.measurement.values import ScalarValue
from maphis.common.label_image import LabelImgInfo, LabelImg
from maphis.measurement.region_property import RegionProperty
from maphis.common.photo import Photo, Subscriber, UpdateContext, UpdateEvent, PhotoUpdate, \
    PhotoUpdateType, LabelImageUpdate, LabelImageUpdateType
from maphis.common.utils import ScaleSetting
from maphis.project.annotation import Annotation, AnnotationType


class LocalPhoto(Photo):

    def __init__(self, folder: Path, img_name: str, lbl_image_info: Dict[str, LabelImgInfo], subs: Subscriber, parent: typing.Optional[QObject] = None):
        super().__init__(parent)
        self._tags: typing.Set[str] = set()
        self._dirty_flag: bool = False
        self._image: typing.Optional[np.ndarray] = None
        self._image_path = folder / img_name
        self._bug_bbox: typing.Optional[typing.Tuple[int, int, int, int]] = None

        self._label_images: Dict[str, LabelImg] = {}
        self._label_image_info: Dict[str, LabelImgInfo] = lbl_image_info
        #self._label_image_types = lbl_image_types

        self._scale: typing.Optional[ScalarValue] = None
        self._scale_setting: typing.Optional[ScaleSetting] = ScaleSetting()

        self._import_time: QDateTime = QDateTime.currentDateTime()
        # print(f'{self.image_name} - {self._import_time}')

        self._lab_approvals: Dict[str, typing.Optional[str]] = {lbl_name: None for lbl_name in lbl_image_info.keys()}
        with Image.open(self._image_path) as im:
            self._image_size = im.size
            self._np_size = self._image_size[::-1]
            self.format = im.format

        # create the label images
        for lbl_name in self._label_image_info.keys():
            lbl_img = self[lbl_name]

        self._annotations: typing.Dict[AnnotationType, typing.List[Annotation]] = {}

        self.__subscriber: Subscriber = subs
        self._thumbnail: typing.Optional[QImage] = None

    @property
    def image(self) -> np.ndarray:
        if self._image is None:
            #self._image = io.imread(str(self._image_path))
            with Image.open(self._image_path) as im:
                self._image = np.asarray(im)
                # This is a workaround around RGBA images
                if self._image.ndim > 2 and self._image.shape[2] > 3:
                    self._image = self._image[:, :, :3]
        return self._image

    @property
    def image_name(self) -> str:
        return self._image_path.name

    @property
    def image_path(self) -> Path:
        return self._image_path

    @image_path.setter
    def image_path(self, path: Path):
        raise NotImplementedError('Changing path is not implemented')

    @property
    def image_size(self) -> typing.Tuple[int, int]:
        return self._image_size

    def __getitem__(self, lab_name: str) -> typing.Optional[LabelImg]:
        if lab_name not in self._label_images:
            lab_fname = self._image_path.name + '.tif'
            self._label_images[lab_name] = LabelImg.create2(self._image_path.parent.parent / lab_name / lab_fname,
                                                            self.image_size, label_info=self.label_image_info[lab_name],
                                                            label_name=lab_name)
            self._label_images[lab_name].property_removed.connect(self._handle_label_image_property_removed)
            self._label_images[lab_name].property_added.connect(self._handle_label_image_property_added)
            self._label_images[lab_name].properties_need_recomputation.connect(self._handle_properties_need_recomputation)
            self._label_images[lab_name].all_properties_valid.connect(self._handle_all_properties_valid)
        lab = self._label_images[lab_name]
        return lab

    @property
    def label_images_(self) -> Dict[str, LabelImg]:
        return self._label_images

    @property
    def label_image_info(self) -> Dict[str, LabelImgInfo]:
        return self._label_image_info

    @property
    def image_scale(self) -> typing.Optional[pint.Quantity]:
        return self._scale_setting.scale

    @image_scale.setter
    def image_scale(self, scale: typing.Optional[pint.Quantity]):
        self._scale_setting.scale = scale

    @property
    def scale_setting(self) -> typing.Optional[ScaleSetting]:
        return self._scale_setting

    @scale_setting.setter
    def scale_setting(self, setting: typing.Optional[ScaleSetting]):
        self._scale_setting = setting
        # self._subscriber.notify(self.image_name, UpdateContext.Photo, {'type': 'image_scale'})
        event = UpdateEvent(
            self,
            UpdateContext.Photo,
            PhotoUpdate(self, PhotoUpdateType.ScaleSet)
        )
        self._subscriber.notify(event)

    @property
    def approved(self) -> Dict[str, typing.Optional[str]]:
        return self._lab_approvals

    def rotate(self, ccw: bool):
        loaded = self._image is not None
        if not loaded:
            self._image = io.imread(str(self._image_path))
        if self.scale_setting is not None and self.scale_setting.scale_line is not None:
            mid = (round(self.image_size[0] * 0.5), round(self.image_size[1] * 0.5))
            self.scale_setting.scale_line.rotate(ccw, mid)
        self._image = cv2.rotate(self._image, cv2.ROTATE_90_COUNTERCLOCKWISE if ccw else cv2.ROTATE_90_CLOCKWISE) #skimage.transform.rotate(self._image, 90 * (-1 if ccw else 1), order=2)
        self._image = np.ascontiguousarray(self._image, dtype=self._image.dtype)
        self._dirty_flag = True
        self._np_size = self._image.shape[:2]
        self._image_size = self._np_size[::-1]
        for lab_img in self._label_images.values():
            lab_img.rotate(ccw)
        if not loaded:
            self.save()
            self._image = None
        self.save()
        # self.__subscriber.notify(self.image_name, UpdateContext.Photo, {'operation':
        #                                                                     'rot_90_ccw' if ccw else 'rot_90_cw'})
        event = UpdateEvent(self, UpdateContext.Photo,
                            PhotoUpdate(self, PhotoUpdateType.Rotate90CCW if ccw else PhotoUpdateType.Rotate90CW))
        self.__subscriber.notify(event)

    def resize(self, factor: float):
        loaded = self._image is not None
        print(f'resizing with factor {factor}')
        # TODO adapt measurements, or at least signal that the measurements are not up-to-date anymore!
        if self._scale_setting is not None and self._scale_setting.scale is not None:
            # print(f'changing scale from {self._scale} to {self._scale * factor}')
            self._scale_setting.scale *= factor
        if not loaded:
            self._image = io.imread(str(self._image_path))
        self._dirty_flag = True
        im = Image.fromarray(self._image)
        print(f'old size is {self._image_size}')
        size = (int(round(factor * self._image_size[0])),
                int(round(factor * self._image_size[1])))
        self._image_size = size
        print(f'new size if {self._image_size}')
        self._np_size = self._image_size[::-1]
        im = im.resize(self._image_size, resample=2)
        self._image = np.asarray(im)
        for lbl_img in self._label_images.values():
            lbl_img.resize(factor)
        if not loaded:
            self.save()
            self._image = None
        if self.scale_setting is not None and self.scale_setting.scale_line is not None:
            mid = (round(self.image_size[0] * 0.5), round(self.image_size[1] * 0.5))
            self.scale_setting.scale_line.scale(factor, (0, 0))

        # self.__subscriber.notify(self.image_name, UpdateContext.Photo,
        #                          {'operation': 'resize',
        #                           'factor': factor})
        event = UpdateEvent(self, UpdateContext.Photo,
                            PhotoUpdate(self, PhotoUpdateType.Resize, data={'factor': factor}))
        self.__subscriber.notify(event)

    def save(self):
        if self.has_unsaved_changes:
            if self._dirty_flag:
                if self._image is not None:
                    #im = Image.fromarray(self._image)
                    #im.save(self._image_path)
                    if self.format != 'TIFF':
                        bgr = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(str(self._image_path), bgr)
                    else:
                        im = Image.fromarray(self._image)
                        im.save(self._image_path)
            for lab_img in self._label_images.values():
                lab_img.save()
        self._dirty_flag = False

    def unload(self):
        self.save()
        self._image = None

        for lab_img in self._label_images.values():
            lab_img.unload()

    def has_segmentation_for(self, label_name: str) -> bool:
        return self._label_images[label_name].is_segmented

    @property
    def has_unsaved_changes(self) -> bool:
        return self._dirty_flag or any([lab.has_unsaved_changes for lab in self._label_images.values()])

    @property
    def _subscriber(self) -> Subscriber:
        return self.__subscriber

    @property
    def tags(self) -> typing.Set[str]:
        return self._tags

    @tags.setter
    def tags(self, _tags: typing.Set[str]):
        self._tags = {tag for tag in _tags if not tag.isspace() and len(tag) > 0}
        # self._subscriber.notify(self.image_name, UpdateContext.Photo,
        #                         {'tags': {
        #                             'added': list(self._tags),
        #                             'removed': []
        #                         }})
        event = UpdateEvent(self, UpdateContext.Photo,
                            PhotoUpdate(self, PhotoUpdateType.TagsUpdated,
                                        # data={
                                        #     'added': list(self._tags),
                                        #     'removed': []
                                        # },
                                        tags_added=list(self._tags)))
        self.__subscriber.notify(event)

    def add_tag(self, tag: str):
        if tag in self._tags or len(tag) == 0 or tag.isspace():
            return
        self._tags.add(tag)
        # self._subscriber.notify(self.image_name, UpdateContext.Photo,
        #                         {'tags': {
        #                             'added': [tag],
        #                             'removed': []
        #                         }})
        event = UpdateEvent(self, UpdateContext.Photo,
                            PhotoUpdate(self, PhotoUpdateType.TagsUpdated,
                                        # data={
                                        #     'added': [tag],
                                        #     'removed': []
                                        # },
                                        tags_added=[tag]))
        self.__subscriber.notify(event)

    def remove_tag(self, tag: str):
        if tag not in self._tags:
            return

        self._tags.remove(tag)
        # self._subscriber.notify(self.image_name, UpdateContext.Photo,
        #                         {'tags': {
        #                             'added': [],
        #                             'removed': [tag]
        #                         }})
        event = UpdateEvent(self, UpdateContext.Photo,
                            PhotoUpdate(self, PhotoUpdateType.TagsUpdated,
                                        # data={
                                        #     'added': [],
                                        #     'removed': [tag]
                                        # },
                                        tags_removed=[tag]))
        self.__subscriber.notify(event)

    def toggle_tag(self, tag: str, enabled: bool):
        if enabled:
            self.add_tag(tag)
        else:
            self.remove_tag(tag)

    @property
    def thumbnail(self) -> typing.Optional[QImage]:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail: typing.Optional[QImage]):
        self._thumbnail = thumbnail
        # TODO fire signal to notify of thumbnail change

    def _handle_label_image_property_removed(self, label_image: LabelImg, reg_prop: RegionProperty):
        update_obj: LabelImageUpdate = LabelImageUpdate(label_image, LabelImageUpdateType.PropertyRemoved)
        update_obj.properties_removed.append(reg_prop)
        update_event = UpdateEvent(self, UpdateContext.LabelImg, update_obj)

        print(f'removing {reg_prop.info.name} from {label_image.label_info.name}`s {reg_prop.label}')
        self.__subscriber.notify(update_event)

    def _handle_label_image_property_added(self, label_image: LabelImg, reg_prop: RegionProperty):
        update_obj: LabelImageUpdate = LabelImageUpdate(label_image, LabelImageUpdateType.PropertyAdded)
        update_obj.properties_removed.append(reg_prop)
        update_event = UpdateEvent(self, UpdateContext.LabelImg, update_obj)

        print(f'adding {reg_prop.info.name} to {label_image.label_info.name}`s {reg_prop.label}')
        self.__subscriber.notify(update_event)

    def _handle_properties_need_recomputation(self, label_image: LabelImg):
        update_obj: LabelImageUpdate = LabelImageUpdate(label_image, LabelImageUpdateType.PropertiesInvalid)
        update_event = UpdateEvent(self, UpdateContext.LabelImg, update_obj)

        self.__subscriber.notify(update_event)

    def _handle_all_properties_valid(self, label_image: LabelImg):
        update_obj: LabelImageUpdate = LabelImageUpdate(label_image, LabelImageUpdateType.PropertiesValid)
        update_event = UpdateEvent(self, UpdateContext.LabelImg, update_obj)

        self.__subscriber.notify(update_event)

    @property
    def import_time(self) -> QDateTime:
        return self._import_time

    @import_time.setter
    def import_time(self, import_time: QDateTime):
        self._import_time = import_time

    @property
    def annotations(self) -> typing.Dict[AnnotationType, typing.List[Annotation]]:
        return self._annotations

    def get_annotations(self, ann_type: AnnotationType) -> typing.List[Annotation]:
        return self._annotations.get(ann_type, [])

    def insert_new_annotation(self, ann_type: AnnotationType, annotation: Annotation):
        annotations: typing.List[Annotation] = self._annotations.setdefault(ann_type, list())
        class_annotations = list(filter(lambda ann: ann.ann_class == annotation.ann_class, annotations))
        new_instance_id = max([ann.ann_instance_id for ann in class_annotations], default=-1) + 1
        annotation.ann_instance_id = new_instance_id
        annotation.instance_name = annotation.ann_instance_id
        self._annotations[ann_type].append(annotation)
        self.new_annotation_added.emit(-1, annotation)
