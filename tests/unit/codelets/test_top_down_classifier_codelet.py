import math
import pytest
from unittest.mock import Mock

from homer.codelets.top_down_classifier_codelet import TopDownClassifierCodelet

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "concept_activation, concept_depth, distance_from_prototype, "
    + "proportion_of_neighbours, expected",
    [
        (1.0, 0.1, 0.0, 1.0, 1.0),
        (0.0, 0.1, 0.0, 1.0, 1.0),
        (1.0, 1.0, 0.0, 1.0, 1.0),
        (1.0, 0.1, 1.0, 1.0, 1.0),
        (1.0, 0.1, 0.0, 0.0, 1.0),
        (0.5, 0.5, 0.5, 0.5, 0.5),
        (1.0, 1.0, 1.0, 0.0, 0.0),
        (0.0, 0.1, 1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 1.0, 1.0, 0.0),
        (0.0, 1.0, 1.0, 0.0, 0.0),
    ],
)
def test_calculate_confidence(
    concept_activation,
    concept_depth,
    distance_from_prototype,
    proportion_of_neighbours,
    expected,
):
    codelet = TopDownClassifierCodelet(Mock(), Mock(), Mock(), Mock())
    result = codelet._calculate_confidence(
        concept_activation,
        concept_depth,
        distance_from_prototype,
        proportion_of_neighbours,
    )
    assert math.isclose(expected, result, abs_tol=FLOAT_COMPARISON_TOLERANCE)


def test_engender_follow_up():
    codelet = TopDownClassifierCodelet(Mock(), Mock(), Mock(), Mock())
    follow_up = codelet.engender_follow_up(Mock())
    assert TopDownClassifierCodelet == type(follow_up)
