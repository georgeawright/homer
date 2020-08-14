from unittest.mock import Mock, patch

from homer.codelets.group_builder import GroupBuilder
from homer.codelets.group_labeler import GroupLabeler
from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlets.label import Label

FLOAT_COMPARISON_TOLERANCE = 1e-1


def test_calculate_confidence():
    distance = 0.5
    expected = 0.5
    with patch.object(Concept, "proximity_between", return_value=distance):
        common_concept = Concept("concept", Mock())
        common_concept.relevant_value = "value"
        label_1 = Label(common_concept, Mock(), Mock(), Mock())
        label_2 = Label(common_concept, Mock(), Mock(), Mock())
        perceptlet_1 = Perceptlet(Mock(), [0, 1, 2], Mock(), Mock())
        perceptlet_1.labels.add(label_1)
        perceptlet_2 = Perceptlet(Mock(), [0, 1, 3], Mock(), Mock())
        perceptlet_2.labels.add(label_2)
        codelet = GroupBuilder(Mock(), Mock(), perceptlet_1, Mock(), Mock())
        codelet.second_target_perceptlet = perceptlet_2
        codelet._calculate_confidence()
        assert expected == codelet.confidence


def test_calculate_confidence_with_no_common_concepts():
    expected = 0.0
    perceptlet_1 = Perceptlet(Mock(), Mock(), Mock(), Mock())
    perceptlet_2 = Perceptlet(Mock(), Mock(), Mock(), Mock())
    codelet = GroupBuilder(Mock(), Mock(), perceptlet_1, Mock(), Mock())
    codelet.second_target_perceptlet = perceptlet_2
    codelet._calculate_confidence()
    assert expected == codelet.confidence


def test_engender_follow_up():
    codelet = GroupBuilder(Mock(), Mock(), Mock(), Mock(), Mock())
    codelet.group = Mock()
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupLabeler == type(follow_up)
