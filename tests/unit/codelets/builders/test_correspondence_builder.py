import pytest
from unittest.mock import Mock

from homer.codelets.builders import CorrespondenceBuilder, RelationBuilder
from homer.structure import Structure
from homer.structures.links import Correspondence


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "relation": Mock()}
    return chamber


@pytest.fixture
def target_structure_one():
    structure = Mock()
    structure.has_correspondence.return_value = False
    return structure


def test_gets_second_target_space_and_structure_if_needed(bubble_chamber):
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, Mock(), Mock(), Mock()
    )
    assert correspondence_builder.target_space_two is None
    assert correspondence_builder.target_structure_two is None
    correspondence_builder.run()
    assert correspondence_builder.target_space_two is not None
    assert correspondence_builder.target_structure_two is not None


def test_gets_parent_concept_if_needed(bubble_chamber):
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, Mock(), Mock(), Mock()
    )
    assert correspondence_builder.parent_concept is None
    correspondence_builder.run()
    assert correspondence_builder.parent_concept is not None


def test_successful_creates_chunk_and_spawns_follow_up(
    bubble_chamber, target_structure_one, parent_concept
):
    correspondence_builder = CorrespondenceBuilder(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber,
        Mock(),
        target_structure_one,
        Mock(),
        parent_concept=parent_concept,
    )
    correspondence_builder.run()
    assert isinstance(correspondence_builder.child_structure, Correspondence)
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)


def test_fails_when_structures_do_not_correspond(bubble_chamber, target_structure_one):
    concept = Mock()
    concept.classify.return_value = 0.0
    correspondence_builder = CorrespondenceBuilder(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber,
        Mock(),
        target_structure_one,
        Mock(),
        parent_concept=concept,
    )
    correspondence_builder.run()
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], RelationBuilder)


def test_fizzles_when_correspondence_already_exists(bubble_chamber):
    target_structure_one = Mock()
    target_structure_one.has_correspondence.return_value = True
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, Mock()
    )
    correspondence_builder.run()
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)
