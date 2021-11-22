import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters.projection_suggesters import (
    LetterChunkProjectionSuggester,
)
from homer.structure_collection import StructureCollection


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(bubble_chamber, target_view):
    word = Mock()
    frame_correspondee = Mock()
    frame_correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = frame_correspondee
    frame_correspondence.end = word
    word.correspondences = bubble_chamber.new_structure_collection(frame_correspondence)
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = frame_correspondee
    frame_correspondee.correspondences = bubble_chamber.new_structure_collection(
        non_frame_correspondence
    )
    target_view.members = bubble_chamber.new_structure_collection(
        frame_correspondence, non_frame_correspondence
    )
    target_view.slot_values[frame_correspondee.structure_id] = Mock()
    return word


def test_gives_suggests_projection_from_slot(
    bubble_chamber, target_view, target_projectee
):
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LetterChunkProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result


def test_gives_full_confidence_to_project_non_slot(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.correspondences = bubble_chamber.new_structure_collection()
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
    assert CodeletResult.SUCCESS == suggester.result
    assert 1.0 == suggester.confidence


def test_fizzles_if_word_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_view.slot_values[target_projectee.structure_id] = Mock()
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LetterChunkProjectionSuggester(
        "", "", bubble_chamber, target_structures, 1.0
    )
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
