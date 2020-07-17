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
def test_and(a, b, expected):
    result = fuzzy.AND(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0), (0.5, 0.5, 0.75)]
)
def test_or(a, b, expected):
    result = fuzzy.OR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.75)]
)
def test_nand(a, b, expected):
    result = fuzzy.NAND(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.25)]
)
def test_nor(a, b, expected):
    result = fuzzy.NOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (0.5, 0.5, 0.5625)]
)
def test_xor(a, b, expected):
    result = fuzzy.XOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)


@pytest.mark.parametrize(
    "a, b, expected", [(1.0, 1.0, 1.0), (0.0, 0.0, 1.0), (0.5, 0.5, 0.4375)]
)
def test_xnor(a, b, expected):
    result = fuzzy.XNOR(a, b)
    assert math.isclose(expected, result, abs_tol=FLOATING_POINT_TOLERANCE)
