import math
import pytest
from unittest.mock import Mock

from homer.codelets.group_labeler import GroupLabeler
from homer.codelets.group_extender import GroupExtender

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.skip
@pytest.mark.parametrize(
    "label_strengths, members_without_label, expected",
    [([0.5, 0.5], 0, 0.5), ([0.5, 0.5], 2, 0.25)],
)
def test_calculate_confidence(label_strengths, members_without_label, expected):
    concept = Mock()
    group = Mock()
    group.members = set()
    for label_strength in label_strengths:
        label = Mock()
        label.parent_concept = concept
        label.strength = label_strength
        member = Mock()
        member.labels = {label}
        group.members.add(member)
    for i in range(members_without_label):
        member = Mock()
        member.labels = set()
        group.members.add(member)
    codelet = GroupLabeler(Mock(), concept, group, Mock())
    confidence = codelet._calculate_confidence()
    assert math.isclose(expected, confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE)


def test_engender_follow_up():
    codelet = GroupLabeler(Mock(), Mock(), Mock(), Mock())
    follow_up = codelet.engender_follow_up(Mock())
    assert GroupExtender == type(follow_up)
