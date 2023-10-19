import pytest
from pint import UnitRegistry

from maphis.common.units import CompoundUnit, UnitStore, Unit


@pytest.fixture
def ustore() -> UnitStore:
    return UnitStore()


@pytest.fixture
def ureg() -> UnitRegistry:
    ureg = UnitRegistry()
    ureg.default_format = '~P'
    return ureg


@pytest.fixture
def pixel(ustore: UnitStore) -> Unit:
    return ustore.units['pixel']


@pytest.fixture
def pixel_squared(pixel: Unit) -> Unit:
    return pixel * pixel


@pytest.fixture
def px_per_mm(ustore: UnitStore) -> CompoundUnit:
    return ustore.units['pixel'] / ustore.units['mm']


@pytest.fixture
def one_per_mm(ustore: UnitStore) -> CompoundUnit:
    return CompoundUnit(set(), ustore.units['mm'])


def test_pint_unit_from_legacy_unit1(px_per_mm: CompoundUnit, ureg: UnitRegistry):
    pint_unit = ureg('pixel/mm')

    from_legacy = ureg(str(px_per_mm))

    assert from_legacy == pint_unit


def test_pint_unit_from_legacy_unit2(one_per_mm: CompoundUnit, pixel_squared: Unit, ureg: UnitRegistry):
    pint_unit = 1 / ureg('mm')

    from_legacy = ureg(str(one_per_mm))

    assert from_legacy == pint_unit

    pint_px_squared = ureg('pixel ** 2')
    from_legacy = ureg(str(pixel_squared))

    assert from_legacy == pint_px_squared