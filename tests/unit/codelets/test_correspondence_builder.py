import pytest
from unittest.mock import Mock, patch

from homer.concept import Concept
from homer.codelets.correspondence_builder import CorrespondenceBuilder
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.perceptlets.group import Group


@pytest.mark.parametrize(
    "both_have_labels_in_space, proximity, number_of_common_labels, expected",
    [(True, 1.0, 1, 1.0), (False, 1.0, 0, 0.0), (True, 0.5, 1, 0.5)],
)
def test_calculate_confidence(
    both_have_labels_in_space, proximity, number_of_common_labels, expected
):
    set_of_common_labels = {Mock() for _ in range(number_of_common_labels)}
    with patch.object(
        Group, "has_label_in_space", return_value=both_have_labels_in_space
    ), patch.object(
        Group, "labels_in_space", return_value=set_of_common_labels
    ), patch.object(
        Concept, "proximity_between", return_value=proximity
    ):
        target_group_a = Group(Mock(), Mock(), Mock(), Mock(), Mock())
        target_group_b = Group(Mock(), Mock(), Mock(), Mock(), Mock())
        parent_space = Concept(Mock(), Mock())
        correspondence_builder = CorrespondenceBuilder(
            Mock(), Mock(), parent_space, target_group_a, target_group_b, Mock()
        )
        assert expected == correspondence_builder._calculate_confidence()


def test_engender_follow_up():
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    follow_up = correspondence_builder._engender_follow_up(Mock(), Mock())
    assert CorrespondenceLabeler == type(follow_up)
