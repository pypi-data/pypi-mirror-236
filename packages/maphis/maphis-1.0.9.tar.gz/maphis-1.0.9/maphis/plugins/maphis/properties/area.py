import copy
import typing
from typing import List, Optional

import numpy as np

from maphis.common.action import action_info
from maphis.common.user_param import Param
from maphis.common.common import Info
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache, Region
from maphis.measurement.values import ScalarValue, ureg
from maphis.measurement.region_property import RegionProperty


@action_info(name='Area', description='Area of the region (px or mm\u00b2)', group='Length & area measurements')
class Area(PropertyComputation):
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
    typing.List[RegionProperty]:

        props: typing.List[RegionProperty] = []

        for region_label in region_labels:
            if region_label not in regions_cache.regions:
                continue
            region: Region = regions_cache.regions[region_label]

            prop = self.example('area')
            prop.label = region.label
            prop.info = copy.deepcopy(self.info)
            value = ScalarValue(int(np.count_nonzero(region.mask)) * (ureg['pixel'] * ureg['pixel']))
            if photo.image_scale is not None and photo.image_scale.magnitude > 0:
                prop.value = ScalarValue(value.value / (photo.image_scale * photo.image_scale))
                # prop.unit = 'mm\u00b2'  # TODO sync unit with the units in Photo
            else:
                prop.value = value
            prop.val_names = ['Area']
            prop.num_vals = 1
            props.append(prop)
        return props

    @property
    def user_params(self) -> List[Param]:
        return super().user_params

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted

    @property
    def computes(self) -> typing.Dict[str, Info]:
        return {'area': self.info}

    def example(self, prop_name: str) -> RegionProperty:
        prop = RegionProperty()
        prop.label = 0
        prop.info = copy.deepcopy(self.info)
        prop.value = ScalarValue(0 * ureg['pixel'] * ureg['pixel'])
        # prop.val_names = ['Area']
        prop.num_vals = 1
        prop.prop_comp_key = prop.info.key
        prop.local_key = prop_name
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return super().target_worksheet('area')

    @property
    def group(self) -> str:
        return super().group
