import pytest
from unittest.mock import Mock, patch

from homer.bubbles import Concept
from homer.bubbles.perceptlets import Group
from homer.classifiers import CorrespondenceClassifier
from homer.perceptlet_collection import PerceptletCollection


@pytest.mark.parametrize(
    "both_have_labels_in_space, proximity, number_of_common_labels, expected",
    [(True, 1.0, 1, 1.0), (False, 1.0, 0, 1.0), (True, 0.5, 1, 0.5)],
)
def test_calculate_confidence(
    both_have_labels_in_space, proximity, number_of_common_labels, expected
):
    set_of_common_labels = PerceptletCollection(
        {Mock() for _ in range(number_of_common_labels)}
    )
    with patch.object(
        Group, "has_label_in_space", return_value=both_have_labels_in_space
    ), patch.object(
        Group, "labels_in_space", return_value=set_of_common_labels
    ), patch.object(
        Concept, "proximity_between", return_value=proximity
    ):
        target_group_a = Group(Mock(), [0, 0, 0], Mock(), Mock(), Mock(), Mock())
        target_group_b = Group(Mock(), [1, 1, 1], Mock(), Mock(), Mock(), Mock())
        parent_space = Concept("concept", Mock())
        classifier = CorrespondenceClassifier()
        confidence = classifier.confidence(target_group_a, target_group_b, parent_space)
        assert expected == confidence
