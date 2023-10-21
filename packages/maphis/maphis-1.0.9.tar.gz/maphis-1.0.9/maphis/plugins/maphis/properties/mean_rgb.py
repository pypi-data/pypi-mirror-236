import copy
import typing
from typing import Optional

import numpy as np
import pint
from PySide6.QtGui import Qt, QColor

from maphis.common.action import action_info
from maphis.common.common import Info
from maphis.common.label_image import RegionProperty, PropertyType
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache, Region
from maphis.common.units import Unit, BaseUnit, SIPrefix
from maphis.common.user_param import Param
from maphis.measurement.values import VectorValue


@action_info(name='Mean RGB', description='Mean RGB', group='Color')
class MeanRGB(PropertyComputation):
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:

        props: typing.List[RegionProperty] = []
        refl = photo['Reflections'].label_image

        for region_label in region_labels:
            if region_label not in regions_cache.regions:
                continue
            region: Region = regions_cache.regions[region_label]

            top, left, height, width = region.bbox
            refl_roi = refl[top:top + height, left:left + width]

            mask = np.logical_xor(region.mask, refl_roi > 0)

            yy, xx = np.nonzero(mask)

            pixels = region.image[yy, xx]

            mean_intensity = np.mean(pixels, axis=0)

            prop = self.example('mean_rgb')
            prop.label = int(region.label)
            prop.value = VectorValue(pint.Quantity(mean_intensity.tolist()))
            prop.value.column_names = ['R', 'G', 'B']

            props.append(prop)
        return props

    @property
    def user_params(self) -> typing.List[Param]:
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
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return super().target_worksheet(self.info.key)

    @property
    def group(self) -> str:
        return super().group

    @classmethod
    def get_representation(cls, reg_prop: RegionProperty, role: Qt.ItemDataRole, alternative_rep: bool=False) -> typing.Any:
        rgb_value: typing.List[float] = reg_prop.value.raw_value
        if role == Qt.ItemDataRole.DisplayRole:
            return f'{rgb_value[0]:.2f}R, {rgb_value[1]:.2f}G, {rgb_value[2]:.2f}B' if not alternative_rep else None
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor.fromRgbF(*(val / 255.0 for val in rgb_value)) if alternative_rep else None
        return PropertyComputation.get_representation(reg_prop, role)
