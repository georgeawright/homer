import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.label_selectors import LabelProjectionSelector
from homer.codelets.suggesters.label_suggesters import LabelProjectionSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def target_view():
    potential_labeling_word = Mock()
    potential_labeling_word.uncorrespondedness = 0.5
    potential_labeling_word.correspondences_to_space.return_value = StructureCollection(
        {Mock()}
    )
    potential_labeling_word.name = "potential labeling word"
    word = Mock()
    word.name = "existing word"
    word.potential_labeling_words = StructureCollection({potential_labeling_word})
    correspondence = Mock()
    correspondence.name = "existing correspondence"
    chunk = Mock()
    chunk.unlabeledness = 0.5
    chunk.name = "existing chunk"
    correspondence.arguments = StructureCollection({chunk, word})
    chunk.is_chunk = True
    chunk.correspondences_to_space.return_value = StructureCollection({correspondence})
    view = Mock()
    view.name = "monitoring view"
    view.interpretation_space.contents = StructureCollection({chunk})
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {"label": Mock(), "select": Mock()}
    chamber.monitoring_views.get_active.return_value = target_view
    return chamber


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
    selector = LabelProjectionSelector(
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
    assert hasinstance(selector.child_codelets, LabelProjectionSuggester)
    assert hasinstance(selector.child_codelets, LabelProjectionSelector)
