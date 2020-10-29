import pytest
from unittest.mock import Mock

from homer.classifiers import ProximityClassifier


@pytest.mark.parametrize("proximity", [(1.0), (0.0)])
def test_classify(proximity):
    classifier = ProximityClassifier()
    concept = Mock()
    concept.proximity_to.return_value = proximity
    example = Mock()
    assert proximity == classifier.classify(concept, example)
