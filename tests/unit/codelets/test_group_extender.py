from unittest.mock import Mock, patch

from homer.codelets.group_extender import GroupExtender
from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlets.group import Group
from homer.perceptlets.label import Label


def test_calculate_confidence():
    distance = 0.5
    expected = 0.5
    with patch.object(Concept, "proximity_between", return_value=distance):
        common_concept = Concept(Mock(), Mock())
        label_1 = Label(common_concept, Mock(), Mock())
        label_2 = Label(common_concept, Mock(), Mock())
        group = Group(Mock(), [0, 1, 2], Mock(), Mock(), Mock())
        group.add_label(label_1)
        candidate = Perceptlet(Mock(), [0, 1, 3], Mock())
        candidate.add_label(label_2)
        codelet = GroupExtender(Mock(), group, Mock())
        confidence = codelet._calculate_confidence(candidate)
        assert expected == confidence


def test_calculate_confidence_with_no_common_concepts():
    expected = 0.0
    group = Group(Mock(), [0, 1, 2], Mock(), Mock(), Mock())
    candidate = Perceptlet(Mock(), [0, 1, 3], Mock())
    codelet = GroupExtender(Mock(), group, Mock())
    confidence = codelet._calculate_confidence(candidate)
    assert expected == confidence


def test_engender_follow_up():
    codelet = GroupExtender(Mock(), Mock(), Mock())
    follow_up = codelet.engender_follow_up(Mock())
    assert GroupExtender == type(follow_up)
