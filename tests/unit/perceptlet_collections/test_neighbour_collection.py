import math
import pytest
from unittest.mock import Mock

from homer.perceptlet_collections import NeighbourCollection

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_eq():
    assert NeighbourCollection([]) == NeighbourCollection([])
    perceptlet = Mock()
    assert NeighbourCollection([perceptlet]) == NeighbourCollection([perceptlet])
    assert not NeighbourCollection([]) == NeighbourCollection([perceptlet])


def test_ne():
    perceptlet = Mock()
    assert NeighbourCollection([]) != NeighbourCollection([perceptlet])
    assert not NeighbourCollection([]) != NeighbourCollection([])
    assert not NeighbourCollection([perceptlet]) != NeighbourCollection([perceptlet])


def test_copy():
    perceptlets = [Mock(), Mock(), Mock()]
    original_collection = NeighbourCollection(perceptlets)
    new_collection = original_collection.copy()
    assert new_collection.perceptlets == set(perceptlets)
    assert new_collection.perceptlets_list == perceptlets
    assert new_collection == original_collection
    original_collection.add(Mock())
    assert new_collection != original_collection


def test_add():
    collection = NeighbourCollection()
    assert collection.perceptlets == set()
    assert collection.perceptlets_list == []
    perceptlet = Mock()
    collection.add(perceptlet)
    assert collection.perceptlets == {perceptlet}
    assert collection.perceptlets_list == [perceptlet]


def test_remove():
    perceptlet = Mock()
    collection = NeighbourCollection([perceptlet])
    assert collection.perceptlets == {perceptlet}
    assert collection.perceptlets_list == [perceptlet]
    collection.remove(perceptlet)
    assert collection.perceptlets == set()
    assert collection.perceptlets_list == []


def test_union():
    perceptlet_1 = Mock()
    perceptlet_2 = Mock()
    collection_1 = NeighbourCollection([perceptlet_1])
    collection_2 = NeighbourCollection([perceptlet_2])
    union = NeighbourCollection.union(collection_1, collection_2)
    assert union.perceptlets == {perceptlet_1, perceptlet_2}
    assert union.perceptlets_list == [perceptlet_1, perceptlet_2]


def test_intersection():
    with pytest.raises(NotImplementedError):
        NeighbourCollection.intersection(NeighbourCollection(), NeighbourCollection())


def test_get_random():
    perceptlets = [Mock() for _ in range(10)]
    collection = NeighbourCollection(perceptlets)
    random_perceptlet = collection.get_random()
    assert random_perceptlet in perceptlets
