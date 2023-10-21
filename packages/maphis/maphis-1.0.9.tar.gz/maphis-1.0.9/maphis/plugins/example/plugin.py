import csv
import typing
from typing import Optional

import numpy as np
import pint
from PySide6.QtWidgets import QApplication, QMessageBox
from openpyxl.workbook import Workbook

from maphis.common.action import action_info, region_computation, param_int, param_string, param_bool, \
    scalar_property_computation, RegionComputation, PropertyComputation, vector_property_computation, general_action, \
    GeneralAction, GeneralActionContext
from maphis.common.common import Info
from maphis.common.label_image import LabelImg
from maphis.common.photo import Photo
from maphis.common.plugin import Plugin, ActionContext
from maphis.common.regions_cache import RegionsCache, Region
from maphis.common.state import State
from maphis.common.storage import Storage
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import ScalarValue, ureg, VectorValue
from maphis.project.annotation import KeypointAnnotation, AnnotationType
from maphis.tools.landmarks import get_landmark_in_real_units


@action_info(name='Example', description='A toy plugin serving as an example on how to create your own.',
             group='Segmentation')
class Example:
    """
    This is a toy plugin to serve as an example on how to create your own. To make MAPHIS load the plugin
    replace the above statement `class Example:` with `class Example(Plugin):`.
    """
    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)

    @staticmethod
    @region_computation('Simple threshold', 'A simple thresholding operation', 'Segmentation')
    @param_int('Threshold value', 'The value of the threshold', 'threshold', 120, 0, 255)
    @param_int('Channel number (RGB)', 'Which channel to threshold on: 0 = R, 1 = G, 2 = B', 'channel', 2, 0, 2)
    @param_bool('Pixels under threshold', 'Take the region under the threshold value', 'invert', False)
    @param_bool('Erase the previous labels', 'Fill with zeros before thresholding.', 'zero_out', False)
    @param_string('Region code', 'Region code to assign to the obtained regions', 'region_code', '1:0:0:0')
    def simple_threshold(reg_comp: RegionComputation, photo: Photo, labels: typing.Optional[typing.Set[int]],
                         storage: Storage) -> typing.List[LabelImg]:
        lab_img = photo['Labels']
        lab_hier = lab_img.label_hierarchy
        code = reg_comp._user_params['region_code'].value
        if code not in lab_hier.nodes_dict:
            QMessageBox.information(QApplication.activeWindow(), 'Region not found',
                                    f"There's no region with code {code} in the current label hierarchy.",
                                    QMessageBox.StandardButton.Ok)
            return []
        node = lab_hier.nodes_dict[code]
        th = reg_comp._user_params['threshold'].value
        mask = photo.image[:, :, reg_comp._user_params['channel'].value] >= th
        if reg_comp._user_params['invert'].value:
            mask = np.logical_not(mask)
        if reg_comp._user_params['zero_out'].value:
            lab_img.label_image = np.zeros_like(lab_img.label_image)
        lab_img.label_image = np.where(mask, node.label, lab_img.label_image)
        return [lab_img]

    @staticmethod
    @scalar_property_computation(name='Area_2', description='Computes the area of a region.', group='Length & area measurements',
                                 export_target='common', default_value=ScalarValue(ureg.Quantity('1 pixel^2')))
    def area2(prop_comp: PropertyComputation, photo: Photo, reg_labels: typing.List[int], regions_cache: RegionsCache,
              props: typing.List[str]) -> typing.List[RegionProperty]:

        # RegionProperty objects holding area values for individual regions
        area_props: typing.List[RegionProperty] = []

        # Check if we have a scale available for this photo
        if photo.image_scale is not None:
            scale: pint.Quantity = photo.image_scale
        else:
            scale = ureg.Quantity(1)

        # For each region with a label `reg_label`, we'll compute its area, generating one `RegionProperty`
        # object per region
        for reg_label in reg_labels:
            # Check whether `reg_label` is present in `regions_cache`: if not, it means no region with such label
            # is present in the current photo, so we skip
            if reg_label not in regions_cache.regions:
                continue
            region: Region = regions_cache.regions[reg_label]

            area_px = np.count_nonzero(region.mask) * ureg('pixel')  # Endow the area value with pixel units

            # Convert to real units by dividing by `scale` - if photo has the scale available
            # Otherwise, dividing by `scale` just divides by one, keeping the value and the units (pixels) the same
            area = area_px / scale

            # Get a new RegionProperty object that we will fill with the `region`'s area
            new_area_prop = prop_comp.example('area2')  # supply the same name as this function's name
            new_area_prop.label = reg_label
            new_area_prop.value = ScalarValue(area)

            # Insert the property into the list
            area_props.append(new_area_prop)

        return area_props

    @staticmethod
    @vector_property_computation(name='Simple vector', description='A simple vector property', group='Test',
                                 export_target='Tests', unit=ureg.Unit('pixel'), value_count=8,
                                 value_names=['a'] * 8)
    def simple_vector(comp: PropertyComputation, photo: Photo, reg_labels: typing.List[int], regions_cache: RegionsCache,
                      props: typing.List[str]) -> typing.List[RegionProperty]:
        prop = comp.example('simple_vector')
        prop.value = VectorValue([i * 3 for i in range(8)] * ureg('mm'))
        return [prop]

    @staticmethod
    @general_action('Export landmarks to XLSX', 'Exports landmarks from all photos into Excel spreadsheet', 'Export:Landmarks',
                    general_action_context=GeneralActionContext.Measurements)
    def export_landmarks_xlsx(gen_action: GeneralAction, state: State, context: ActionContext):
        fpath = state.project.folder / 'landmarks.xlsx'
        wb = Workbook()
        ws = wb.active

        ws.append(['image_name', 'landmark_name', 'x (px)', 'y (px)', 'x (mm)', 'y (mm)'])

        for photo in state.project.storage.images:
            lm_annotations: typing.List[KeypointAnnotation] = photo.get_annotations(AnnotationType.Keypoint)
            if len(lm_annotations) == 0:
                continue
            for annotation in lm_annotations:
                for kp in annotation.kps:
                    real_kp = get_landmark_in_real_units(kp, photo)
                    ws.append((photo.image_name, kp.name, kp.x, kp.y, real_kp.x, real_kp.y))
        wb.save(fpath)

    @staticmethod
    @general_action('Export to landmarks to CSV', 'Exports landmarks from all photos into a CSV file', 'Export:Landmarks',
                    general_action_context=GeneralActionContext.Measurements)
    def _export_landmarks_csv(gen_action: GeneralAction, state: State, context: ActionContext):
        fpath = state.project.folder / 'landmarks.csv'
        with open(fpath, 'w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ['image_name', 'landmark_name', 'x (px)', 'y (px)', 'x (mm)', 'y (mm)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for photo in state.project.storage.images:
                lm_annotations: typing.List[KeypointAnnotation] = photo.get_annotations(AnnotationType.Keypoint)
                if len(lm_annotations) == 0:
                    continue
                for annotation in lm_annotations:
                    for kp in annotation.kps:
                        real_kp = get_landmark_in_real_units(kp, photo)
                        writer.writerow({'image_name': photo.image_name,
                                         'landmark_name': kp.name,
                                         'x (px)': kp.x,
                                         'y (px)': kp.y,
                                         'x (mm)': real_kp.x,
                                         'y (mm)': real_kp.y})

