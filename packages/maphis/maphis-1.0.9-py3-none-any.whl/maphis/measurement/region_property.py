from enum import IntEnum
from pathlib import Path
from typing import Optional

import typing

from PySide6.QtGui import QPixmap
from maphis.common.common import Info
from maphis.measurement.values import Value, ScalarValue, VectorValue, MatrixValue, ureg, ValueType


class PropertyType(IntEnum):
    String = 0,
    Scalar = 1,
    Vector = 2,
    Intensity = 3,
    Other = 4
    NDArray = 5
    IntensityHSV = 6


class RegionProperty:
    """A class representing a property for a specific region.
    """

    def __init__(self):
        self._info: Optional[Info] = None
        self.label: int = -1
        # self.prop_type: PropertyType = PropertyType.Scalar
        # self.value: Optional[Union[Value, Tuple[List[Any], Union[CompoundUnit, Unit]]]] = None  # either Value, or a tuple of list of values(float, int...) and a Unit
        # self.num_vals: int = 1
        # self._val_names: typing.List[str] = []  # names of individual scalar values or matrices
        # self.col_names: typing.List[str] = []  # in the case when self.prop_type = PropertyType.NDArray
        # self.row_names: typing.List[str] = []  # same here
        self.value: typing.Optional[Value] = None
        self.vector_viz: Optional[QPixmap] = None

        self._str_rep: str = ''
        self._update_str_rep()

        self.prop_comp_key: str = ''
        self.local_key: str = ''
        self.settings: typing.Dict[str, typing.Dict[str, str]] = {}
        self._up_to_date: bool = True
        self.image_path: Path = Path()

    @property
    def info(self) -> Optional[Info]:
        return self._info

    @info.setter
    def info(self, info: Optional[Info]):
        self._info = info
        self._update_str_rep()

    @property
    def prop_key(self) -> str:
        return f'{self.prop_comp_key}.{self.local_key}'

    def __str__(self) -> str:
        # return f'{self.info.name}: {self.format_value()} {self.unit}'
        # if len(self._str_rep) == 0:
        #     self._update_str_rep()
        # return self._str_rep
        return f'{"" if self._info is None else self._info.name}: {self.value.value}'

    def _update_str_rep(self):
        if self.value is None:
            return
        # if isinstance(self.value, Value):
        self._str_rep = f'{"" if self._info is None else self._info.name}: {self.value.value}'
        # return
        # val_str = self.format_value()
        # self._str_rep = f'{"" if self._info is None else self.info.name}: {val_str} {self.value.value}'

    @property
    def prop_type(self) -> PropertyType:
        return self.value.value_type

    # def format_value(self) -> str:
    #     if self.prop_type == PropertyType.Scalar:  # So self.value is of type `Value`
    #         # if type(self.value) == float:
    #         #     return f'{self.value:.2f}'
    #         return str(self.value)
    #     elif self.prop_type == PropertyType.Intensity: # self.value is of type Tuple[List[Any], CompoundUnit]
    #         if self.num_vals == 1:
    #             if type(self.value[0][0]) == float:
    #                 return f'{self.value[0][0]:.2f} {self.val_names[0]}'
    #             return f'{self.value[0][0]} {self.val_names[0]}'
    #         else:
    #             val_string = '('
    #             for i in range(self.num_vals):
    #                 val_string += f'{self.value[0][i]:.2f} {self.val_names[i]}, '
    #             return val_string[:-2] + ')'
    #     elif self.prop_type == PropertyType.Vector:
    #         val_string = ''
    #         for i in range(self.num_vals):
    #             val_string += f'{self.value[0][i]:.2f}, '
    #         return val_string[:-2]
    #     else:
    #         val_string = ''
    #         #print(f"self.prop_type: {self.prop_type}")
    #         #print(f"self.num_vals: {self.num_vals}")
    #         #print(f"self.value: {self.value}")
    #         for i in range(self.num_vals):
    #             val_string += f'{self.value[0][i]}, '
    #         #print(f"val_string[:-2]: {val_string[:-2]}")
    #         return val_string[:-2]
    #     raise ValueError(f'Unsupported type of value: {type(self.value)}')

    # @property
    # def val_names(self) -> typing.List[str]:
    #     if len(self._val_names) == 0:
    #         return [f'value_{i}' for i in range(self.num_vals)]
    #     return self._val_names

    # @val_names.setter
    # def val_names(self, val_names: typing.Sequence[str]):
    #     self._val_names = list(val_names)

    @classmethod
    def from_dict(cls, dict_obj: typing.Dict[str, typing.Any]) -> 'RegionProperty':
        reg_prop = RegionProperty()
        reg_prop.label = dict_obj['label']

        # check whether `value_dict` is an actual `dict` - meaning it is an actual `Value` implementation
        # or if it is a string, indicating that it is the previous version of Value storage
        if dict_obj.get('property_version', 1.0) < 2.0:
            raise 
            # __type = PropertyType(dict_obj['prop_type'])
            # value_dict = {
            #
            # }
            #
            # if __type == PropertyType.Scalar:
            #     value = ScalarValue(0 * ureg('pixel'))
            #     value_dict = value.to_dict()
            #     value_dict['value'] =
            # elif __type == PropertyType.NDArray:
            #     path_unit = eval(dict_obj['value'])
            #     ndarr = np.load(path_unit[0])
            #     unit: Unit = path_unit[1]
            #     reg_prop.value = (np.load(path_unit[0]), path_unit[1])
        else:
            value_dict = dict_obj['value']

        image_path: Path = dict_obj['image_path']

        if (value_type := ValueType(value_dict['type'])) == ValueType.Scalar:
            reg_prop.value = ScalarValue.from_dict(value_dict)
        elif value_type == ValueType.Vector:
            reg_prop.value = VectorValue.from_dict(value_dict)
        elif value_type == ValueType.Matrix:
            value_dict['path_to_value'] = image_path.parent / value_dict['path_to_value']
            reg_prop.value = MatrixValue.from_dict(value_dict)
        reg_prop.prop_comp_key = dict_obj['prop_comp_key']
        reg_prop.local_key = dict_obj['local_key']
        reg_prop.settings = dict_obj['settings']
        reg_prop._up_to_date = dict_obj.get('up_to_date', True)
        info = Info()
        info.name = dict_obj['name']
        info.key = dict_obj['key']
        info.description = dict_obj['description']
        reg_prop.info = info
        return reg_prop

    def to_dict(self, **kwargs) -> typing.Dict[str, typing.Any]:
        return {
            'name': self.info.name,
            'label': self.label,
            'value': self.value.to_dict(**kwargs),
            'key': self.info.key,
            'description': self.info.description,
            'prop_comp_key': self.prop_comp_key,
            'local_key': self.local_key,
            'settings': self.settings,
            'up_to_date': self.up_to_date,
            'property_version': 2.0
        }

    def __hash__(self) -> int:
        # return hash((self.info.key, self.label))
        return hash((self.prop_key, self.label))

    def __eq__(self, other) -> bool:
        if not isinstance(other, RegionProperty):
            return False
        return hash(self) == hash(other)

    @property
    def up_to_date(self) -> bool:
        return self._up_to_date

    @up_to_date.setter
    def up_to_date(self, is_up_to_date: bool):
        self._up_to_date = is_up_to_date
        # TODO fire a signal
