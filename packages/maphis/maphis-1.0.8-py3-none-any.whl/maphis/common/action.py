import abc
import copy
import inspect
import typing
from enum import IntEnum

import pint
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget

from maphis.common.param_widget import ParamWidget
from maphis.common.storage import Storage
from maphis.measurement.region_property import RegionProperty
from maphis.measurement.values import ScalarValue, ureg, VectorValue
from maphis.common.common import Info
from maphis.common.label_image import LabelImg
from maphis.common.photo import Photo
from maphis.common.regions_cache import RegionsCache
from maphis.common.state import State
from maphis.common.utils import get_dict_from_doc_str
from maphis.common.user_param import Param, ParamBuilder


class Action:
    """A class specifying the common interface for `RegionComputation`, `PropertyComputation` and `GeneralAction`.

    Attributes:
        info (Info): metadata
        _user_params (Dict[str, Param]): dictionary of user `Param`s. It is up to the programmer under what
            keys the `Param`s are stored.
        _group (str): a category where this `Action` belongs.
        _settings_widget (Optional[ParamWidget]): an optional `ParamWidget` if you want to parameters to the user
    """

    FOLDER = ''
    TEMPLATE = ''
    default_user_params: typing.Dict[str, Param] = {}

    def __init__(self, info: typing.Optional[Info] = None):
        self.info = Info() if info is None else info
        self._user_params: typing.Dict[str, Param] = self.default_user_params
        self._group = 'General'
        self._default_call_func = None
        self._setting_widget: typing.Optional[ParamWidget] = None

    @property
    def user_params(self) -> typing.List[Param]:
        """
        Returns:
            list of `Param` instances.
        """
        return list(self._user_params.values())

    @property
    def user_params_dict(self) -> typing.Dict[str, Param]:
        return self._user_params

    @property
    def can_be_executed(self) -> typing.Tuple[bool, str]:
        """Determines whether this `Action` can be executed or not.

        Returns:
            `(True, <message>)` if this `Action` can be executed, otherwise `(False, <message>)`. Generally, `<message>`
             is presented to the user in a GUI dialog window to let the user know why the `Action` cannot be executed.
        """
        return True, ''

    @property
    def group(self) -> str:
        """Group the Action belongs to.
        It is used to organize `PropertyComputation`s, or where to put `GeneralAction`s in the application's
        menu bar.
        """
        return self._group

    def __hash__(self) -> int:
        return hash(self.info.key)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        """An optional widget containing parameters to customize the `Action`s behaviour.
        Returns:
            optional widget with user parameters.
        """
        if len(self._user_params) > 0 and self._setting_widget is None:
            self._setting_widget = ParamWidget(list(self._user_params.values()))
        return None if self._setting_widget is None else self._setting_widget.widget

    def _setup_params(self):
        pass

    def current_settings_to_str_dict(self) -> typing.Dict[str, typing.Dict[str, str]]:
        """Serialize the current values of user parameters provided by the `Action` into a dictionary.
        The returned dictionary has 2 entries:
            - 'standard_parameters' -> a dictionary of serialized `Param` values, keyed by the keys of
                `self._user_params`
            - 'custom_parameters' -> this can be anything, it is up to the `Action` implementation to correctly
                deserialize in the method `Action.setup_settings_from_dict`.

        Returns:
            dictionary of string representations of user parameters for this `Action`
        """
        return {
            'standard_parameters': {param_key: str(param.value) for param_key, param in self._user_params.items()},
            'custom_parameters': {}
        }

    def setup_settings_from_dict(self, _dict: typing.Dict[str, typing.Dict[str, str]]):
        """Deserializes parameter values from the provided `_dict` argument.
        Custom implementation of subclasses of `Action` must take care of properly deserializing values stored under the
        'custom_parameters' key.

        Args:
            _dict: string representations of parameter values
        """
        standard_params: typing.Dict[str, str] = _dict['standard_parameters']
        for param_key, param_value_str in standard_params.items():
            param_obj: Param = self.user_params_dict[param_key]
            param_obj.parse(param_value_str)

    def initialize(self) -> typing.Tuple[bool, str]:
        """Prepare everything before executing the `Action` such as loading heavy resources etc.

        Returns:
            `(True, <message>)` if the `Action` is properly initialized, `(False, <message>)` otherwise. Generally,
                `<message>` is displayed inside a GUI dialog window to let the user know why the initialization failed.
        """
        return True, ''


