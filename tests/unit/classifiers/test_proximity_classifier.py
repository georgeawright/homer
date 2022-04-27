import pytest
from unittest.mock import Mock

from linguoplotter.classifiers import ProximityClassifier
from linguoplotter.structure_collection import StructureCollection


@pytest.mark.parametrize("proximity", [(1.0), (0.0)])
def test_classify_argument(proximity):
    classifier = ProximityClassifier()
    concept = Mock()
    concept.proximity_to.return_value = proximity
    example = Mock()
    assert proximity == classifier.classify(concept=concept, start=example)


@pytest.mark.parametrize("proximity", [(1.0), (0.0)])
def test_classify_item_in_collection(proximity):
    classifier = ProximityClassifier()
    concept = Mock()
    concept.proximity_to.return_value = proximity
    example = Mock()
    collection = StructureCollection(Mock(), [example])
    assert proximity == classifier.classify(concept=concept, collection=collection)
