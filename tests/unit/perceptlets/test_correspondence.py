import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.correspondence import Correspondence

FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "number_of_correspondences, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness(number_of_correspondences, expected_unhappiness):
    correspondence = Correspondence("value", Mock(), Mock(), Mock(), Mock(), Mock())
    for i in range(number_of_correspondences):
        correspondence.add_correspondence(Mock())
    assert math.isclose(
        expected_unhappiness,
        correspondence.unhappiness,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    )


def test_is_between():
    first = Mock()
    second = Mock()
    third = Mock()
    correspondence = Correspondence(Mock(), Mock(), first, second, Mock(), Mock())
    assert correspondence.is_between(first, second)
    assert correspondence.is_between(second, first)
    assert not correspondence.is_between(first, third)
    assert not correspondence.is_between(third, second)