class RegionComputation(Action):
    """Base class for custom `RegionComputation`s.
    """
    FOLDER = 'regions'
    TEMPLATE = 'region_computation_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(RegionComputation, self).__init__(info)
        self._region_restricted = False if self.__doc__ is None else "REGION_RESTRICTED" in self.__doc__

    @classmethod
    def from_call_func(cls, func: typing.Callable[[Photo, typing.Optional[typing.Set[int]], typing.Optional[Storage]], typing.List[LabelImg]]) -> 'RegionComputation':
        if hasattr(func, 'info'):
            info = func.info
        else:
            info = None
        comp = RegionComputation(info)
        comp._default_call_func = func
        if hasattr(func, '_group'):
            comp._group = func._group
        if (params_dict := getattr(func, 'maphis_params', None)) is not None:
            comp._user_params = params_dict
        return comp

    @abc.abstractmethod
    def __call__(self, photo: Photo, labels: typing.Optional[typing.Set[int]] = None, storage: typing.Optional[Storage]=None) -> typing.List[LabelImg]:
        """The actual implementation of the functionality that is to be provided.

        Args:
            photo: the photo that the `RegionComputation` should compute for.
            labels: restrict the computation on this set of labels
            storage: the `Storage` the photo belongs to

        Returns:
            list of `LabelImg`s that were modified. The `LabelImg`s in the list must originate from `photo`.
        """
        if self._default_call_func is not None:
            return self._default_call_func(self, photo, labels, storage)
        return []

    @property
    def region_restricted(self) -> bool:
        return self._region_restricted


class PropertyComputation(Action):
    """Base class for custom `PropertyComputation`s

    Attributes:
        _units (pint.UnitRegistry): the unit registry (`pint.UnitRegistry`) that is used by the application.
        _pixels: (pint.Unit): pixels unit
        _no_unit (pint.Unit): `no unit` for unitless dimensionless values
        example_props_dict (Dict[str, RegionProperty]): dictionary of exemplary `RegionProperty`s
        _export_target (str): the values computed by this computation will be stored in the sheet (xlsx export) or
            file (csv export) named by the value specified by this variable.
    """
    FOLDER = 'properties'
    TEMPLATE = 'property_computation_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(PropertyComputation, self).__init__(info)
        # doc_dict = get_dict_from_doc_str(self.__doc__)
        self._region_restricted = self.__doc__ is not None and "REGION_RESTRICTED" in self.__doc__
        self._units: pint.UnitRegistry = ureg
        self._pixels: pint.Unit = self._units['pixel']
        self._no_unit: pint.Unit = self._units['dimensionless']
        self.example_props_dict: typing.Dict[str, RegionProperty] = {}
        self._export_target: str = 'common'
        self._computes_dict: typing.Dict[str, Info] = {}

    @abc.abstractmethod
    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, props: typing.List[str]) -> typing.List[RegionProperty]:
        """The actual computation of the property. The property is computed for the `photo` and only for
        regions specified by `region_labels`. If this computation allows to compute various variants, they will be
        specified in `props` (for example, when you are computing GLCM properties, you have these options to compute:
        'Contrast', 'Dissimilarity', 'Energy' and some more. These are considered as variants).

        Args:
            photo: photo for which to compute the property
            region_labels: labels of regions that we want to compute the property for
            regions_cache: regions cache for efficient access to regions
            props: which variants of the property (if any) to compute

        Returns:
            list of properties computed for the photo.
        """
        if self._default_call_func is not None:
            return self._default_call_func(self, photo, region_labels, regions_cache, props)
        return []

    @property
    def region_restricted(self) -> bool:
        return self._region_restricted

    @property
    @abc.abstractmethod
    def computes(self) -> typing.Dict[str, Info]:
        return {k: rp.info for k, rp in self.example_props_dict.items()}

    @abc.abstractmethod
    def example(self, prop_name: str) -> RegionProperty:
        if len(self.example_props_dict) > 0:
            return copy.deepcopy(self.example_props_dict[prop_name])
        prop = RegionProperty()
        prop.prop_comp_key = self.info.key
        prop.local_key = prop_name
        prop.info = copy.deepcopy(self.info)
        prop.settings = self.current_settings_to_str_dict()
        prop.value = ScalarValue(1 * self._no_unit)
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return self._export_target

    @property
    @abc.abstractmethod
    def requested_props(self) -> typing.List[str]:
        return []

    @classmethod
    def get_representation(cls, reg_prop: RegionProperty, role: Qt.ItemDataRole, alternative_rep: bool=False) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return str(reg_prop.value)
        return None

    @classmethod
    def from_call_func(cls, _func) -> 'PropertyComputation':
        if hasattr(_func, 'info'):
            info = _func.info
        else:
            info = None
        comp = PropertyComputation(info)
        if hasattr(_func, '_group'):
            comp._group = _func._group
        if (params_dict := getattr(_func, 'maphis_params', None)) is not None:
            comp._user_params = params_dict
        comp._default_call_func = _func
        comp.example_props_dict = _func.example_property
        comp._export_target = _func.export_target
        return comp


