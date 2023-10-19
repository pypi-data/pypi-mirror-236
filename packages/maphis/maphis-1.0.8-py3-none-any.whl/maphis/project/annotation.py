import dataclasses
import typing
from enum import IntEnum

from PySide6.QtCore import QObject, Signal


# class Annotation:
    # def __init__(self):
    #     self.name: str = ''
    #     self.origin: str = ''
    #     self.view: str = ''
    #     self.data: typing.Optional[typing.Union[ScalarValue, VectorValue, MatrixValue]] = None
    #
    # def to_dict(self) -> typing.Dict[str, typing.Any]:
    #     return {
    #         'name': self.name,
    #         'origin': self.origin,
    #         'view': self.view,
    #         'data': self.data.to_dict()
    #     }
    #
    # @classmethod
    # def from_dict(cls, _dict: typing.Dict[str, typing.Any]) -> 'Annotation':
    #     ann = Annotation()
    #     ann.name = _dict['name']
    #     ann.origin = _dict['origin']
    #     ann.view = _dict['view']
    #     ann.data = value_from_dict(_dict['data'])
    #
    #     return ann


class AnnotationType(IntEnum):
    Keypoint = 0
    AABBox = 1
    OBBox = 2
    Polygon = 3


class Annotation(QObject):
    new_annotation_data = Signal(object, object)
    modified_annotation_data = Signal(object, object)
    deleted_annotation_data = Signal(object, object)

    def __init__(self, ann_type: AnnotationType, _class: str, _id: int, instance_name: str='', _note: str='', parent: QObject=None):
        super().__init__(parent)
        self.type: AnnotationType = ann_type
        self.ann_class: str = _class
        self.ann_instance_id: int = _id
        self.ann_note: str = _note
        if instance_name == '' or instance_name is None:
            self.instance_name: str = f'{self.ann_class}_{self.ann_instance_id}'
        else:
            self.instance_name: str = instance_name
        self._annotations_counter: int = 0

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'type': self.type,
            'class': self.ann_class,
            'instance_id': self.ann_instance_id,
            'instance_name': self.instance_name,
            'note': self.ann_note,
            '_annotations_counter': self._annotations_counter
        }

    def __hash__(self) -> int:
        return hash((self.type, self.ann_class, self.ann_instance_id))

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


@dataclasses.dataclass
class Keypoint:
    name: str = ''
    x: int = -1
    y: int = -1
    v: int = -1
    color: typing.Tuple[int, int, int] = (250, 192, 33)
    deletable: bool = True
    additional_data: typing.Optional[typing.Any] = None
    id: int = -1

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        return hash(self.id) == hash(other)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'v': self.v,
            'color': self.color,
            'deletable': self.deletable,
            'additional_data': self.additional_data,
            'id': self.id
        }

    @staticmethod
    def from_dict(_dict: typing.Dict[str, typing.Any]) -> 'Keypoint':
        kp = Keypoint(
            _dict['name'],
            _dict['x'],
            _dict['y'],
            _dict['v'],
            _dict.get('color', (250, 192, 33)),
            _dict['deletable'],
            _dict['additional_data'],
            _dict['id']
        )
        return kp


class KeypointAnnotation(Annotation):
    def __init__(self, name: str, _id: int, instance_name: str='', _note: str='', kps: typing.Optional[typing.List[Keypoint]]=None):
        super().__init__(AnnotationType.Keypoint, _class=name, _id=_id, instance_name=instance_name, _note=_note)
        if kps is None:
            kps = list()
        self.kps: typing.List[Keypoint] = kps

    def _kp_index(self, kp_id: int) -> int:
        for i, kp in enumerate(self.kps):
            if kp.id == kp_id:
                return i
        return -1

    def add_keypoint(self, kp: Keypoint):
        kp.id = self._annotations_counter
        self._annotations_counter += 1
        self.kps.append(kp)
        self.new_annotation_data.emit(self, {'kp_index': len(self.kps) - 1, 'kp': self.kps[-1]})

    def delete_keypoint(self, kp: Keypoint):
        kp_idx = self._kp_index(kp.id)
        if kp_idx < 0:
            return
        kp = self.kps.pop(kp_idx)
        kp.v = -1
        self.deleted_annotation_data.emit(self, {'kp_index': kp_idx, 'kp': kp})

    def update_keypoint(self, kp: Keypoint):
        try:
            kp_idx: int = self.kps.index(kp)
            self.kps[kp_idx] = kp
            self.modified_annotation_data.emit(self, {'kp_index': kp_idx, 'kp': self.kps[kp_idx]})
        except ValueError:
            # add the keypoint into the annotation
            self.add_keypoint(kp)

    @property
    def instance_ids(self) -> typing.List[int]:
        return []

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        _dict = super().to_dict()
        return {
            **_dict,
            'keypoints': [kp.to_dict() for kp in self.kps]
        }

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, typing.Any]) -> 'KeypointAnnotation':
        kpa = KeypointAnnotation(_dict['class'], _dict['instance_id'], _dict['instance_name'], _dict['note'],
                                  [Keypoint.from_dict(kp_dict) for kp_dict in _dict['keypoints']])
        kpa._annotations_counter = _dict['_annotations_counter']
        return kpa


class AnnotationIDDispenser:
    def __init__(self, annotations: typing.List[Annotation]):
        self._annotations: typing.List[Annotation] = annotations

    def get_next_id(self) -> int:
        ann_ids = {annotation.ann_instance_id for annotation in self._annotations}

        for i in range(max(ann_ids, default=0) + 1):
            if i not in ann_ids:
                return i
