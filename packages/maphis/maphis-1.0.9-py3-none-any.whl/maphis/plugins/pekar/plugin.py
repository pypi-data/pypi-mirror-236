import typing
from typing import Optional

import arthseg
import cv2
import numpy as np

from maphis.common.action import region_computation, RegionComputation, action_info
from maphis.common.common import Info
from maphis.common.label_image import LabelImg
from maphis.common.photo import Photo
from maphis.common.plugin import Plugin
from maphis.common.state import State
from maphis.common.storage import Storage


@action_info(name='Pekar', description='Functions for semantic segmentation of arthropods.',
             group='Segmentation')
class Pekar(Plugin):
    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)

    @staticmethod
    @region_computation(name='Reflections', description="Generates 'reflections' mask based on lightness.",
                        group='Segmentation')
    def reflections(comp: RegionComputation, photo: Photo, label: typing.Optional[typing.Set[int]], storage: Storage) \
        -> typing.List[LabelImg]:
        k = 2.0

        copy = photo['Reflections'].clone()

        mask = photo['Labels'].label_image
        light = cv2.cvtColor(photo.image, cv2.COLOR_RGB2HLS)[:, :, 1]
        reflections_mask = np.zeros_like(mask, dtype=bool)
        background_label = photo['Labels'].label_hierarchy.label('0:0:0:0')

        for label in np.unique(mask):
            if label != background_label:
                average = np.mean(light[mask == label])
                deviation = np.std(light[mask == label])
                reflections_mask[mask == label] = (
                        light[mask == label] > k * deviation + average
                )

        reflection_label = copy.label_hierarchy.nodes_flat[-1].label
        copy.label_image = np.where(
            reflections_mask, reflection_label, 0
        ).astype(np.uint32)

        return [copy]

    @staticmethod
    @region_computation(name='Segment appendages', description='Labels appendages into smaller parts based on '
                                                               "geodetic distance from the specimen's body.",
                        group='Segmentation')
    def segment_appendages(comp: RegionComputation, photo: Photo, labels: typing.Optional[typing.Set[int]],
                           storage: Storage) -> typing.List[LabelImg]:
        copy = photo['Labels'].clone()
        label_hierarchy = copy.label_hierarchy

        leg_labels = {
            label_hierarchy.label('1:2:1:0'): [
                label_hierarchy.label('1:2:1:1'),
                label_hierarchy.label('1:2:1:2'),
                label_hierarchy.label('1:2:1:3'),
            ],
            label_hierarchy.label('1:2:2:0'): [
                label_hierarchy.label('1:2:2:1'),
                label_hierarchy.label('1:2:2:2'),
                label_hierarchy.label('1:2:2:3'),
            ],
            label_hierarchy.label('1:2:3:0'): [
                label_hierarchy.label('1:2:3:1'),
                label_hierarchy.label('1:2:3:2'),
                label_hierarchy.label('1:2:3:3'),
            ],
            label_hierarchy.label('1:2:4:0'): [
                label_hierarchy.label('1:2:4:1'),
                label_hierarchy.label('1:2:4:2'),
                label_hierarchy.label('1:2:4:3'),
            ],
            label_hierarchy.label('1:2:5:0'): [
                label_hierarchy.label('1:2:5:1'),
                label_hierarchy.label('1:2:5:2'),
                label_hierarchy.label('1:2:5:3'),
            ],
            label_hierarchy.label('1:2:6:0'): [
                label_hierarchy.label('1:2:6:1'),
                label_hierarchy.label('1:2:6:2'),
                label_hierarchy.label('1:2:6:3'),
            ],
            label_hierarchy.label('1:2:7:0'): [
                label_hierarchy.label('1:2:7:1'),
                label_hierarchy.label('1:2:7:2'),
                label_hierarchy.label('1:2:7:3'),
            ],
            label_hierarchy.label('1:2:8:0'): [
                label_hierarchy.label('1:2:8:1'),
                label_hierarchy.label('1:2:8:2'),
                label_hierarchy.label('1:2:8:3'),
            ],
        }

        body_labels = {
            label_hierarchy.label('1:1:1:0'),
            label_hierarchy.label('1:1:2:0'),
        }
        back_label = label_hierarchy.label('1:1:3:0')

        copy.label_image = arthseg.leg_segments(
            copy.label_image,
            labels=leg_labels,
            body_labels=body_labels,
            alternative_labels={back_label},
        )

        return [copy]
