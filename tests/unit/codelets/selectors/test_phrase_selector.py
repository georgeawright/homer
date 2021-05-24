import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors import PhraseSelector
from homer.codelets.suggesters import PhraseSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"phrase": Mock(), "select": Mock()}
    target_one = Mock()
    target_two = Mock()
    target_three = Mock()
    target_one.members = StructureCollection({target_two, target_three})
    target_two.members = StructureCollection({Mock(), Mock()})
    target_three.members = StructureCollection({Mock(), Mock()})
    target_one.unhappiness = 1.0
    target_two.unhappiness = 1.0
    target_three.unhappiness = 1.0
    chamber.text_fragments = StructureCollection({target_one, target_two, target_three})
    target_one.potential_rule_mates = StructureCollection({target_two, target_three})
    target_two.potential_rule_mates = StructureCollection({target_one, target_three})
    target_three.potential_rule_mates = StructureCollection({target_one, target_two})
    return chamber


def test_finds_challenger_when_not_given_one(bubble_chamber):
    word = Mock()
    word.is_word = True
    word.unhappiness = 1.0
    phrase = Mock()
    phrase.is_phrase = True
    phrase.unhappiness = 1.0
    word.potential_rule_mates = StructureCollection({phrase})
    phrase.potential_rule_mates = StructureCollection({word})
    text_space = Mock()
    text_space.contents = StructureCollection({word, phrase})

    with patch.object(
        PhraseSuggester, "arrange_targets", return_value=(word, phrase, None)
    ):
        common_member = Mock()
        champion = Mock()
        champion.members = StructureCollection({Mock(), common_member})
        champion.size = 2
        champion.parent_space = text_space
        challenger = Mock()
        challenger.members = StructureCollection({common_member, Mock()})
        challenger.size = 2
        challenger.parent_space = text_space
        champion.quality = 1.0
        champion.activation = 1.0
        challenger.quality = 1.0
        challenger.activation = 1.0
        collection = Mock()
        collection.get_active.return_value = challenger
        champion.nearby.return_value = collection
        selector = PhraseSelector(
            Mock(), Mock(), bubble_chamber, StructureCollection({champion}), Mock()
        )
        assert selector.challengers is None
        selector.run()
        assert selector.challengers == StructureCollection({challenger})


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
    word = Mock()
    word.is_word = True
    word.unhappiness = 1.0
    phrase = Mock()
    phrase.is_phrase = True
    phrase.unhappiness = 1.0
    word.potential_rule_mates = StructureCollection({phrase})
    phrase.potential_rule_mates = StructureCollection({word})
    text_space = Mock()
    text_space.contents = StructureCollection({word, phrase})
    with patch.object(random, "random", return_value=random_number), patch.object(
        PhraseSuggester, "arrange_targets", return_value=(word, phrase, None)
    ):
        champion = Mock()
        champion.parent_space = text_space
        champion.size = 2
        champion.quality = champion_quality
        champion.activation = champion_activation
        challenger = Mock()
        challenger.parent_space = text_space
        challenger.size = 2
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        selector = PhraseSelector(
            Mock(),
            Mock(),
            bubble_chamber,
            StructureCollection({champion}),
            Mock(),
            challengers=StructureCollection({challenger}),
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
        assert hasinstance(selector.child_codelets, PhraseSuggester)
        assert hasinstance(selector.child_codelets, PhraseSelector)
