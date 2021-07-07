import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.chunk_selectors import ChunkProjectionSelector
from homer.codelets.suggesters.chunk_suggesters import ChunkProjectionSuggester
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
    chamber.monitoring_views.get.return_value = target_view
    return chamber


def test_finds_challenger_when_not_given_one(bubble_chamber, target_view):
    common_members = StructureCollection({Mock(), Mock()})
    champion = Mock()
    champion.is_chunk = True
    champion.members = common_members
    champion.size = 2
    champion_correspondence = Mock()
    champion_correspondence.is_correspondence = True
    champion_correspondence.parent_view = target_view
    challenger = Mock()
    challenger.is_chunk = True
    challenger.members = common_members
    challenger.size = 2
    challenger_correspondence = Mock()
    challenger_correspondence.is_correspondence = True
    challenger_correspondence.parent_view = target_view
    challenger.correspondences = StructureCollection({challenger_correspondence})
    champion.quality = 1.0
    champion.activation = 1.0
    champion_correspondence.quality = 1.0
    champion_correspondence.activation = 1.0
    challenger.quality = 1.0
    challenger.activation = 1.0
    challenger_correspondence.quality = 1.0
    challenger_correspondence.activation = 1.0
    collection = Mock()
    collection.get.return_value = challenger
    champion.nearby.return_value = collection
    selector = ChunkProjectionSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({champion, champion_correspondence}),
        Mock(),
    )
    assert selector.challengers is None
    selector.run()
    assert selector.challengers == StructureCollection(
        {challenger, challenger_correspondence}
    )


@pytest.mark.parametrize(
    "champion_quality, champion_activation, "
    + "challenger_quality, challenger_activation, "
    + "random_number, expected_winner",
    [
        (1.0, 0.5, 0.0, 0.5, 0.5, "champion"),  # champion is better
        (0.5, 1.0, 1.0, 0.0, 0.5, "challenger"),  # challenger is better
        (0.5, 1.0, 1.0, 0.0, 0.1, "champion"),  # challenger is better but rand too low
        (1.0, 1.0, 0.5, 0.0, 0.9, "challenger"),  # champion is better but rand too high
    ],
)
def test_winner_is_boosted_loser_is_decayed_follow_up_is_spawned(
    champion_quality,
    champion_activation,
    challenger_quality,
    challenger_activation,
    random_number,
    expected_winner,
    bubble_chamber,
    target_view,
):
    with patch.object(random, "random", return_value=random_number):
        champion = Mock()
        champion.is_chunk = True
        champion.size = 2
        champion.quality = champion_quality
        champion.activation = champion_activation
        champion_correspondence = Mock()
        champion_correspondence.is_correspondence = True
        champion_correspondence.parent_view = target_view
        champion_correspondence.quality = champion_quality
        champion_correspondence.activation = champion_activation
        challenger = Mock()
        challenger.is_chunk = True
        challenger.size = 2
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        challenger_correspondence = Mock()
        challenger_correspondence.is_correspondence = True
        challenger_correspondence.parent_view = target_view
        challenger_correspondence.quality = challenger_quality
        challenger_correspondence.activation = challenger_activation
        selector = ChunkProjectionSelector(
            Mock(),
            Mock(),
            bubble_chamber,
            StructureCollection({champion, champion_correspondence}),
            Mock(),
            challengers=StructureCollection({challenger, challenger_correspondence}),
        )
        selector.run()
        assert CodeletResult.SUCCESS == selector.result
        if expected_winner == "champion":
            assert champion.boost_activation.is_called()
            assert challenger.decay_activation.is_called()
        else:
            assert challenger.boost_activation.is_called()
            assert champion.decay_activation.is_called()
        assert 2 == len(selector.child_codelets)
        assert hasinstance(selector.child_codelets, ChunkProjectionSuggester)
        assert hasinstance(selector.child_codelets, ChunkProjectionSelector)
