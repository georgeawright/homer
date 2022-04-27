import pytest
from unittest.mock import Mock

from linguoplotter.structure_collection import StructureCollection


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
    collection_3 = StructureCollection(Mock(), [structure_1])
    collection_4 = StructureCollection(Mock(), [structure_3])
    collection_5 = StructureCollection(Mock(), [structure_1, structure_2, structure_2])

    intersection = StructureCollection.intersection(collection_1, collection_2)
    assert intersection.structures == {structure_2: True}

    intersection = StructureCollection.intersection(collection_3, collection_4)
    assert intersection.structures == {}

    intersection = StructureCollection.intersection(collection_1, collection_3)
    assert intersection.structures == {structure_1: True}

    intersection = StructureCollection.intersection(
        collection_1, collection_2, collection_3
    )
    assert intersection.structures == {}

    intersection = StructureCollection.intersection(
        collection_1, collection_2, collection_5
    )
    assert intersection.structures == {structure_2: True}

    intersection = StructureCollection.intersection(
        collection_1, collection_2, collection_3, collection_4, collection_5
    )
    assert intersection.structures == {}


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


def test_filter():
    structure_1 = Mock()
    structure_1.has_label.return_value = True
    structure_2 = Mock()
    structure_2.has_label.return_value = False
    collection = StructureCollection(Mock(), [structure_1, structure_2])
    assert StructureCollection(Mock(), [structure_1]) == collection.filter(
        lambda x: x.has_label(Mock())
    )


def test_at():
    structure_1 = Mock()
    structure_1.location.coordinates = [[0, 0], [0, 1]]
    structure_2 = Mock()
    structure_2.location.coordinates = [[0, 1], [1, 1]]

    collection = StructureCollection(Mock(), [structure_1, structure_2])

    location_0_0 = Mock()
    location_0_0.coordinates = [[0, 0]]
    location_0_0_0_1 = Mock()
    location_0_0_0_1.coordinates = [[0, 0], [0, 1]]
    location_0_1 = Mock()
    location_0_1.coordinates = [[0, 1]]
    location_1_1 = Mock()
    location_1_1.coordinates = [[1, 1]]

    assert StructureCollection(Mock(), [structure_1]) == collection.at(location_0_0)
    assert StructureCollection(Mock(), [structure_1, structure_2]) == collection.at(
        location_0_0_0_1
    )
    assert StructureCollection(Mock(), [structure_1, structure_2]) == collection.at(
        location_0_1
    )
    assert StructureCollection(Mock(), [structure_2]) == collection.at(location_1_1)


def test_next_to():
    structure_1 = Mock()
    structure_1.location.coordinates = [[0]]
    structure_2 = Mock()
    structure_2.location.coordinates = [[1]]
    structure_3 = Mock()
    structure_3.location.coordinates = [[2]]
    structure_4 = Mock()
    structure_4.location.coordinates = [[0], [1]]

    collection = StructureCollection(
        Mock(), [structure_1, structure_2, structure_3, structure_4]
    )

    assert StructureCollection(Mock(), [structure_2]) == collection.next_to(
        structure_1.location
    )
    assert StructureCollection(
        Mock(), [structure_1, structure_3]
    ) == collection.next_to(structure_2.location)
    assert StructureCollection(
        Mock(), [structure_2, structure_4]
    ) == collection.next_to(structure_3.location)


def test_is_near():
    location_1 = Mock()
    location_1.is_near.return_value = True
    structure_1 = Mock()
    structure_1.location_in_space.return_value = location_1

    location_2 = Mock()
    location_2.is_near.return_value = False
    structure_2 = Mock()
    structure_2.location_in_space.return_value = location_2

    collection = StructureCollection(Mock(), [structure_1, structure_2])

    assert StructureCollection(Mock(), [structure_1]) == collection.near(Mock())


def test_where():
    structure_1 = Mock()
    structure_1.attribute = True
    structure_2 = Mock()
    structure_2.attribute = False
    collection = StructureCollection(Mock(), [structure_1, structure_2])
    assert StructureCollection(Mock(), [structure_1]) == collection.where(
        attribute=True
    )
    assert StructureCollection(Mock(), [structure_2]) == collection.where(
        attribute=False
    )


def test_where_not():
    structure_1 = Mock()
    structure_1.attribute = Mock()
    structure_2 = Mock()
    structure_2.attribute = None
    collection = StructureCollection(Mock(), [structure_1, structure_2])
    assert StructureCollection(Mock(), [structure_1]) == collection.where_not(
        attribute=None
    )


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
