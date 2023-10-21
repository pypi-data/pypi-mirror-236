import copy
import typing
from typing import Optional

import numpy as np
from skimage.morphology import medial_axis

from maphis.common.action import action_info
from maphis.common.common import Info
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache
from maphis.common.user_param import Param
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import ScalarValue, ureg


@action_info(name='Mean width', description='Mean width of a region (px or real units)', group='Length & area measurements')
class MeanWidth(PropertyComputation):
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:
        props: typing.List[RegionProperty] = []

        for label in region_labels:
            if label not in regions_cache.regions:
                continue
            reg_obj = regions_cache.regions[label]
            m_axis, dst_T = medial_axis(reg_obj.mask, return_distance=True)
            rr, cc = np.nonzero(m_axis)
            mean_width = np.mean(2.0 * dst_T[rr, cc])
            if np.isnan(mean_width):
                # TODO inspect `get_longest_geodesic2` function
                mean_width = -42.0

            prop = self.example('mean_width')
            prop.info = copy.deepcopy(self.info)
            prop.label = label
            if photo.image_scale is not None:
                prop.value = ScalarValue((float(mean_width) * ureg['pixel']) / photo.image_scale)
                # prop.unit = 'mm'
            else:
                prop.value = ScalarValue(float(mean_width) * ureg['pixel'])
                # prop.unit = 'px'
            prop.num_vals = 1
            prop.val_names = ['Mean width']
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