class GeneralActionContext(IntEnum):
    """The necessary context in which a [GeneralAction][maphis.common.action.GeneralAction] is enabled.
    """
    Application = 0
    Project = 1
    Photo = 2
    LabelImg = 3
    LabelEditor = 4
    Measurements = 5


class GeneralAction(Action):
    """Base class for custom [GeneralAction][maphis.common.action.GeneralAction].
    """

    FOLDER = 'general'
    TEMPLATE = 'general_action_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(GeneralAction, self).__init__(info)
        self._general_action_context: GeneralActionContext = GeneralActionContext.Application

    @classmethod
    def from_call_func(cls, _func: typing.Callable[[State, 'ActionContext'], None]) -> 'GeneralAction':
        if hasattr(_func, 'info'):
            info = _func.info
        else:
            info = None
        gen_act = GeneralAction(info)
        if hasattr(_func, '_group'):
            gen_act._group = _func._group
        if hasattr(_func, 'general_action_context'):
            gen_act._general_action_context = _func.general_action_context
        gen_act._default_call_func = _func

        return gen_act

    @abc.abstractmethod
    def __call__(self, state: State, context: 'ActionContext') -> None:
        if self._default_call_func is not None:
            return self._default_call_func(self, state, context)

    @property
    def general_action_context(self) -> GeneralActionContext:
        return self._general_action_context


