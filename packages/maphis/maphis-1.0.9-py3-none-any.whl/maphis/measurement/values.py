import abc
from enum import IntEnum
import typing
from pathlib import Path

import numpy as np
import pint

from maphis.common.units import LegacyValue


ureg = pint.UnitRegistry(Path(__file__).parent / 'default_en.txt')
ureg.default_format = '~P'


class ValueType(IntEnum):
    Scalar = 0
    Vector = 1
    Matrix = 2


class Value(abc.ABC):
    def __init__(self, value: pint.Quantity):
        self._value: pint.Quantity = value

    @property
    def value(self) -> pint.Quantity:
        return self._value

    @value.setter
    def value(self, val: pint.Quantity):
        self._value = val

    @property
    def value_type(self) -> ValueType:
        return ValueType.Scalar

    @property
    def count(self) -> int:
        return 0

    @property
    def unit(self) -> pint.Unit:
        return self._value.units

    @property
    def raw_value(self) -> typing.Union[float, np.ndarray]:
        return self._value.magnitude

    def __str__(self) -> str:
        return f'{self.value:.3f~#P}'

    def to_dict(self, **kwargs) -> typing.Dict[str, str]:
        return {}

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, str]) -> typing.Optional['Value']:
        return None

    def __add__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `+` (__add__) is not supported for the types {type(self)} and {type(other)}.')
        return self.value.__add__(value)

    def __sub__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `-` (__sub__) is not supported for the types {type(self)} and {type(other)}.')
        return self.value.__sub__(value)

    def __mul__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `*` (__mul__) is not supported for the types {type(self)} and {type(other)}.')
        return self.value.__mul__(value)

    def __truediv__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `/` (__truediv__) is not supported for the types {type(self)} and {type(other)}')
        return self.value.__truediv__(value)

    def __mod__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `__mod__` is not supported for the types {type(self)} and {type(other)}')
        return self.value.__mod__(value)

    def __divmod__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `__divmod__` is not supported for the types {type(self)} and {type(other)}.')
        return self.value.__divmod__(value)

    def __floordiv__(self, other) -> pint.Quantity:
        if isinstance(other, Value):
            value = other.value
        elif isinstance(other, pint.Quantity):
            value = other
        else:
            raise TypeError(f'The operator `__floordiv__` is not supported for the types {type(self)} and {type(other)}.')
        return self.value.__floordiv__(value)

    def __pow__(self, power, modulo=None) -> pint.Quantity:
        return self.value.__pow__(power, modulo)


class ScalarValue(Value):
    def __init__(self, value: pint.Quantity):
        super().__init__(value)

    @property
    def count(self) -> int:
        return 1

    @property
    def value_type(self) -> ValueType:
        return ValueType.Scalar

    def to_dict(self, **kwargs) -> typing.Dict[str, str]:
        return {
            'type': self.value_type,
            'value': str(self._value.magnitude),
            'units': str(self._value.units),
            'dtype': str(self.raw_value.dtype) if type(self.raw_value) == np.ndarray else type(self.raw_value).__name__
        }

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, str]) -> typing.Optional['ScalarValue']:
        """
        Constructs a `ScalarValue` from a dictionary. Raises KeyError if the dictionary does not
        have all the needed fields.
        """
        return ScalarValue(ureg.Quantity(_dict['value'] + ' ' + _dict['units']))


class VectorValue(Value):
    def __init__(self, value: pint.Quantity):
        super().__init__(value)
        self._column_names: typing.List[str] = []

    @property
    def count(self) -> int:
        return self._value.magnitude.shape[0]

    @property
    def value_type(self) -> ValueType:
        return ValueType.Vector

    @property
    def column_names(self) -> typing.List[str]:
        if len(self._column_names) < self.count:
            self._column_names = [f'col_{i}' for i in range(self.count)]
        return self._column_names

    @column_names.setter
    def column_names(self, cnames: typing.Iterable[str]):
        self._column_names = list(cnames)

    def to_dict(self, **kwargs) -> typing.Dict[str, str]:
        return {
            'type': self.value_type,
            'shape': self.raw_value.shape,
            'value': np.array_str(self._value.magnitude).replace('[', '').replace(']', '').replace('\n', ''),
            'units': str(self._value.units),
            'column_names': self.column_names,
            'dtype': str(self.raw_value.dtype)
        }

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, str]) -> 'VectorValue':
        """
        Constructs a `VectorValue` from a dictionary. Raises KeyError if the dictionary does not
        have all the needed fields.
        """
        raw_vals_str = _dict['value']
        unit_str = _dict['units']
        raw_value = np.fromstring(raw_vals_str, dtype=np.dtype(_dict['dtype']), sep=' ')
        unit = ureg(unit_str)
        value = raw_value * unit
        vec_value = VectorValue(value)
        vec_value.column_names = _dict['column_names']

        return vec_value


