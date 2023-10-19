import dataclasses
import json
import logging
from enum import IntEnum
from pathlib import Path
from typing import Optional, Any, List, Dict, Tuple, Union
import time

import numpy as np
import typing
from PIL import Image
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from maphis.measurement.region_property import RegionProperty, PropertyType
from scipy import ndimage
from skimage import io
import pint

from maphis.common.label_hierarchy import LabelHierarchy


class LabelImgType(IntEnum):
    Mask = 0,
    Regions = 1,


class LabelImgInfo:
    """
    Info about a particular `LabelImg` object.
    """

    def __init__(self, label_name: str, is_default: bool, constrain_to: typing.Dict[str, typing.List[str]], label_hierarchy: Optional[LabelHierarchy]=None):
        self.name: str = label_name
        self.is_default = is_default  # if this is the default label image to show at startup
        # self.constrain_to: Optional[str] = always_constrain_to  # whether the editing should be always constrained to some other label image
        # self.can_constrain_to: Optional[List[str]] = allow_constrain_to  # what other label images can serve as constraints
        #
        # if self.constrain_to is not None:
        #     self.can_constrain_to = None
        self.constrain_to: typing.Dict[str, typing.List[str]] = constrain_to
        self.label_hierarchy: LabelHierarchy = label_hierarchy

    @property
    def can_be_constrained(self) -> bool:
        # return self.constrain_to is not None or self.can_constrain_to is not None
        return len(self.constrain_to) > 0

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'name': self.name,
            'label_hierarchy_file': self.label_hierarchy._fname,
            'constrain_to': [
                {
                    'label_image_name': label_img_name,
                    'regions': region_codes
                }
            for label_img_name, region_codes in self.constrain_to.items()],
            'is_default': self.is_default
        }

    @staticmethod
    def from_dict(_info_dict: typing.Dict[str, typing.Any]) -> 'LabelImgInfo':
        return LabelImgInfo(label_name=_info_dict['name'],
                            is_default=_info_dict['is_default'],
                            constrain_to={constraint_entry['label_image_name']: constraint_entry['regions'] for constraint_entry in _info_dict['constrain_to']})