def action_info(name: str, description: str, group: str="General")\
        -> typing.Union[GeneralAction, PropertyComputation, RegionComputation, typing.Callable[[typing.Any], typing.Any]]:
    """Decorator to provide information about [Action][maphis.common.action.Action] subclasses. By an [Action][maphis.common.action.Action] subclass it is understood either
    classes that subclass [GeneralAction][maphis.common.action.GeneralAction], [RegionComputation][maphis.common.action.RegionComputation]
     or [PropertyComputation][maphis.common.action.PropertyComputation], or functions that are
    decorated by [@region_computation][maphis.common.action.region_computation], [@scalar_property_computation][maphis.common.action.scalar_property_computation],
    [@vector_property_computation][maphis.common.action.vector_property_computation] or [@general_action][maphis.common.action.general_action].

    Args:
        name (str): the name - how it would be shown in GUI
        description (str): description of what it does
        group (str): category - for `GeneralAction`s it determines the placement in the menu bar, e.g. 'File:Export:as JSON' will make it accessible
            in the menu bar as 'File>Export>as Json'. For `PropertyComputation`s it determines the category in the
            dialog for computing new properties.

    Returns:
        the decorated `Action` subclass or function
    """
    def wrap(_obj: object):
        if inspect.isclass(_obj):
            old_init = _obj.__init__

            def __init__(self, *args, **kwargs):
                old_init(self, *args, **kwargs)
                self.info = Info(name, description, f'{_obj.__module__}.{_obj.__name__}')
                self._group = group
            _obj.__init__ = __init__
            return _obj
        elif inspect.isfunction(_obj):
            func_name = _obj.__name__
            _obj.info = Info(name, description, f'{_obj.__module__}.{func_name}')
            _obj._group = group
            return _obj
    return wrap


def region_computation(name: str, description: str, group: str="General") \
        -> typing.Callable[[RegionComputation, Photo, typing.Optional[typing.Set[int]], Storage], typing.List[LabelImg]]:
    """Decorator to turn a function of appropriate signature into a [`RegionComputation`][maphis.common.action.RegionComputation] subclass.
    The function signature is expected to be one of these two:
    1. <func_name>(`RegionComputation`, `Photo`, *args) -> List[`LabelImg`]
    2. <func_name>(`RegionComputation`, `Photo`, Optional[Set[int]], `Storage`) -> List[`LabelImg`]

    `<func_name>` is used as a key of your computation in MAPHIS and will be stored in project files to correctly
    identify the origin of results (segmentations, properties, etc.), so it's good provide clear and easy to interpret
    name for your function.

    Args:
        name: name of the `RegionComputation`
        description: what this computation does
        group: category, most likely will be 'Segmentation' for `RegionComputation`, but not limited to.

    Returns:
       the decorated function which will be turned into `RegionComputation` by MAPHIS.
    """
    def wrap(_func: typing.Callable[[RegionComputation, Photo, typing.Optional[typing.Set[int]], Storage], typing.List[LabelImg]]):
        action_wrapped = action_info(name, description, group)(_func)
        action_wrapped.action_type = 'region'
        return action_wrapped
    return wrap


def general_action(name: str, description: str, group: str="General",
                   general_action_context: GeneralActionContext=GeneralActionContext.Application) \
        -> typing.Callable[[GeneralAction, State, 'ActionContext'], None]:
    """Decorator to turn a function of appropriate signature into a `GeneralAction` subclass.
    The function signature is expected to be as follows:
    <func_name>(`GeneralAction`, `State`, `ActionContext`) -> None

    `<func_name>` is used as a key of your computation in MAPHIS and will be stored in project files to correctly
    identify the origin of results (segmentations, properties, etc.), so it's good provide clear and easy to interpret
    name for your function.

    Args:
        name: name of the `GeneralAction`
        description: what this action does
        group: placement of this action in the menu bar, e.g. `File:Save as:Json` will place this action under `File>Save as>Json` menu bar entry.
        general_action_context (GeneralActionContext): what is the necessary context for this action to be enabled in

    Returns:
       the decorated function which will be turned into `GeneralAction` by MAPHIS.
    """

    def wrap(_func: typing.Callable[[GeneralAction, State, 'ActionContext'], None]):
        action_wrapped = action_info(name, description, group)(_func)
        action_wrapped.action_type = 'general'
        action_wrapped.general_action_context = general_action_context
        return action_wrapped
    return wrap


def _define_property_computation(name: str, description: str, group: str, export_target: str):
    def wrap(_func: typing.Callable[[Photo, typing.List[int], RegionsCache, typing.List[str]], typing.List[RegionProperty]]):
        action_wrapped = action_info(name, description, group)(_func)
        action_wrapped.action_type = 'property'
        action_wrapped.export_target = export_target
        return action_wrapped
    return wrap


