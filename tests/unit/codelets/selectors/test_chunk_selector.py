import pytest
import random
from unittest.mock import Mock, patch

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.evaluators import ChunkEvaluator
from linguoplotter.codelets.selectors import ChunkSelector
from linguoplotter.codelets.suggesters import ChunkSuggester
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.tools import hasinstance


def test_finds_challenger_when_not_given_one(bubble_chamber):
    common_members = bubble_chamber.new_structure_collection(Mock(), Mock())
    champion = Mock()
    champion.is_chunk = True
    champion.is_slot = False
    champion.members = common_members
    champion.size = 2
    challenger = Mock()
    challenger.is_slot = False
    challenger.members = common_members
    challenger.size = 2
    champion.quality = 1.0
    champion.activation = 1.0
    challenger.quality = 1.0
    challenger.activation = 1.0
    collection = Mock()
    collection.get.return_value = challenger
    champion.nearby.return_value = collection
    selector = ChunkSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(champion),
        Mock(),
    )
    assert selector.challengers is None
    selector.run()
    assert selector.challengers == bubble_chamber.new_structure_collection(challenger)


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
):
    with patch.object(random, "random", return_value=random_number):
        champion = Mock()
        champion.is_slot = False
        champion.size = 2
        champion.quality = champion_quality
        champion.activation = champion_activation
        challenger = Mock()
        challenger.is_slot = False
        challenger.size = 2
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        selector = ChunkSelector(
            Mock(),
            Mock(),
            bubble_chamber,
            bubble_chamber.new_structure_collection(champion),
            Mock(),
            challengers=bubble_chamber.new_structure_collection(challenger),
        )
        selector.run()
        assert CodeletResult.FINISH == selector.result
        if expected_winner == "champion":
            assert champion.boost_activation.is_called()
            assert challenger.decay_activation.is_called()
        else:
            assert challenger.boost_activation.is_called()
            assert champion.decay_activation.is_called()
        assert 2 == len(selector.child_codelets)
        assert hasinstance(selector.child_codelets, ChunkSuggester)
        assert hasinstance(selector.child_codelets, ChunkEvaluator)