class LabelImg(QObject):
    """
    A class representing a label image.
    """

    property_added = Signal(object, RegionProperty)
    property_removed = Signal(object, RegionProperty)
    property_updated = Signal(object, RegionProperty)
    properties_need_recomputation = Signal(object)
    all_properties_valid = Signal(object)

    def __init__(self, image_size: Tuple[int, int]):
        super(LabelImg, self).__init__(None)
        self._label_img: Optional[np.ndarray] = None
        self.size = image_size
        self._path: typing.Optional[Path] = None
        self._bbox: typing.Optional[typing.Tuple[int, int, int, int]]
        self._region_props: Dict[int, Dict[str, RegionProperty]] = {}
        self.label_img_type: LabelImgType = LabelImgType.Regions
        self.label_info: typing.Optional[LabelImgInfo] = None
        self.label_semantic: str = ''
        self._used_labels: Optional[typing.Set[int]] = None
        self._dirty_flag: bool = False
        self.prop_list: typing.Set[RegionProperty] = set()
        self.timestamp: int = -1
        self.is_segmented: bool = False

    @property
    def path(self) -> typing.Optional[Path]:
        if self._path is not None:
            return self._path
        return None

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def label_image(self) -> np.ndarray:
        if self._label_img is None:
            if self._path.exists():
                self._label_img = io.imread(str(self._path))
                self.is_segmented = bool(np.any(self._label_img > 0))
            else:
                self._label_img = np.zeros(self.size[::-1], np.uint32)
        return self._label_img

    @label_image.setter
    def label_image(self, lbl_nd: np.ndarray):
        if self._label_img is None:
            self._label_img = lbl_nd
        else:
            self.set_image(lbl_nd)
        self.is_segmented = bool(np.any(self._label_img > 0))
        self._dirty_flag = True
        self._invalidate_measurements()

    @property
    def is_set(self) -> bool:
        return self._label_img is not None

    def reload(self):
        if self._path.exists():
            loaded_img = io.imread(str(self._path))
            self._label_img = loaded_img.astype(np.uint32)
            self._used_labels = set(np.unique(self._label_img))
        else:
            self._label_img = np.zeros(self.size[::-1], dtype=np.uint32)
            self._used_labels = {0}

    def unload(self):
        self.save()
        self._label_img = None

    def _serialize_prop_value(self, reg_prop: RegionProperty) -> Union[typing.Any, str]:
        """Returns a representation of `RegionProperty.value` in a form suitable for serialization in .json."""
        if reg_prop.prop_type == PropertyType.NDArray:
            path = f'{self._path}_{reg_prop.info.name}_{reg_prop.label}.npy'
            fname = Path(path).name
            np.save(path, reg_prop.value[0])
            return repr((fname, reg_prop.value[1]))  # return path to the serialized ndarray and the unit that the array is in
        return repr(reg_prop.value)

    def save(self):
        if self._dirty_flag:
            if self._label_img is not None:
                self._used_labels = set(np.unique(self._label_img))
                io.imsave(str(self._path), self._label_img, check_contrast=False)
                #im = Image.fromarray(self._label_img)
                #im.save(self._path)
            prop_dict = {
                self.label_hierarchy.code(label): {
                    'measurements': [
                        prop.to_dict(label_folder=self._path.parent, npy_fname=f'{self._path.name}_{prop.info.name}_{prop.label}.npy')
                            # 'name': prop.info.name,
                            # 'label': prop.label,
                            # 'value': self._serialize_prop_value(prop),
                            # # 'unit': prop.unit,
                            # 'prop_type': prop.prop_type,
                            # 'num_vals': prop.num_vals,
                            # 'val_names': prop.val_names,
                            # 'col_names': prop.col_names,
                            # 'row_names': prop.row_names,
                            # 'key': prop.info.key,
                            # 'description': prop.info.description,
                            # 'prop_comp_key': prop.prop_comp_key,
                            # 'local_key': prop.local_key,
                            # 'settings': prop.settings,
                            # 'up_to_date': prop.up_to_date
                        for prop in prop_dict.values()
                    ]
                } for label, prop_dict in self._region_props.items()
            }
            with open(f'{self._path}_measurements.json', 'w') as f:
                json.dump(prop_dict, f, indent=2)
            self._dirty_flag = False

    @classmethod
    def create2(cls, path: Path, image_size: typing.Tuple[int, int], label_info: LabelImgInfo, label_name: str) -> 'LabelImg':
        """Creates new `LabelImg` object.

        path: Path - where this label image should be stored
        image_size: (height, width)
        label_info: LabelImgInfo
        label_name: str - not used, stored in `label_info`
        """
        lbl = LabelImg(image_size)
        #lbl._type = label_type
        lbl._path = path
        #lbl.label_img_type = label_type
        lbl.label_info = label_info
        lbl.label_semantic = label_info.name
        lbl._load_measurements()
        return lbl

    def make_empty(self, size: typing.Tuple[int, int]):
        self._label_img = np.zeros(size, np.uint32)
        self._used_labels = {0}

    def set_image(self, img: np.ndarray):
        if self._label_img is not None and img is not None:
            if self._label_img.shape != img.shape:
                raise ValueError(f'The shape must be {self._label_img.shape}, got {img.shape}.')
            elif self._label_img.dtype != img.dtype:
                raise ValueError(f'The dtype must be {self._label_img.dtype}, got {img.dtype}.')
        self._label_img = img
        self._dirty_flag = True
        self._invalidate_measurements()

    def clone(self) -> 'LabelImg':
        lbl = LabelImg(self.size)
        lbl._path = self._path
        lbl._label_img = self._label_img.copy() if self._label_img is not None else None
        # lbl.label_img_type = self.label_img_type
        lbl.label_info = self.label_info
        lbl.label_semantic = self.label_semantic
        lbl._label_hierarchy = self.label_hierarchy
        lbl._used_labels = self._used_labels
        lbl._dirty_flag = self._dirty_flag
        return lbl

    def _compute_bbox(self):
        coords = np.nonzero(self._label_img)
        top, left = np.min(coords[0]), np.min(coords[1])
        bottom, right = np.max(coords[0]), np.max(coords[1])
        self._bug_bbox = [left, top, right, bottom]

    @property
    def region_props(self) -> Dict[int, Dict[str, RegionProperty]]:
        """Returns a dictionary of (label -> (property_key -> `RegionProperty`) pairs."""
        return self._region_props

    @region_props.setter
    def region_props(self, props: Dict[int, Dict[str, RegionProperty]]):
        for label, props in props.items():
            label_props = self._region_props.setdefault(label, dict())
            for prop_key, prop in props.items():
                label_props[prop_key] = prop
                self.property_added.emit(self, prop)
                #label_prop = label_props.setdefault(prop_key, RegionProperty())
                #label_prop.label = prop.label
                #label_prop.info = prop.info
                #label_prop.value = prop.value
                #label_prop.unit = prop.unit
                #label_prop.prop_type = prop.prop_type
                #label_prop.num_vals = prop.num_vals
        if self.has_valid_measurements():
            self.all_properties_valid.emit(self)
        self._dirty_flag = True

    def clear_region_props(self):
        self._region_props.clear()

    def set_region_prop(self, region_label: int, prop: RegionProperty):
        # self.region_props = {region_label: {prop.info.key: prop}}
        self.region_props = {region_label: {prop.prop_key: prop}}
        if prop in self.prop_list:  # meaning the combination of (property_key, region_label) is in self.prop_list (it does not take into account the actual value of the property)
            self.prop_list.remove(prop)
        self.prop_list.add(prop)

    def get_region_props(self, region_label: int) -> Optional[Dict[str, RegionProperty]]:
        """Returns (property_key -> `RegionProperty) for `region_label`."""
        if region_label in self._region_props:
            return self._region_props[region_label]
        return None

    def remove_property(self, label: int, property_key: str):
        if label not in self._region_props:
            return
        if property_key not in self._region_props[label]:
            return
        reg_prop: RegionProperty = self._region_props[label][property_key]
        del self._region_props[label][property_key]
        self.prop_list.remove(reg_prop)
        self.set_dirty()
        self.property_removed.emit(self, reg_prop)
        if self.has_valid_measurements():
            self.all_properties_valid.emit(self)

    @property
    def label_hierarchy(self) -> LabelHierarchy:
        return self.label_info.label_hierarchy

    @label_hierarchy.setter
    def label_hierarchy(self, lab_hier: LabelHierarchy):
        pass
        # TODO handle possible changes to the label image

    def __getitem__(self, level: int) -> Optional[np.ndarray]:
        """Returns a label image generated from this one, where all the labels are from the level `level` of `label_hierarchy`."""
        if self.label_hierarchy is None:
            return self.label_image
        if level >= len(self.label_info.label_hierarchy.hierarchy_levels):
            return None
        level_mask = self.label_info.label_hierarchy.hierarchy_levels[level].accumulated_bit_mask
        return np.bitwise_and(self.label_image, level_mask)

    @property
    def used_labels(self) -> Optional[typing.Set[int]]:
        """Returns the set of labels that are present in this label image."""
        if self._dirty_flag or self._used_labels is None:
            self._used_labels = set(np.unique(self.label_image))
            self._dirty_flag = False
        return self._used_labels

    def set_dirty(self):
        self._dirty_flag = True
        self._invalidate_measurements()
        self.timestamp = time.time()

    def _load_measurements(self):
        self._dirty_flag = False
        if (path := Path(f'{str(self._path)}_measurements.json')).exists():
            with open(path) as f:
                props = json.load(f)
            for code in props.keys():
                for prop_dict in props[code]['measurements']:
                    prop_dict['label_image_folder'] = str(self.path.parent)
                    prop_dict['image_path'] = self._path
                    reg_prop = RegionProperty.from_dict(prop_dict)
                    if reg_prop is None:
                        continue
                    # TODO remove these two if's eventually
                    if (prop_key := reg_prop.prop_comp_key).startswith('arthropod_describer.'):
                        _, suffix = prop_key.split('arthropod_describer.')
                        reg_prop.prop_comp_key = f'maphis.{suffix}'
                        self._dirty_flag = True
                    if (prop_key := reg_prop.info.key).startswith('arthropod_describer.'):
                        _, suffix = prop_key.split('arthropod_describer.')
                        reg_prop.info.key = f'maphis.{suffix}'
                        self._dirty_flag = True
                    self.set_region_prop(reg_prop.label, reg_prop)

    def rotate(self, ccw: bool):
        unload = self._label_img is not None
        if self._label_img is None:
            self.reload()
        self._label_img = ndimage.rotate(self._label_img, 90 if ccw else -90, order=0, prefilter=False)
        self.size = self._label_img.shape[::-1]
        self._dirty_flag = True
        if unload:
            self.unload()

    #def save(self):
    #    if self._dirty_flag:
    #        self.unload()
    #        self._dirty_flag = False

    def resize(self, factor: float):
        unload = self._label_img is not None
        if self._label_img is None:
            self.reload()
        im = Image.fromarray(self._label_img)
        sz = (int(round(factor * self.size[0])),
              int(round(factor * self.size[1])))
        self.size = sz
        im = im.resize(sz, resample=Image.NEAREST)
        self._label_img = np.asarray(im, dtype=np.uint32)
        self._dirty_flag = True
        if unload:
            self.unload()

    def mask_for(self, label: int) -> np.ndarray:
        """Returns a binary (np.bool) image where `True` values mark pixels whose value is `label` or are descendants of `label`."""
        level = self.label_hierarchy.get_level(label)
        level_img = self[level]
        return level_img == label

    @property
    def has_unsaved_changes(self) -> bool:
        return self._dirty_flag

    @property
    def bbox(self) -> typing.Optional[typing.Tuple[int, int, int, int]]:
        mask = self._label_img > 0
        rr, cc = np.nonzero(mask)
        if len(rr) == 0:
            return None
        top, left, bottom, right = np.min(rr), np.min(cc), np.max(rr), np.max(cc)

        return left, top, right - left + 1, bottom - top + 1

    def _invalidate_measurements(self):
        need_to_recompute = False
        for region_label, region_props in self._region_props.items():
            for region_prop, region_prop in region_props.items():
                region_prop.up_to_date = False
                need_to_recompute = True
        # TODO fire a signal
        if need_to_recompute:
            self.properties_need_recomputation.emit(self)

    def has_valid_measurements(self) -> bool:
        for region_label, region_props in self._region_props.items():
            for prop_key, region_prop in region_props.items():
                if not region_prop.up_to_date:
                    return False
        return True
