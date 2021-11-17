import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.tools import hasinstance


@pytest.fixture
def same_concept(bubble_chamber):
    concept = Mock()
    concept.name = "same"
    concept.structure_type = Correspondence
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def same_different_space(bubble_chamber, same_concept):
    space = Mock()
    space.contents.of_type.return_value = bubble_chamber.new_structure_collection(
        same_concept
    )
    bubble_chamber.spaces.add(space)
    return space


@pytest.fixture
def conceptual_space(bubble_chamber):
    space = Mock()
    space.is_conceptual_space = True
    space.is_basic_level = True
    bubble_chamber.spaces.add(space)
    return space


@pytest.fixture
def target_space_one(bubble_chamber, conceptual_space):
    space = Mock()
    space.name = "target_space_one"
    space.is_conceptual_space = False
    space.parent_spaces = []
    space.conceptual_spaces = bubble_chamber.new_structure_collection(conceptual_space)
    return space


@pytest.fixture
def target_space_two(bubble_chamber, conceptual_space):
    space = Mock()
    space.name = "target_space_two"
    space.is_conceptual_space = False
    space.conceptual_spaces = bubble_chamber.new_structure_collection(conceptual_space)
    return space


@pytest.fixture
def target_structure_one(bubble_chamber, conceptual_space, target_space_one):
    structure = Mock()
    structure.is_slot = False
    structure.correspondences = bubble_chamber.new_structure_collection()
    structure.has_correspondence.return_value = False
    structure.parent_spaces = bubble_chamber.new_structure_collection(
        conceptual_space, target_space_one
    )
    return structure


@pytest.fixture
def target_structure_two(bubble_chamber, conceptual_space, target_space_two):
    structure = Mock()
    structure.is_slot = True
    structure.correspondences = bubble_chamber.new_structure_collection()
    structure.name = "target_structure_two"
    structure.parent_spaces = bubble_chamber.new_structure_collection(
        target_space_two, conceptual_space
    )
    target_space_two.contents.of_type.return_value = (
        bubble_chamber.new_structure_collection(structure)
    )
    return structure


@pytest.fixture
def existing_correspondence():
    correspondence = Mock()
    return correspondence


@pytest.fixture
def target_view(
    bubble_chamber, existing_correspondence, target_space_one, target_space_two
):
    input_space = Mock()
    input_space.name = "target space 2 container"
    input_space.contents.of_type.return_value = bubble_chamber.new_structure_collection(
        target_space_two
    )
    view = Mock()
    view.input_spaces = bubble_chamber.new_structure_collection(input_space)
    view.has_member.return_value = False
    view.members = bubble_chamber.new_structure_collection(existing_correspondence)
    view.slot_values = {}
    return view


def test_gets_second_target_space_and_structure_if_needed(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    same_concept,
    target_space_two,
    target_structure_two,
):
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    assert correspondence_suggester.target_space_two is None
    assert correspondence_suggester.target_structure_two is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_space_two == target_space_two
    assert correspondence_suggester.target_structure_two == target_structure_two


def test_gets_parent_concept_if_needed(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
):
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": None,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    assert correspondence_suggester.parent_concept is None
    correspondence_suggester.run()
    assert correspondence_suggester.parent_concept is not None


def test_gives_high_confidence_for_good_example(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    same_concept,
    target_space_two,
    target_structure_two,
):
    same_concept.classifier.classify.return_value = 1.0
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert correspondence_suggester.confidence == 1
    assert len(correspondence_suggester.child_codelets) == 1
    assert isinstance(correspondence_suggester.child_codelets[0], CorrespondenceBuilder)


def test_gives_low_confidence_for_bad_example(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
):
    concept = Mock()
    concept.classifier.classify.return_value = 0.0
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": concept,
    }

    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert correspondence_suggester.confidence == 0
    assert len(correspondence_suggester.child_codelets) == 1
    assert isinstance(correspondence_suggester.child_codelets[0], CorrespondenceBuilder)


def test_fizzles_when_correspondence_already_exists(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
    same_concept,
):
    target_view.has_member.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }

    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.FIZZLE == result
