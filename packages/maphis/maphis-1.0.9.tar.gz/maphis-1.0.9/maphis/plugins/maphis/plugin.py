import csv
import typing
from typing import Optional

import numpy as np
from PySide6.QtWidgets import QMessageBox, QApplication
from openpyxl.workbook import Workbook

from maphis.common.action import RegionComputation, GeneralAction, region_computation, general_action, param_int, \
    param_bool, param_string, scalar_property_computation, PropertyComputation, vector_property_computation, action_info
from maphis.common.common import Info
from maphis.common.label_image import LabelImg
from maphis.common.photo import Photo
from maphis.common.plugin import Plugin, ActionContext
from maphis.common.regions_cache import RegionsCache
from maphis.common.state import State
from maphis.common.storage import Storage
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import ureg, ScalarValue, VectorValue
from maphis.project.annotation import KeypointAnnotation, AnnotationType, Keypoint


@action_info(name='MAPHIS', description='Plugin containing various measurement computations.', group='General')
class MaphisPlugin(Plugin):
    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)


def get_landmark_in_real_units(kp: Keypoint, photo: Photo) -> Keypoint:
    if photo.image_scale is None:
        return Keypoint(kp.name)
    return Keypoint(kp.name,
                    x=(ureg.Quantity(kp.x, 'pixel') / photo.image_scale).to('mm').magnitude,
                    y=(ureg.Quantity(kp.y, 'pixel') / photo.image_scale).to('mm').magnitude)
