import math
import pytest
from unittest.mock import Mock

from homer.perceptlet_collection import PerceptletCollection

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_eq():
    assert PerceptletCollection(set()) == PerceptletCollection(set())
    perceptlet = Mock()
    assert PerceptletCollection({perceptlet}) == PerceptletCollection({perceptlet})
    assert not PerceptletCollection(set()) == PerceptletCollection({perceptlet})


def test_ne():
    perceptlet = Mock()
    assert PerceptletCollection(set()) != PerceptletCollection({perceptlet})
    assert not PerceptletCollection(set()) != PerceptletCollection(set())
    assert not PerceptletCollection({perceptlet}) != PerceptletCollection({perceptlet})


def test_copy():
    perceptlets = {Mock(), Mock(), Mock()}
    original_collection = PerceptletCollection(perceptlets)
    new_collection = original_collection.copy()
    assert new_collection.perceptlets == perceptlets
    assert new_collection == original_collection
    original_collection.add(Mock())
    assert new_collection != original_collection


def test_add():
    collection = PerceptletCollection(set())
    assert collection.perceptlets == set()
    perceptlet = Mock()
    collection.add(perceptlet)
    assert collection.perceptlets == {perceptlet}


def test_remove():
    perceptlet = Mock()
    collection = PerceptletCollection({perceptlet})
    assert collection.perceptlets == {perceptlet}
    collection.remove(perceptlet)
    assert collection.perceptlets == set()


def test_union():
    perceptlet_1 = Mock()
    perceptlet_2 = Mock()
    collection_1 = PerceptletCollection({perceptlet_1})
    collection_2 = PerceptletCollection({perceptlet_2})
    union = PerceptletCollection.union(collection_1, collection_2)
    assert union.perceptlets == {perceptlet_1, perceptlet_2}


def test_intersection():
    perceptlet_1 = Mock()
    perceptlet_2 = Mock()
    perceptlet_3 = Mock()
    collection_1 = PerceptletCollection({perceptlet_1, perceptlet_2})
    collection_2 = PerceptletCollection({perceptlet_2, perceptlet_3})
    intersection = PerceptletCollection.intersection(collection_1, collection_2)
    assert intersection.perceptlets == {perceptlet_2}


@pytest.mark.parametrize(
    "no_of_valid_members, no_of_invalid_members, expected_proportion",
    [(1, 1, 0.5), (1, 2, 0.33333), (0, 1, 0.0)],
)
def test_number_and_proportion_with_label(
    no_of_valid_members, no_of_invalid_members, expected_proportion,
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
    collection = PerceptletCollection(set.union(valid_members, invalid_members))
    actual_proportion = collection.proportion_with_label(concept)
    assert math.isclose(
        expected_proportion, actual_proportion, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_get_random():
    perceptlets = {Mock() for _ in range(10)}
    collection = PerceptletCollection(perceptlets)
    random_perceptlet = collection.get_random()
    assert random_perceptlet in perceptlets
