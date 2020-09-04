from unittest.mock import Mock, patch

from homer.codelets.group_extender import GroupExtender
from homer.bubbles import Concept, Perceptlet
from homer.bubbles.perceptlets import Group, Label


def test_calculate_confidence():
    distance = 0.5
    expected = 0.5
    with patch.object(Concept, "proximity_between", return_value=distance):
        space = Concept("concept", Mock())
        label_concept = Mock()
        label_concept.space = space
        label_1 = Label(label_concept, Mock(), Mock(), Mock(), Mock())
        label_2 = Label(label_concept, Mock(), Mock(), Mock(), Mock())
        group = Group(Mock(), [0, 1, 2], Mock(), Mock(), Mock(), Mock())
        group.labels.add(label_1)
        candidate = Perceptlet(Mock(), [0, 1, 3], Mock(), Mock(), Mock())
        candidate.labels.add(label_2)
        codelet = GroupExtender(Mock(), Mock(), group, Mock(), Mock())
        codelet.second_target_perceptlet = candidate
        codelet._calculate_confidence()
        assert expected == codelet.confidence


def test_calculate_confidence_with_no_common_concepts():
    expected = 0.0
    group = Group(Mock(), [0, 1, 2], Mock(), Mock(), Mock(), Mock())
    candidate = Perceptlet(Mock(), [0, 1, 3], Mock(), Mock(), Mock())
    codelet = GroupExtender(Mock(), Mock(), group, Mock(), Mock())
    codelet.second_target_perceptlet = candidate
    codelet._calculate_confidence()
    assert expected == codelet.confidence


def test_engender_follow_up(target_perceptlet):
    codelet = GroupExtender(Mock(), Mock(), target_perceptlet, Mock(), Mock())
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupExtender == type(follow_up)
