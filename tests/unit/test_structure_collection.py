import math
import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_eq():
    assert StructureCollection(set()) == StructureCollection(set())
    structure = Mock()
    assert StructureCollection({structure}) == StructureCollection({structure})
    assert not StructureCollection(set()) == StructureCollection({structure})


def test_ne():
    structure = Mock()
    assert StructureCollection(set()) != StructureCollection({structure})
    assert not StructureCollection(set()) != StructureCollection(set())
    assert not StructureCollection({structure}) != StructureCollection({structure})


def test_copy():
    structures = {Mock(), Mock(), Mock()}
    original_collection = StructureCollection(structures)
    new_collection = original_collection.copy()
    assert new_collection.structures == structures
    assert new_collection == original_collection
    original_collection.add(Mock())
    assert new_collection != original_collection


def test_add():
    collection = StructureCollection(set())
    assert collection.structures == set()
    structure = Mock()
    collection.add(structure)
    assert collection.structures == {structure}


def test_remove():
    structure = Mock()
    collection = StructureCollection({structure})
    assert collection.structures == {structure}
    collection.remove(structure)
    assert collection.structures == set()


def test_union():
    structure_1 = Mock()
    structure_2 = Mock()
    collection_1 = StructureCollection({structure_1})
    collection_2 = StructureCollection({structure_2})
    union = StructureCollection.union(collection_1, collection_2)
    assert union.structures == {structure_1, structure_2}


def test_intersection():
    structure_1 = Mock()
    structure_2 = Mock()
    structure_3 = Mock()
    collection_1 = StructureCollection({structure_1, structure_2})
    collection_2 = StructureCollection({structure_2, structure_3})
    intersection = StructureCollection.intersection(collection_1, collection_2)
    assert intersection.structures == {structure_2}


def test_difference():
    structure_1 = Mock()
    structure_2 = Mock()
    structure_3 = Mock()
    collection_1 = StructureCollection({structure_1, structure_2})
    collection_2 = StructureCollection({structure_2, structure_3})
    difference = StructureCollection.difference(collection_1, collection_2)
    assert difference.structures == {structure_1}


@pytest.mark.parametrize(
    "no_of_valid_members, no_of_invalid_members, expected_proportion",
    [(1, 1, 0.5), (1, 2, 0.33333), (0, 1, 0.0)],
)
def test_number_and_proportion_with_label(
    no_of_valid_members,
    no_of_invalid_members,
    expected_proportion,
):
    concept = Mock()
    valid_members = set()
    for _ in range(no_of_valid_members):
        member = Mock()
        member.has_label.side_effect = [True]
        valid_members.add(member)
    invalid_members = set()
    for _ in range(no_of_invalid_members):
        member = Mock()
        member.has_label.side_effect = [False]
        invalid_members.add(member)
    collection = StructureCollection(set.union(valid_members, invalid_members))
    actual_proportion = collection.proportion_with_label(concept)
    assert math.isclose(
        expected_proportion, actual_proportion, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_get_random():
    structures = {Mock() for _ in range(10)}
    collection = StructureCollection(structures)
    random_structure = collection.get_random()
    assert random_structure in structures


def test_get_random_with_exclude():
    structure_1 = Mock()
    structure_2 = Mock()
    collection = StructureCollection({structure_1, structure_2})
    assert structure_2 == collection.get_random(exclude=[structure_1])
