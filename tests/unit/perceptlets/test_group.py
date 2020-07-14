import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.group import Group


FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_size_flat_group():
    expected_group_size = 30
    members = [Mock() for _ in range(expected_group_size)]
    group = Group(members, Mock())
    assert expected_group_size == group.size


def test_size_recursive_group():
    group_depth = 30
    group = Group([Mock()], Mock())
    for _ in range(group_depth):
        group = Group([group], Mock())
    assert 1 == group.size


@pytest.mark.parametrize(
    "group_size, expected_importance", [(1, 0), (2, 0.5), (10, 0.9), (100, 0.99)]
)
def test_size_based_importance(group_size, expected_importance):
    members = [Mock() for _ in range(group_size)]
    group = Group(members, Mock())
    assert math.isclose(
        expected_importance,
        group._size_based_importance,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    )


@pytest.mark.parametrize(
    "number_of_labels, number_of_groups, number_of_relations, expected_unhappiness",
    [(0, 0, 0, 1.0), (1, 0, 0, 1.0), (1, 1, 1, 0.333), (2, 3, 0, 0.2)],
)
def test_unhappiness(
    number_of_labels, number_of_groups, number_of_relations, expected_unhappiness
):
    group = Group("value", [])
    for i in range(number_of_labels):
        group.add_label(Mock())
    for i in range(number_of_groups):
        group.add_group(Mock())
    for i in range(number_of_relations):
        group.add_relation(Mock())
    assert math.isclose(
        expected_unhappiness, group.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
