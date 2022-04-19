import pytest
from unittest.mock import Mock

from linguoplotter.classifiers import DifferentnessClassifier
from linguoplotter.structure_collection import StructureCollection


def test_differentness_of_single_item_in_collection():
    classifier = DifferentnessClassifier()
    item = Mock()
    parent_space = Mock()
    parent_space.is_conceptual_space = False
    conceptual_space = Mock()
    conceptual_space.is_conceptual_space = True
    conceptual_space.is_basic_level = True
    conceptual_space.proximity_between.return_value = 1.0
    item.parent_spaces = StructureCollection(Mock(), [parent_space, conceptual_space])
    collection = StructureCollection(Mock(), [item])
    assert 0.0 == classifier.classify(collection=collection)


@pytest.mark.parametrize("proximity", [(0.0), (0.5), (1.0)])
def test_differentness_of_two_items_in_collection(proximity):
    differentness = 1 - proximity
    classifier = DifferentnessClassifier()

    parent_space = Mock()
    parent_space.is_conceptual_space = False
    conceptual_space = Mock()
    conceptual_space.is_conceptual_space = True
    conceptual_space.is_basic_level = True
    conceptual_space.proximity_between.return_value = proximity

    item_1 = Mock()
    item_1.parent_spaces = StructureCollection(Mock(), [parent_space, conceptual_space])
    item_2 = Mock()
    item_2.parent_spaces = StructureCollection(Mock(), [parent_space, conceptual_space])

    collection = StructureCollection(Mock(), [item_1, item_2])

    assert differentness == classifier.classify(collection=collection)


@pytest.mark.parametrize("proximity", [(0.0), (0.5), (1.0)])
def test_differentness_of_two_arguments(proximity):
    differentness = 1 - proximity
    classifier = DifferentnessClassifier()

    parent_space = Mock()
    parent_space.is_conceptual_space = False
    conceptual_space = Mock()
    conceptual_space.is_conceptual_space = True
    conceptual_space.is_basic_level = True
    conceptual_space.proximity_between.return_value = proximity

    start = Mock()
    start.parent_spaces = StructureCollection(Mock(), [parent_space, conceptual_space])
    end = Mock()
    end.parent_spaces = StructureCollection(Mock(), [parent_space, conceptual_space])

    assert differentness == classifier.classify(
        start=start, end=end, space=conceptual_space
    )
