import pytest

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero


@pytest.mark.parametrize(
    "raw_float, equivalent_float_value",
    [(0.5, 0.5), (0.0, 0.0), (1.0, 1.0), (-0.1, 0.0), (1.1, 1.0)],
)
def test_constructor(raw_float, equivalent_float_value):
    assert FloatBetweenOneAndZero(raw_float) == equivalent_float_value
