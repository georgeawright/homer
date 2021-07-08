import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.relation_selectors import RelationProjectionSelector
from homer.codelets.suggesters.relation_suggesters import RelationProjectionSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def target_view():
    view = Mock()
    existing_correspondence = Mock()
    existing_correspondence.name = "existing correspondence"
    existing_chunk = Mock()
    existing_chunk.unrelatedness = 0.5
    existing_word = Mock()
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    potential_relating_word = Mock()
    potential_relating_word.uncorrespondedness = 0.5
    potential_relating_word.has_correspondence_to_space.return_value = False
    existing_word.potential_relating_words = StructureCollection(
        {potential_relating_word}
    )
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    existing_chunk.correspondences_to_space.return_value = StructureCollection(
        {existing_correspondence}
    )
    view.interpretation_space.contents.of_type.return_value = StructureCollection(
        {existing_chunk}
    )
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {"relation": Mock(), "select": Mock()}
    chamber.monitoring_views.get_active.return_value = target_view
    return chamber


@pytest.mark.skip
def test_chunk_and_correspondence_are_boosted_follow_up_is_spawned(
    bubble_chamber, target_view
):
    label = Mock()
    label.size = 1
    label.quality = 1.0
    label.activation = 0.0
    correspondence = Mock()
    correspondence.is_correspondence = True
    correspondence.parent_view = target_view
    correspondence.quality = 1.0
    correspondence.activation = 0.0
    selector = RelationProjectionSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({label, correspondence}),
        Mock(),
    )
    selector.run()
    assert CodeletResult.SUCCESS == selector.result
    assert label.boost_activation.is_called()
    assert 2 == len(selector.child_codelets)
    assert hasinstance(selector.child_codelets, RelationProjectionSuggester)
    assert hasinstance(selector.child_codelets, RelationProjectionSelector)
