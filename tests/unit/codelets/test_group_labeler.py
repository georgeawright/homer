import math
import pytest
from unittest.mock import Mock

from homer.codelets import GroupExtender, GroupLabeler

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "label_strengths, group_size, expected",
    [([0.5, 0.5], 2, 0.5), ([0.5, 0.5], 4, 0.25)],
)
def test_calculate_confidence(label_strengths, group_size, expected):
    concept = Mock()
    group = Mock()
    group.size = group_size
    group.members = set()
    for label_strength in label_strengths:
        label = Mock()
        label.parent_concept = concept
        label.strength = label_strength
        member = Mock()
        member.labels = {label}
        group.members.add(member)
    codelet = GroupLabeler(Mock(), Mock(), group, Mock(), Mock())
    codelet.parent_concept = concept
    codelet._calculate_confidence()
    assert math.isclose(
        expected, codelet.confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_engender_follow_up():
    codelet = GroupLabeler(Mock(), Mock(), Mock(), Mock(), Mock())
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupExtender == type(follow_up)


def test_engender_alternative_follow_up():
    codelet = GroupLabeler(Mock(), Mock(), Mock(), 1, Mock())
    follow_up = codelet._engender_alternative_follow_up()
    assert GroupLabeler == type(follow_up)
