import dataclasses
import typing

import numpy as np

from maphis.common.photo import Photo


@dataclasses.dataclass
class Region:
    """Object representing a region. `mask` and `image` attributes are subimages of the original label image and photo that
    the region represented by this object originates from.

    Attributes:
        label (int): the integer label of the region
        mask (np.ndarray): binary mask of the region
        image (np.ndarray): subimage of the photo this region covers
        bbox (Tuple[int, int, int, int]): corners of the bounding box of this region - (top, left, bottom, right)
    """

    label: int
    mask: np.ndarray
    image: np.ndarray
    bbox: typing.Tuple[int, int, int, int]  # top, left, bottom, right


class RegionsCache:
    """Stores [`Region`][maphis.common.regions_cache.Region] objects, one for each integer label present in `region_labels`.
    Intended for efficient access to regions so you don't have to repeatedly search for them.

    Attributes:
        regions (typing.Dict[int, [`Region`][maphis.common.regions_cache.Region]]): dictionary of [`Region`][maphis.common.regions_cache.Region] objects, keyed by corresponding region labels
        data_storage (typing.Dict[str, typing.Any]): this is for you to cache arbitrary data pertaining to the specific photo, that you expect you will need
            at some later point.

    """
    def __init__(self, region_labels: typing.Set[int], photo: Photo, label_name: str):
        self.regions: typing.Dict[int, Region] = {}
        label_img = photo[label_name]
        regions_by_level = label_img.label_hierarchy.group_by_level(region_labels)

        for level, labels in regions_by_level.items():
            label_img_on_level = label_img[level]
            for label in labels:
                region_mask = label_img_on_level == label
                yy, xx = np.nonzero(region_mask)
                if len(yy) == 0:
                    continue
                top, left, bottom, right = np.min(yy), np.min(xx), np.max(yy), np.max(xx)

                mask_roi = region_mask[top:bottom+1, left:right+1]
                image_roi = photo.image[top:bottom+1, left:right+1]

                region = Region(label, mask_roi, image_roi, (top, left, bottom-top+1, right-left+1))
                self.regions[label] = region
        self.data_storage: typing.Dict[str, typing.Any] = {}
