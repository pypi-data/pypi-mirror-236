import csv
import typing
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication

from maphis.common.action import action_info, GeneralActionContext
from maphis.common.utils import attempt_to_save_with_retries
from maphis.common.common import Info
from maphis.common.plugin import GeneralAction, ActionContext
from maphis.common.state import State
from maphis.plugins.maphis.general.common import _filter_by_NDArray, get_prop_tuple_list, \
    _group_measurements_by_sheet, _tabular_export_routine, _ndarray_export_routine, show_export_success_message
from maphis.project.annotation import KeypointAnnotation, AnnotationType
from maphis.project.project import Project
from maphis.tools.landmarks import get_landmark_in_real_units

"""
GROUP: Export:Measurements
NAME: Export to CSV
KEY: export_csv
DESCRIPTION: Export measurements to CSV.
"""


@action_info('Export to CSV', 'Export measurements to a CSV file', 'Export:Measurements')
class ExportCSV(GeneralAction):
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, state: State, context: ActionContext) -> None:
        prop_tuple_list = get_prop_tuple_list(context)
        nd_props, other_props = _filter_by_NDArray(prop_tuple_list, context)

        file_grouped_props = _group_measurements_by_sheet(other_props, context)

        file_names: typing.List[str] = []

        for group_name, prop_list in file_grouped_props.items():
            path, _ = attempt_to_save_with_retries(write_results, 'Save as...', 'single_file', ['csv'],
                                         QApplication.activeWindow(),
                                         path=context.storage.location / f'{context.current_label_name}_results_{group_name}.csv',
                                         object=None, routine=_tabular_export_routine, prop_list=prop_list,
                                         context=context)
            # with open(context.storage.location / f'{context.current_label_name}_results_{group_name}.csv', 'w', newline='') as f:
            #     writer = csv.writer(f, dialect='excel')
            #     _tabular_export_routine(prop_list, writer.writerow, context)
            if path is not None:
                file_names.append(path.name)

        sheet_nd_props = _group_measurements_by_sheet(nd_props, context)

        for group_name, prop_list in sheet_nd_props.items():
            path, _ = attempt_to_save_with_retries(write_results, 'Save as...', 'single_file', ['csv'],
                                                   QApplication.activeWindow(),
                                                   path=context.storage.location / f'{context.current_label_name}_results_{group_name}.csv',
                                                   object=None, routine=_ndarray_export_routine, prop_list=prop_list,
                                                   context=context)
            # with open(context.storage.location / f'{context.current_label_name}_results_{group_name}.csv', 'w', newline='') as f:
            #     writer = csv.writer(f, dialect='excel')
            #     _ndarray_export_routine(prop_list, writer.writerow, context)
            if path is not None:
                file_names.append(path.name)

        landmark_csv_path = self._export_landmarks_to_csv(state.project, state.project.folder)
        if landmark_csv_path is not None:
            file_names.append(landmark_csv_path.name)

        # filenames = '\n'.join(file_names)
        # filenames = filenames[:-2]
        if len(file_names) > 0:
            show_export_success_message(context.storage.location, file_names, context)

    @property
    def general_action_context(self) -> GeneralActionContext:
        return GeneralActionContext.Measurements

    def _export_landmarks_to_csv(self, project: Project, folder: typing.Optional[Path]=None) -> typing.Optional[Path]:
        if folder is None:
            folder = project.folder
        exp_path = folder / 'landmarks.csv'
        try:
            with open(exp_path, 'w', newline='', encoding="utf-8") as csvfile:
                fieldnames = ['image_name', 'landmark_name', 'x (px)', 'y (px)', 'x (mm)', 'y (mm)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for photo in project.storage.images:
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
            return exp_path
        except Exception:
            # TODO handle specific errors
            return None


def write_results(path: Path, object: typing.Any, routine, prop_list, context: ActionContext) -> Path:
    with open(path, 'w',
              newline='') as f:
        writer = csv.writer(f, dialect='excel')
        routine(prop_list, writer.writerow, context)

    return path