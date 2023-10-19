import json
import typing
from pathlib import Path

from maphis.common.label_hierarchy import LabelHierarchy
from maphis.common.label_image import LabelImgInfo
from maphis.common.local_storage import LocalStorage
from maphis.common.storage import Storage


class Project:
    PROJECT_FILE_VERSION = '1.0'

    def __init__(self):
        self._project_name: str = ''
        self._project_type: str = ''
        self._origin: str = ''
        self._folder: Path = Path()
        self._label_images_info: typing.Dict[str, LabelImgInfo] = {}
        self._default_label_image_name: str = ''
        self._storage: typing.Optional[Storage] = None
        self._loaded_plugins: typing.List[str] = []

    @staticmethod
    def load_from(folder: Path) -> typing.Optional['Project']:
        if not folder.exists() or not (folder / 'project_info.json').exists():
            return None
        with open(folder / 'project_info.json', 'r') as f:
            project_info = json.load(f)
        if project_info['project_file_version'] != Project.PROJECT_FILE_VERSION:
            return None
        project = Project()
        project._folder = folder
        project._project_type = project_info['project_type']
        project._origin = project_info['origin']
        project._project_name = project_info['project_name']
        project._loaded_plugins = project_info['plugins']

        label_images_info = project_info['label_images_info']

        for label_img_info_dict in label_images_info['label_images']:
            lbl_info = LabelImgInfo.from_dict(label_img_info_dict)
            label_hierarchy = LabelHierarchy.load_from(project._folder / label_img_info_dict['label_hierarchy_file'])
            lbl_info.label_hierarchy = label_hierarchy
            project._label_images_info[lbl_info.name] = lbl_info
            if lbl_info.is_default:
                project._default_label_image_name = lbl_info.name
        project._storage = LocalStorage.load_from(folder, project._label_images_info)
        project._storage._label_hierarchies = {
            label_name: label_info.label_hierarchy  for label_name, label_info in project._label_images_info.items()
        }
        return project

    @property
    def project_type(self) -> str:
        return self._project_type

    @property
    def origin(self) -> str:
        return self._origin

    @property
    def folder(self) -> Path:
        return self._folder

    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def label_images_info(self) -> typing.Dict[str, LabelImgInfo]:
        return self._label_images_info

    @property
    def default_label_image(self) -> str:
        return self._default_label_image_name

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def loaded_plugins(self) -> typing.List[str]:
        return self._loaded_plugins

    def save(self) -> bool:
        try:
            self._storage.save()
            with open(self._folder / 'project_info.json', 'w') as f:
                project_dict = {
                    'project_file_version': Project.PROJECT_FILE_VERSION,
                    'project_type': self._project_type,
                    'origin': self._origin,
                    'project_name': self._project_name,
                    'label_images_info': {
                        'label_images': [
                            label_img_info.to_dict() for label_img_info in self._label_images_info.values()
                        ]
                    },
                    'plugins': self._loaded_plugins
                }
                json.dump(project_dict, f, indent=2)
        except Exception as e:
            return False
        return True

    def is_approved(self, photo_idx) -> bool:
        photo = self.storage.images[photo_idx]
        return photo.approved[self.default_label_image] == self.label_images_info[self.default_label_image].label_hierarchy.hierarchy_levels[-1].name
