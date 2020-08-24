import pytest
import statistics
from unittest.mock import Mock

from homer.bubbles.perceptlets import Group
from homer.perceptlet_collection import PerceptletCollection


def test_size_flat_group():
    expected_group_size = 30
    member = Mock()
    member.size = 1
    members = [member for _ in range(expected_group_size)]
    group = Group(Mock(), Mock(), Mock(), members, Mock(), Mock())
    assert expected_group_size == group.size


def test_size_recursive_group():
    group_depth = 30
    member = Mock()
    member.size = 1
    group = Group(Mock(), Mock(), Mock(), {member}, Mock(), Mock())
    for _ in range(group_depth):
        group = Group(Mock(), Mock(), Mock(), [group], Mock(), Mock())
    assert 1 == group.size


@pytest.mark.parametrize("no_of_members", [(10)])
def test_get_random_member_returns_member(no_of_members):
    members = PerceptletCollection({Mock() for _ in range(no_of_members)})
    group = Group(Mock(), Mock(), Mock(), members, Mock(), Mock())
    assert group.members.get_random() in members


@pytest.mark.parametrize("original_value, member_values", [(1, [2, 3, 4, 0])])
def test_add_member_maintains_average(original_value, member_values):
    original_member = Mock()
    original_member.value = [original_value]
    original_member.size = 1
    group = Group(
        [original_value],
        Mock(),
        PerceptletCollection(),
        PerceptletCollection({original_member}),
        Mock(),
        Mock(),
    )
    for member_value in member_values:
        new_member = Mock()
        new_member.value = [member_value]
        new_member.size = 1
        new_member.neighbours = PerceptletCollection()
        group.add_member(new_member)
    assert [statistics.fmean(member_values + [original_value])] == group.value
