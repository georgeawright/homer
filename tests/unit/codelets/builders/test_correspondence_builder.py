import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder, RelationBuilder
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    labeling_spaces = Mock()
    labeling_spaces.child_spaces = StructureCollection({Mock(), Mock()})
    correspondential_concepts = Mock()
    correspondential_concepts.contents = StructureCollection({parent_concept})
    target_structure_two = Mock()
    target_structure_two.parent_spaces = labeling_spaces.child_spaces
    working_spaces = Mock()
    working_space = Mock()
    working_space_contents = Mock()
    working_space_contents.get_exigent.return_value = target_structure_two
    working_space.contents.of_type.return_value = working_space_contents
    working_spaces.contents.get_active.return_value = working_space
    chamber.spaces = {
        "label concepts": labeling_spaces,
        "correspondential concepts": correspondential_concepts,
        "working spaces": working_spaces,
    }
    return chamber


@pytest.fixture
def target_structure_one(bubble_chamber):
    structure = Mock()
    structure.has_correspondence.return_value = False
    structure.parent_spaces = bubble_chamber.spaces["label concepts"].child_spaces
    return structure


def test_gets_second_target_space_and_structure_if_needed(
    bubble_chamber,
    target_structure_one,
    parent_concept,
):
    correspondence_builder = CorrespondenceBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        Mock(),
        target_structure_one,
        Mock(),
        parent_concept=parent_concept,
    )
    assert correspondence_builder.target_space_two is None
    assert correspondence_builder.target_structure_two is None
    correspondence_builder.run()
    assert correspondence_builder.target_space_two is not None
    assert correspondence_builder.target_structure_two is not None


def test_gets_parent_concept_if_needed(bubble_chamber, target_structure_one):
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, Mock()
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
        bubble_chamber,
        Mock(),
        target_structure_one,
        Mock(),
        parent_concept=parent_concept,
    )
    result = correspondence_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(correspondence_builder.child_structure, Correspondence)
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)


def test_fails_when_structures_do_not_correspond(bubble_chamber, target_structure_one):
    concept = Mock()
    concept.classifier.classify.return_value = 0.0
    correspondence_builder = CorrespondenceBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        Mock(),
        target_structure_one,
        Mock(),
        parent_concept=concept,
    )
    result = correspondence_builder.run()
    assert CodeletResult.FAIL == result
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], RelationBuilder)


def test_fizzles_when_correspondence_already_exists(bubble_chamber):
    target_structure_one = Mock()
    target_structure_one.has_correspondence.return_value = True
    target_structure_one.parent_spaces = bubble_chamber.spaces[
        "label concepts"
    ].child_spaces
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, Mock()
    )
    result = correspondence_builder.run()
    assert CodeletResult.FIZZLE == result
    assert correspondence_builder.child_structure is None
    assert len(correspondence_builder.child_codelets) == 1
    assert isinstance(correspondence_builder.child_codelets[0], CorrespondenceBuilder)
