import copy
import typing
from typing import Optional

import numpy as np
import skimage

from maphis.common.action import action_info
from maphis.common.common import Info
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache
from maphis.common.user_param import Param
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import ScalarValue, ureg


@action_info(name='Max feret diameter', description='Maximum Feret diameter (px or real units)', group='Length & area measurements')
class MaxFeret(PropertyComputation):
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:
        props: typing.List[RegionProperty] = []

        for label in region_labels:
            if label not in regions_cache.regions:
                continue
            region_obj = regions_cache.regions[label]
            reg_props = skimage.measure.regionprops_table(region_obj.mask.astype(np.uint8), region_obj.image,
                                                          properties=['label', 'feret_diameter_max'])

            prop = self.example('max_feret')
            prop.label = int(label)
            prop.info = copy.deepcopy(self.info)
            prop.value = ScalarValue(float(reg_props['feret_diameter_max'][0]) * ureg['pixel'])
            if photo.image_scale is not None and photo.image_scale.magnitude > 0:
                prop.value = ScalarValue(prop.value.value / photo.image_scale)
            prop.val_names = ['Max Feret']
            prop.num_vals = 1
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
        prop.num_vals = 1
        prop.val_names = []
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return super().target_worksheet(self.info.key)

    @property
    def group(self) -> str:
        return super().group
