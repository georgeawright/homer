import pytest
from unittest.mock import Mock

from homer.classifiers import DifferenceClassifier


@pytest.mark.parametrize(
    "start_value, end_value, prototype_difference, expected",
    [
        ([[10]], [[5]], 5, 1),
        ([[5]], [[10]], 5, 0),
        ([[10]], [[5]], -5, 0),
        ([[5]], [[10]], -5, 1),
        ([[10]], [[10]], 0, 1),
        ([[10]], [[5]], 0, 0),
        ([[5]], [[10]], 0, 0),
    ],
)
def test_classify_link(start_value, end_value, prototype_difference, expected):
    classifier = DifferenceClassifier(prototype_difference)
    start = Mock()
    start_location = Mock()
    start_location.coordinates = start_value
    start.location_in_space.return_value = start_location
    end = Mock()
    end_location = Mock()
    end_location.coordinates = end_value
    end.location_in_space.return_value = end_location
    space = Mock()
    space.parent_concept.relevant_value = "value"
    assert expected == classifier.classify_link(start=start, end=end, space=space)
