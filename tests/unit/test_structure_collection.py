import math
import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection


def test_union():
    structure_1 = Mock()
    structure_2 = Mock()
    collection_1 = StructureCollection(Mock(), [structure_1])
    collection_2 = StructureCollection(Mock(), [structure_2])
    union = StructureCollection.union(collection_1, collection_2)
    assert union.structures == {structure_1: True, structure_2: True}


def test_intersection():
    structure_1 = Mock()
    structure_2 = Mock()
    structure_3 = Mock()
    collection_1 = StructureCollection(Mock(), [structure_1, structure_2])
    collection_2 = StructureCollection(Mock(), [structure_2, structure_3])
    intersection = StructureCollection.intersection(collection_1, collection_2)
    assert intersection.structures == {structure_2: True}


def test_difference():
    structure_1 = Mock()
    structure_2 = Mock()
    structure_3 = Mock()
    collection_1 = StructureCollection(Mock(), [structure_1, structure_2])
    collection_2 = StructureCollection(Mock(), [structure_2, structure_3])
    difference = StructureCollection.difference(collection_1, collection_2)
    assert difference.structures == {structure_1: True}


def test_eq_and_ne():
    structure_1 = Mock()
    structure_2 = Mock()
    collection_a = StructureCollection(Mock(), [])
    collection_b = StructureCollection(Mock(), [])
    collection_c = StructureCollection(Mock(), [structure_1])
    collection_d = StructureCollection(Mock(), [structure_1])
    collection_e = StructureCollection(Mock(), [structure_2])
    collection_f = StructureCollection(Mock(), [structure_1, structure_2])
    collection_g = StructureCollection(Mock(), [structure_2, structure_1])

    assert collection_a == collection_b
    assert collection_c == collection_d
    assert collection_f == collection_g

    assert not collection_a == collection_c
    assert not collection_a == collection_f
    assert not collection_c == collection_e
    assert not collection_c == collection_f

    assert collection_a != collection_c
    assert collection_a != collection_f
    assert collection_c != collection_e
    assert collection_c != collection_f

    assert not collection_a != collection_b
    assert not collection_c != collection_d
    assert not collection_f != collection_g


def test_get_item():
    structure_1 = Mock()
    structure_2 = Mock()
    structure_2.name = "structure"
    collection = StructureCollection(Mock(), [structure_1, structure_2])
    assert structure_2 == collection["structure"]


def test_copy():
    structures = [Mock(), Mock(), Mock()]
    original_collection = StructureCollection(Mock(), structures)
    new_collection = original_collection.copy()
    for structure in structures:
        assert structure in original_collection
        assert structure in new_collection
    assert new_collection == original_collection
    original_collection.add(Mock())
    assert new_collection != original_collection


def test_is_empty():
    collection = StructureCollection(Mock(), [])
    assert collection.is_empty()
    collection.add(Mock())
    assert not collection.is_empty()


def test_add():
    collection = StructureCollection(Mock(), [])
    assert collection.structures == {}
    structure = Mock()
    collection.add(structure)
    assert collection.structures == {structure: True}


def test_remove():
    structure = Mock()
    collection = StructureCollection(Mock(), [structure])
    assert collection.structures == {structure: True}
    collection.remove(structure)
    assert collection.structures == {}


def test_of_type():
    class A:
        pass

    class B:
        pass

    structure_1 = A()
    structure_2 = B()
    collection = StructureCollection(Mock(), [structure_1, structure_2])
    assert StructureCollection(Mock(), [structure_1]) == collection.of_type(A)
    assert StructureCollection(Mock(), [structure_2]) == collection.of_type(B)
