import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder
from homer.codelets.suggesters.chunk_suggesters import ChunkProjectionSuggester
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
        "suggest": Mock(),
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
def test_gives_high_confidence_if_word_does_not_have_correspondence(
    bubble_chamber, target_view, target_word
):
    target_word.has_correspondence_to_space.return_value = False
    target_structures = {"target_view": target_view, "target_word": target_word}
    suggester = ChunkProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], ChunkProjectionBuilder)


@pytest.mark.skip
def test_fizzles_if_target_word_already_has_correspondence_in_interpretation(
    bubble_chamber, target_view, target_word
):
    target_word.has_correspondence_to_space.return_value = True
    target_structures = {"target_view": target_view, "target_word": target_word}
    suggester = ChunkProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
