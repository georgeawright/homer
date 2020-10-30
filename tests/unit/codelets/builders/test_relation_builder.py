import pytest
from unittest.mock import Mock

from homer.codelets.builders import ChunkBuilder, RelationBuilder
from homer.structures.links import Relation


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "relation": Mock()}
    chamber.get_random_relation_concept.return_value = parent_concept
    return chamber


@pytest.fixture
def target_structure_two():
    structure = Mock()
    return structure


@pytest.fixture
def target_structure_one(target_structure_two):
    structure = Mock()
    parent_space_contents = Mock()
    parent_space_contents.get_exigent.return_value = target_structure_two
    structure.parent_spaces.get_random.return_value = parent_space_contents
    structure.has_relation.return_value = False
    structure.nearby.get_unhappy.return_value = Mock()
    return structure


def test_bottom_up_codelet_gets_a_concept(bubble_chamber):
    target_structure_one = Mock()
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure_one, Mock()
    )
    assert relation_builder.parent_concept is None
    relation_builder.run()
    assert relation_builder.parent_concept is not None


def test_codelet_gets_a_second_target_structure(bubble_chamber, target_structure_one):
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure_one, Mock()
    )
    assert relation_builder.target_structure_two is None
    relation_builder.run()
    assert relation_builder.target_structure_two is not None


def test_successful_creates_chunk_and_spawns_follow_up(
    bubble_chamber, target_structure_one
):
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure_one, Mock()
    )
    relation_builder.run()
    assert isinstance(relation_builder.child_structure, Relation)
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationBuilder)


def test_fails_when_structures_cannot_be_related(
    parent_concept, bubble_chamber, target_structure_one
):
    parent_concept.classify.return_value = 0.0
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure_one, Mock()
    )
    relation_builder.run()
    assert relation_builder.child_structure is None
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], ChunkBuilder)


def test_fizzles_when_relation_already_exists(bubble_chamber, target_structure_one):
    target_structure_one.has_relation.return_value = True
    relation_builder = RelationBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_structure_one, Mock()
    )
    relation_builder.run()
    assert relation_builder.child_structure is None
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationBuilder)
