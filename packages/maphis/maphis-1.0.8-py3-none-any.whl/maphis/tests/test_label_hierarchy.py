import pytest

from maphis.common.label_hierarchy import HierarchyLevel


def get_bit_mask_str(nbits: int, bit_count: int, bit_start: int) -> str:
    return '0' * (nbits - (bit_start + bit_count)) + '1' * bit_count + '0' * bit_start


@pytest.mark.parametrize(["n_bits", "bit_count", "bit_start"], [(32, 4, 12), (32, 8, 0), (32, 8, 24)])
def test_level_mask(n_bits: int, bit_count: int, bit_start: int):
    """
    Test whether the `__init__` function of `HierarchyLevel` generates a correct
    `bit_mask` given the `bit_count` and `bit_start` parameters.
    """
    mask_str = get_bit_mask_str(n_bits, bit_count, bit_start)

    level = HierarchyLevel('a', bit_count, bit_start, n_bits=n_bits)

    assert level.bit_mask == int(mask_str, base=2)