class MatrixValue(Value):
    def __init__(self, value: pint.Quantity):
        super().__init__(value)
        self._row_names: typing.List[str] = []
        self._column_names: typing.List[str] = []
        self._channel_names: typing.List[str] = []

    @property
    def value_type(self) -> ValueType:
        return ValueType.Matrix

    @property
    def count(self) -> int:
        return len(self._value.magnitude)

    @property
    def dims(self) -> int:
        return self._value.magnitude.dim

    @property
    def row_count(self) -> int:
        return self._value.magnitude.shape[1]

    @property
    def column_count(self) -> int:
        return self._value.magnitude.shape[2]

    @property
    def channel_count(self) -> int:
        return self._value.magnitude.shape[0]

    @property
    def row_names(self) -> typing.List[str]:
        if len(self._row_names) < self.row_count:
            self._row_names = [f'row_{i}' for i in range(self.row_count)]
        return self._row_names

    @row_names.setter
    def row_names(self, rnames: typing.Iterable[str]):
        self._row_names = list(rnames)

    @property
    def column_names(self) -> typing.List[str]:
        if len(self._column_names) < self.column_count:
            self._column_names = [f'col_{i}' for i in range(self.column_count)]
        return self._column_names

    @column_names.setter
    def column_names(self, cnames: typing.Iterable[str]):
        self._column_names = list(cnames)

    @property
    def channel_names(self) -> typing.List[str]:
        if len(self._channel_names) < self.channel_count:
            self._channel_names = [f'ch_{i}' for i in range(self.channel_count)]
        return self._channel_names

    @channel_names.setter
    def channel_names(self, chnames: typing.Iterable[str]):
        self._channel_names = list(chnames)

    @property
    def raw_value(self) -> np.ndarray:
        return self._value.magnitude

    def to_dict(self, **kwargs) -> typing.Dict[str, str]:
        ndarr = self._value.magnitude
        folder: typing.Optional[Path] = kwargs.get('label_folder', None)
        npy_fname: typing.Optional[str] = kwargs.get('npy_fname', None)
        if folder is not None:
            if npy_fname is not None:
                np.save(str(folder / npy_fname), ndarr)
            else:
                raise ValueError(f'Provide a name for the file to be save in the folder {folder}')
            value = None
        else:
            value = np.array_str(self.raw_value).replace('[', '').replace(']', '').replace('\n', '')
        return {
            'type': self.value_type,
            'shape': self.raw_value.shape,
            'value': value,
            'path_to_value': npy_fname,
            'units': str(self._value.units),
            'row_names': self.row_names,
            'column_names': self.column_names,
            'channel_names': self.channel_names,
            'dtype': str(self.raw_value.dtype)
        }

    @classmethod
    def from_dict(cls, _dict: typing.Dict[str, str]) -> 'MatrixValue':
        """
        Constructs a `MatrixValue` from a dictionary. Raises KeyError if the dictionary does not
        have all the needed fields.
        """
        matrix_path = Path(_dict['path_to_value']) if _dict.get('path_to_value', None) is not None else None
        if matrix_path is not None:
            ndarr = np.load(str(matrix_path))
        else:
            ndarr = np.fromstring(_dict['value'], dtype=np.dtype(_dict['dtype']), sep=' ').reshape(_dict['shape'])
        units = ureg(_dict['units'])
        matrix_val = MatrixValue(ndarr * units)
        matrix_val.row_names = _dict['row_names']
        matrix_val.column_names = _dict['column_names']
        matrix_val.channel_names = _dict['channel_names']
        return matrix_val


def value_from_dict(_dict: typing.Dict[str, typing.Any]) -> typing.Union[ScalarValue, VectorValue, MatrixValue]:
    value_type = ValueType(_dict['type'])
    if value_type == ValueType.Scalar:
        return ScalarValue.from_dict(_dict)
    elif value_type == ValueType.Vector:
        return VectorValue.from_dict(_dict)
    return MatrixValue.from_dict(_dict)


unitless_vector = typing.Union[typing.List[int], typing.List[float]]


class UnitlessVaue(abc.ABC):
    def __init__(self):
        self._value: typing.Any = None

    @property
    def value(self) -> typing.Any:
        return self._value

    @value.setter
    def value(self, val: typing.Any):
        pass


class UnitlessScalar(UnitlessVaue):
    def __init__(self, value: typing.Union[int, float]):
        super().__init__()
        self._value: typing.Union[int, float] = value

    @property
    def value(self) -> typing.Union[int, float]:
        return self._value

    @value.setter
    def value(self, val: typing.Union[int, float]):
        self._value = val


class UnitlessVector(UnitlessVaue):
    def __init__(self, value: unitless_vector):
        super().__init__()
        self._value: unitless_vector = value

    @property
    def value(self) -> unitless_vector:
        return self._value

    @value.setter
    def value(self, val: unitless_vector):
        self._value = val


class UnitlessMatrix(UnitlessVaue):
    def __init__(self, value: np.ndarray):
        super().__init__()
        self._value: np.ndarray = value

    @property
    def value(self) -> np.ndarray:
        return self._value

    @value.setter
    def value(self, val: np.ndarray):
        self._value = val


def convert_legacy_value_to_new_value(legacy_value: LegacyValue) -> ScalarValue:
    pint_unit = ureg(str(legacy_value.unit))

    return legacy_value.value * pint_unit
