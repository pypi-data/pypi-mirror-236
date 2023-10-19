import typing

from maphis.common.label_image import RegionProperty
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache


class ComputationsScheduler:
    def __init__(self, props_by_regions: typing.Dict[int, typing.List[PropertyComputation]]):
        self.props_by_regions: typing.Dict[int, typing.List[PropertyComputation]] = props_by_regions
        self.regions_labels: typing.Set[int] = set(props_by_regions.keys())

    def run(self, photo: Photo, label_name: str) -> typing.List[RegionProperty]:
        regions_cache = RegionsCache(self.regions_labels, photo, label_name)

        props: typing.List[RegionProperty] = []

        for label, prop_comps in self.props_by_regions.items():
            for prop_comp in prop_comps:
                pass