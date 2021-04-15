import pytest
from unittest.mock import Mock

from homer.classifiers import DifferenceClassifier


@pytest.mark.parametrize(
    "start_value, end_value, expected", [([[10]], [[5]], 1), ([[5]], [[10]], 0)]
)
def test_classify(start_value, end_value, expected):
    scalar_classifier = Mock()
    scalar_classifier.classify = lambda **x: 1 if x["start"].value[0][0] > 0 else 0
    classifier = DifferenceClassifier(scalar_classifier)
    start = Mock()
    start.value = start_value
    end = Mock()
    end.value = end_value
    space = Mock()
    space.parent_concept.relevant_value = "value"
    assert expected == classifier.classify(start=start, end=end, space=space)
