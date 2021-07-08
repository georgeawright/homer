import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.chunk_selectors import ReverseChunkProjectionSelector
from homer.codelets.suggesters.chunk_suggesters import ReverseChunkProjectionSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def target_view():
    word = Mock()
    word.is_word = True
    word.has_label.return_value = True
    view = Mock()
    view.text_space.contents = StructureCollection({word})
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "select": Mock(), "noun": Mock()}
    chamber.monitoring_views.get_active.return_value = target_view
    return chamber


@pytest.mark.skip
def test_chunk_and_correspondence_are_boosted_follow_up_is_spawned(
    bubble_chamber, target_view
):
    chunk = Mock()
    chunk.size = 1
    chunk.quality = 1.0
    chunk.activation = 0.0
    interpretation_chunk = Mock()
    interpretation_chunk.is_chunk = True
    interpretation_chunk.quality = 1.0
    interpretation_chunk.activation = 0.0
    interpretation_chunk.members = StructureCollection({chunk})
    correspondence = Mock()
    correspondence.is_correspondence = True
    correspondence.quality = 1.0
    correspondence.activation = 0.0
    correspondence.parent_view = target_view
    selector = ReverseChunkProjectionSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({chunk, interpretation_chunk, correspondence}),
        Mock(),
    )
    selector.run()
    assert CodeletResult.SUCCESS == selector.result
    assert chunk.boost_activation.is_called()
    assert 2 == len(selector.child_codelets)
    assert hasinstance(selector.child_codelets, ReverseChunkProjectionSuggester)
    assert hasinstance(selector.child_codelets, ReverseChunkProjectionSelector)
