import math
import pytest
from unittest.mock import Mock

from homer.codelets.top_down_classifier_codelet import TopDownClassifierCodelet

FLOAT_COMPARISON_TOLERANCE = 1e-5


@pytest.mark.parametrize(
    "activation,depth,distance,proportion_of_neighbours,weights,expected",
    [(1.0, 1, 0, 1.0, [0.5, -0.1, -0.1, 0.5], 0.9)],
)
def test_calculate_confidence(
    activation, depth, distance, proportion_of_neighbours, weights, expected,
):
    codelet = TopDownClassifierCodelet(Mock(), Mock(), Mock(), weights, Mock())
    inputs = [activation, depth, distance, proportion_of_neighbours]
    result = codelet.calculate_confidence(inputs)
    assert math.isclose(expected, result, abs_tol=FLOAT_COMPARISON_TOLERANCE)


def test_engender_follow_up():
    codelet = TopDownClassifierCodelet(Mock(), Mock(), Mock(), Mock(), Mock())
    follow_up = codelet.engender_follow_up(Mock())
    assert TopDownClassifierCodelet == type(follow_up)
