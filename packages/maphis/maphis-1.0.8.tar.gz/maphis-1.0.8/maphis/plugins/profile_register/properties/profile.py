import copy
import typing
from typing import Optional

import cv2
import numpy as np
import skimage
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from maphis import qimage2ndarray
from maphis.common.action import action_info
from maphis.common.common import Info
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache
from maphis.common.user_params import UserParam
from maphis.common.utils import vector_to_img
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import VectorValue, ureg


@action_info(name='Profile', description='Compute a profile feature vector', group='Shape measurements')
class Contour(PropertyComputation):
    sample_count = 40

    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:
        # lab_img = photo['Labels'].label_image
        # lab_hier = photo['Labels'].label_hierarchy
        props: typing.List[RegionProperty] = []
        # path = Path(f'C:/Users/radoslav/Desktop/contour_debug/{photo.image_name}/')
        # if not path.exists():
        #     path.mkdir()
        for label in region_labels:
            # lab_path = path / lab_hier.nodes[label].name
            # if not lab_path.exists():
            #    lab_path.mkdir()

            # region = lab_img == label

            if label not in regions_cache.regions:
                continue

            region_obj = regions_cache.regions[label]
            region = region_obj.mask

            # roi_rgb = cv2.cvtColor(255 * region.astype(np.uint8), cv2.COLOR_GRAY2BGR)

            # cv2.imwrite(str(lab_path / 'region.png'), roi_rgb)

            yy, xx = np.nonzero(region)

            x_c, y_c = round(np.mean(xx)), round(np.mean(yy))  # centroid for nonzero pixels in `roi`

            # roi_cent = cv2.circle(roi_rgb, (x_c, y_c), 3, [0, 255, 0])

            # cv2.imwrite(str(lab_path / 'roi_centroid.png'), roi_cent)

            reg_orient = skimage.measure.regionprops_table(1 * region, properties=('orientation',))

            # get the angle between y-axis and the major axis of the region in `roi`
            angle = np.rad2deg(reg_orient['orientation'][0])

            # rotate `roi` so that the major axis coincides with y-axis
            rotated = skimage.transform.rotate(region, angle=-angle, center=(x_c, y_c), resize=True)

            # io.imsave(str(lab_path / 'roi_rotated.png'), rotated)

            outline = np.logical_xor(rotated, cv2.erode(255 * rotated.astype(np.uint8), np.ones((3, 3)),
                                                        borderValue=0, borderType=cv2.BORDER_CONSTANT) > 0)

            # io.imsave(str(lab_path / 'outline.png'), outline)

            outline_yy, outline_xx = np.nonzero(outline)

            xs_by_y: typing.Dict[int, typing.List[int]] = {}

            for y, x in zip(outline_yy, outline_xx):
                xs_by_y.setdefault(y, []).append(x)

            outline_yy = np.unique(outline_yy)

            # step = outline_yy.shape[0] / float(self.sample_count)

            step = (np.max(outline_yy) - np.min(outline_yy)) / float(self.sample_count - 1)

            feat_vector: typing.List[float] = []

            y_start = outline_yy[0]
            y_curr = y_start
            offset = 0

            # viz = cv2.cvtColor(255 * outline.copy().astype(np.uint8), cv2.COLOR_GRAY2BGR)

            for i in range(self.sample_count):
                y_curr = min(int(round(y_start + offset)), max(outline_yy))
                offset += step
                if y_curr not in xs_by_y:
                    left = 0
                    right = -1
                else:
                    left = min(xs_by_y[y_curr])
                    right = max(xs_by_y[y_curr])

                # viz[y_curr, left] = [255, 0, 0]
                # viz[y_curr, right] = [0, 255, 0]

                width = 0.5 * (right - left + 1)
                if photo.image_scale is not None:
                    width /= photo.image_scale.magnitude
                feat_vector.append(width)

            # cv2.imwrite(str(lab_path / 'viz.png'), viz)

            prop = self.example('profile')
            if photo.image_scale is not None:
                prop.value = VectorValue((feat_vector * ureg['pixel']) / photo.image_scale)
            else:
                prop.value = VectorValue(feat_vector * ureg['pixel'])
            prop.label = label
            props.append(prop)
        return props

    @property
    def user_params(self) -> typing.List[UserParam]:
        return super().user_params

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted

    @property
    def computes(self) -> typing.Dict[str, Info]:
        return {self.info.key: self.info}

    def example(self, prop_name: str) -> RegionProperty:
        prop = super().example(prop_name)
        prop.label = 0
        prop.info = copy.deepcopy(self.info)
        prop.num_vals = self.sample_count
        prop.val_names = []
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return "Profiles"

    @property
    def group(self) -> str:
        return super().group

    @classmethod
    def get_representation(cls, reg_prop: RegionProperty, role: Qt.ItemDataRole, alternative_rep: bool=False) -> typing.Any:
       if role == Qt.ItemDataRole.DecorationRole and alternative_rep:
           viz = vector_to_img(reg_prop.value.raw_value, (128, 24))
           viz = np.dstack((viz,) * 3)
           # mask = np.array(viz[:, :, 0] > 200)[:, :, np.newaxis]
           # viz = np.where(mask, [[*self._invalid_property_bg_color.toTuple()[:3]]], [[0, 0, 0]])
           return QPixmap(qimage2ndarray.array2qimage(viz))
       elif role == Qt.ItemDataRole.DisplayRole:
           return str(reg_prop.value.value) if not alternative_rep else None
       return PropertyComputation.get_representation(reg_prop, role, alternative_rep)
