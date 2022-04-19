import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters.projection_suggesters import (
    LetterChunkProjectionSuggester,
)
from linguoplotter.structure_collection import StructureCollection


@pytest.fixture
def target_view(bubble_chamber):
    view = Mock()
    view.slot_values = {}
    input_space = Mock()
    input_space.quality = 1
    view.input_spaces = bubble_chamber.new_structure_collection(input_space)
    return view


@pytest.fixture
def target_projectee(bubble_chamber, target_view):
    word = Mock()
    grammar_label = Mock()
    grammar_label.parent_concept.is_slot = True
    grammar_label.parent_concept.is_filled_in = True
    meaning_label = Mock()
    meaning_label.parent_concept.is_slot = True
    meaning_label.parent_concept.is_filled_in = True
    word.labels = bubble_chamber.new_structure_collection(grammar_label, meaning_label)
    word.relations = bubble_chamber.new_structure_collection()
    parent_space = Mock()
    parent_space.is_contextual_space = True
    word.parent_spaces = bubble_chamber.new_structure_collection(parent_space)
    word.correspondences = bubble_chamber.new_structure_collection()
    return word


def test_suggests_projection_from_slot(bubble_chamber, target_view, target_projectee):
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LetterChunkProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FINISH == suggester.result


def test_gives_full_confidence_to_project_non_slot(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.is_slot = False
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LetterChunkProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FINISH == suggester.result
    assert 1.0 == suggester.confidence


def test_fizzles_if_word_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LetterChunkProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
