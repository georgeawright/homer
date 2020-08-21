import math
import pytest
from unittest.mock import Mock, patch

from homer.bubbles import Concept, Perceptlet
from homer.codelets import RawPerceptletLabeler

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "proximity_to_prototype, proportion_of_neighbours, expected",
    [
        (0.0, 1.0, 1.0),
        (1.0, 1.0, 1.0),
        (0.0, 0.0, 0.0),
        (0.5, 0.5, 0.75),
        (1.0, 0.0, 1.0),
    ],
)
def test_calculate_confidence(
    proximity_to_prototype, proportion_of_neighbours, expected,
):
    with patch.object(
        Concept, "proximity_to", return_value=proximity_to_prototype
    ), patch.object(
        Perceptlet,
        "proportion_of_neighbours_with_label",
        return_value=proportion_of_neighbours,
    ), patch.object(
        Perceptlet, "get_value", return_value=Mock()
    ):
        parent_concept = Concept("concept_name", Mock())
        target_perceptlet = Perceptlet(Mock(), Mock(), Mock(), Mock(), Mock())
        codelet = RawPerceptletLabeler(
            Mock(), Mock(), parent_concept, target_perceptlet, Mock(), Mock()
        )
        codelet._calculate_confidence()
    assert math.isclose(
        expected, codelet.confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_engender_follow_up():
    codelet = RawPerceptletLabeler(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert RawPerceptletLabeler == type(follow_up)
