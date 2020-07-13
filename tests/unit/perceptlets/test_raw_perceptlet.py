import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.raw_perceptlet import RawPerceptlet


FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "label_strengths, expected_importance",
    [
        ([], 0),
        ([0.2, 0.3], 0.333),
        ([0.7, 0.8], 0.6),
        ([1, 1], 0.667),
        ([1, 1, 1, 1], 0.8),
    ],
)
def test_importance(label_strengths, expected_importance):
    perceptlet = RawPerceptlet("value", [])
    for label_strength in label_strengths:
        label = Mock()
        label.strength = label_strength
        perceptlet.add_label(label)
    assert math.isclose(
        expected_importance, perceptlet.importance, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "number_of_labels, number_of_groups, number_of_relations, expected_unhappiness",
    [(0, 0, 0, 1.0), (1, 0, 0, 1.0), (1, 1, 1, 0.333), (2, 3, 0, 0.2)],
)
def test_unhappiness(
    number_of_labels, number_of_groups, number_of_relations, expected_unhappiness
):
    perceptlet = RawPerceptlet("value", [])
    for i in range(number_of_labels):
        perceptlet.add_label(Mock())
    for i in range(number_of_groups):
        perceptlet.add_group(Mock())
    for i in range(number_of_relations):
        perceptlet.add_relation(Mock())
    assert math.isclose(
        expected_unhappiness, perceptlet.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
