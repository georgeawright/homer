import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder
from homer.codelets.evaluators.chunk_evaluators import ChunkProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.fixture
def target_view():
    word = Mock()
    word.is_word = True
    view = Mock()
    view.text_space.contents = StructureCollection({word})
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {
        "build": Mock(),
        "chunk": Mock(),
        "noun": Mock(),
        "same": Mock(),
        "text": Mock(),
    }
    chamber.monitoring_views = StructureCollection({target_view})
    return chamber


@pytest.fixture
def target_word():
    word = Mock()
    return word


@pytest.mark.skip
def test_successful_creates_chunk_corresponding_to_word_and_spawns_follow_up(
    bubble_chamber, target_view, target_word
):
    target_word.has_correspondence_to_space.return_value = False
    target_structures = {"target_view": target_view, "target_word": target_word}
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert len(builder.child_codelets) == 1
    assert isinstance(builder.child_codelets[0], ChunkProjectionEvaluator)


@pytest.mark.skip
def test_fizzles_if_target_word_already_has_correspondence_in_interpretation(
    bubble_chamber, target_view, target_word
):
    target_word.has_correspondence_to_space.return_value = True
    target_structures = {"target_view": target_view, "target_word": target_word}
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
