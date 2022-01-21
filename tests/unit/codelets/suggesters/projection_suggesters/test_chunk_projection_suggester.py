import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters.projection_suggesters import ChunkProjectionSuggester
from homer.structure_collection import StructureCollection


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "same": Mock(), "chunk": Mock()}
    return chamber


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    chunk = Mock()
    return chunk


def test_gives_full_confidence_to_project_chunk(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = ChunkProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FINISH == suggester.result
    assert 1.0 == suggester.confidence


def test_fizzles_if_chunk_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = ChunkProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
