from unittest.mock import Mock, patch

from homer.codelets.group_builder import GroupBuilder
from homer.codelets.group_extender import GroupExtender
from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlets.label import Label

FLOAT_COMPARISON_TOLERANCE = 1e-1


def test_calculate_confidence():
    distance = 0.5
    expected = 0.5
    with patch.object(Concept, "proximity_between", return_value=distance):
        common_concept = Concept(Mock(), Mock())
        label_1 = Label(common_concept, Mock(), Mock(), Mock())
        label_2 = Label(common_concept, Mock(), Mock(), Mock())
        perceptlet_1 = Perceptlet(Mock(), Mock(), Mock(), Mock())
        perceptlet_1.add_label(label_1)
        perceptlet_2 = Perceptlet(Mock(), Mock(), Mock(), Mock())
        perceptlet_2.add_label(label_2)
        codelet = GroupBuilder(Mock(), Mock(), Mock(), Mock())
        confidence = codelet._calculate_confidence(perceptlet_1, perceptlet_2)
        assert expected == confidence


def test_calculate_confidence_with_no_common_concepts():
    expected = 0.0
    perceptlet_1 = Perceptlet(Mock(), Mock(), Mock(), Mock())
    perceptlet_2 = Perceptlet(Mock(), Mock(), Mock(), Mock())
    codelet = GroupBuilder(Mock(), Mock(), Mock(), Mock())
    confidence = codelet._calculate_confidence(perceptlet_1, perceptlet_2)
    assert expected == confidence


def test_engender_follow_up():
    codelet = GroupBuilder(Mock(), Mock(), Mock(), Mock())
    follow_up = codelet.engender_follow_up(Mock(), Mock())
    assert GroupExtender == type(follow_up)