def scalar_property_computation(name: str, description: str, group: str, export_target: str, default_value: ScalarValue)\
        -> typing.Callable[[PropertyComputation, Photo, typing.List[int], RegionsCache, typing.List[str]], typing.List[RegionProperty]]:
    """Decorator to turn a function of appropriate signature into a [`PropertyComputation`][maphis.common.action.PropertyComputation] subclass that generates
    scalar properties.
    The function signature is expected to be as follows:
    <func_name>([`PropertyComputation`][maphis.common.action.PropertyComputation], [`Photo`][maphis.common.photo.Photo], List[int], `RegionsCache`, List[str]) -> List[`RegionProperty`]

    `<func_name>` is used as a key of your computation in MAPHIS and will be stored in project files to correctly
    identify the origin of results (segmentations, properties, etc.), so it's good provide clear and easy to interpret
    name for your function.

    Args:
        name: name of the [`PropertyComputation`][maphis.common.action.PropertyComputation]
        description: what kind of scalar property this computation computes
        group: category of property, e.g., 'Dimensions', 'Shape',... (see the `Compute new measurements` dialog in MAPHIS)
        export_target (str): name of the sheet in Excel spreadsheet where values of this property will be stored. In case of CSV export, `export_target` will be a suffix of one of the generated csv files.
        default_value (ScalarValue): default value for this property

    Returns:
        the decorated function which will be turned into [`PropertyComputation`][maphis.common.action.PropertyComputation] by MAPHIS.
    """
    def wrap(_func: typing.Callable[[PropertyComputation, Photo, typing.List[int], RegionsCache, typing.List[str]], typing.List[RegionProperty]]):
        _comp_wrapped = _define_property_computation(name, description, group, export_target)(_func)
        prop = RegionProperty()
        prop.value = default_value
        prop.label = 0
        prop.prop_comp_key = _comp_wrapped.info.key
        prop.local_key = _func.__name__
        prop.info = _comp_wrapped.info
        _comp_wrapped.example_property = {_func.__name__: prop}
        return _comp_wrapped

    return wrap


def vector_property_computation(name: str, description: str, group: str, export_target: str,
                                value_count: int, value_names: typing.List[str], unit: pint.Unit) -> \
        typing.Callable[[PropertyComputation, Photo, typing.List[int], RegionsCache, typing.List[str]], typing.List[RegionProperty]]:
    """Decorator to turn a function of appropriate signature into a `PropertyComputation` subclass that generates
    vector properties.
    The function signature is expected to be as follows:
    `<func_name>(PropertyComputation, Photo, List[int], RegionsCache, List[str]) -> List[RegionProperty]`

    `<func_name>` is used as a key of your computation in MAPHIS and will be stored in project files to correctly
    identify the origin of results (segmentations, properties, etc.), so it's good provide clear and easy to interpret
    name for your function.

    Args:
        name: name of the `PropertyComputation`
        description: what kind of vector property this computation computes
        group: category of property, e.g., 'Dimensions', 'Shape',... (see the `Compute new measurements` dialog in MAPHIS)
        export_target (str):

    Returns:
       the decorated function which will be turned into `PropertyComputation` by MAPHIS.
    """
    def wrap(_func: typing.Callable[[Photo, typing.List[int], RegionsCache, typing.List[str]], typing.List[RegionProperty]]):
        _comp_wrapped = _define_property_computation(name, description, group, export_target)(_func)
        prop = RegionProperty()
        prop.value = VectorValue(([0] * value_count) * unit)
        prop.value._column_names = value_names
        prop.label = 0
        prop.prop_comp_key = _comp_wrapped.info.key
        prop.local_key = _func.__name__
        prop.info = _comp_wrapped.info
        _comp_wrapped.example_property = {_func.__name__: prop}
        return _comp_wrapped
    return wrap


