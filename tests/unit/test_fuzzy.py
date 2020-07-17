import math
import pytest

from homer import fuzzy

FLOATING_POINT_TOLERANCE = 1e-5


@pytest.mark.parametrize(
    "a, expected", [(1.0, 0.0), (0.0, 1.0), (0.2, 0.8), (0.8, 0.2), (0.5, 0.5)]
)
def test_not(a, expected):
    result = fuzzy.NOT(a)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0), (0.5, 0.5, 0.25)]
)
def test_binary_and(a, b, expected):
    result = fuzzy._AND(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "args, expected",
    [
        ([1.0, 1.0, 1.0, 1.0], 1.0),
        ([0.0, 0.0, 0.0, 0.0], 0.0),
        ([0.5, 0.5, 0.5, 0.5], 0.0625),
    ],
)
def test_nary_and(args, expected):
    result = fuzzy.AND(*args)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0), (0.5, 0.5, 0.75)]
)
def test_binary_or(a, b, expected):
    result = fuzzy._OR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "args, expected",
    [
        ([1.0, 1.0, 1.0, 1.0], 1.0),
        ([0.0, 0.0, 0.0, 0.0], 0.0),
        ([0.5, 0.5, 0.5, 0.5], 0.9375),
    ],
)
def test_nary_or(args, expected):
    result = fuzzy.OR(*args)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.75)]
)
def test_binary_nand(a, b, expected):
    result = fuzzy._NAND(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.25)]
)
def test_binary_nor(a, b, expected):
    result = fuzzy._NOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (0.5, 0.5, 0.5625)]
)
def test_binary_xor(a, b, expected):
    result = fuzzy._XOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "args, expected",
    [
        ([1.0, 1.0, 1.0, 1.0], 0.0),
        ([0.0, 0.0, 0.0, 0.0], 0.0),
        ([0.5, 0.5, 0.5, 0.5], 0.56156),
    ],
)
def test_nary_xor(args, expected):
    result = fuzzy.XOR(*args)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 1.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.4375)]
)
def test_binary_xnor(a, b, expected):
    result = fuzzy._XNOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)