def param_int(name: str, description: str, key: str, default_value: int, min_value: int, max_value: int) \
    -> typing.Union[GeneralAction, PropertyComputation, RegionComputation, typing.Callable[[typing.Any], typing.Any]]:
    """ Decorator that adds an integer user parameter to subclasses of `GeneralAction`, `RegionComputation` or
    `PropertyComputation` or functions that have been decorated with `@general_action`, `@region_computation` or
    `@property_computation` decorators.

    Args:
        name (str): name of the parameter - how it will be presented in the GUI
        description (str): what this parameter affects
        key (str): how this parameter will be referenced to in your implementation, but also in project files.
        default_value (int): default value
        min_value (int): the lowest permissible value
        max_value (int): the highest permissible value

    Returns:
        the decorated `Action` or decorated function with the added parameter
    """
    def wrap(_obj: object):
        param = ParamBuilder().int_param().name(name).description(description).key(key) \
            .default_value(default_value).min_value(min_value).max_value(max_value).build()
        if inspect.isfunction(_obj):
            if not hasattr(_obj, 'maphis_params'):
                _obj.maphis_params = {}
            _obj.maphis_params[param.key] = param
        elif inspect.isclass(_obj):
            if not hasattr(_obj, 'default_user_params'):
                _obj.default_user_params = {}
            _obj.default_user_params[param.key] = param
        return _obj
    return wrap


def param_string(name: str, description: str, key: str, default_value: str) \
    -> typing.Union[GeneralAction, PropertyComputation, RegionComputation, typing.Callable[[typing.Any], typing.Any]]:
    """ Decorator that adds a string user parameter to subclasses of `GeneralAction`, `RegionComputation` or
    `PropertyComputation` or functions that have been decorated with `@general_action`, `@region_computation` or
    `@property_computation` decorators.

    Args:
        name: name of the parameter - how it will be presented in the GUI
        description (str): what this parameter affects
        key (str): how this parameter will be referenced to in your implementation, but also in project files.
        default_value (str): default value

    Returns:
        the decorated `Action` or decorated function with the added parameter
    """
    def wrap(_obj: object):
        param = ParamBuilder().string_param().name(name).description(description).key(key) \
            .default_value(default_value).build()
        if inspect.isfunction(_obj):
            if not hasattr(_obj, 'maphis_params'):
                _obj.maphis_params = {}
            _obj.maphis_params[param.key] = param
        elif inspect.isclass(_obj):
            if not hasattr(_obj, 'default_user_params'):
                _obj.default_user_params = {}
            _obj.default_user_params[param.key] = param
        return _obj
    return wrap


def param_bool(name: str, description: str, key: str, default_value: bool) \
    -> typing.Union[GeneralAction, PropertyComputation, RegionComputation, typing.Callable[[typing.Any], typing.Any]]:
    """ Decorator that adds a boolean user parameter to subclasses of `GeneralAction`, `RegionComputation` or
    `PropertyComputation` or functions that have been decorated with `@general_action`, `@region_computation` or
    `@property_computation` decorators.

    Args:
        name: name of the parameter - how it will be presented in the GUI
        description (str): what this parameter affects
        key (str): how this parameter will be referenced to in your implementation, but also in project files.
        default_value (bool): default value

    Returns:
        the decorated `Action` or decorated function with the added parameter
    """
    def wrap(_obj: object):
        param = ParamBuilder().bool_param().name(name).description(description).key(key) \
            .default_value(default_value).build()
        if inspect.isfunction(_obj):
            if not hasattr(_obj, 'maphis_params'):
                _obj.maphis_params = {}
            _obj.maphis_params[param.key] = param
        elif inspect.isclass(_obj):
            if not hasattr(_obj, 'default_user_params'):
                _obj.default_user_params = {}
            _obj.default_user_params[param.key] = param
        return _obj
    return wrap
