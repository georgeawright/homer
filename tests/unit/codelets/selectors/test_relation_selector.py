import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import RelationBuilder
from homer.codelets.selectors import RelationSelector
from homer.structure_collection import StructureCollection


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"relation": Mock(), "select": Mock()}
    return chamber


def test_finds_challenger_when_not_given_one(bubble_chamber):
    champion = Mock()
    challenger = Mock()
    champion.quality = 1.0
    champion.activation = 1.0
    challenger.quality = 1.0
    challenger.activation = 1.0
    champion.start.relations_in_space_with.return_value = StructureCollection(
        {champion, challenger}
    )
    selector = RelationSelector(Mock(), Mock(), bubble_chamber, champion, Mock())
    assert selector.challenger is None
    selector.run()
    assert selector.challenger == challenger


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
        champion.quality = champion_quality
        champion.activation = champion_activation
        challenger = Mock()
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        selector = RelationSelector(
            Mock(), Mock(), bubble_chamber, champion, Mock(), challenger=challenger
        )
        selector.run()
        assert CodeletResult.SUCCESS == selector.result
        if expected_winner == "champion":
            assert champion.boost_activation.is_called()
            assert challenger.decay_activation.is_called()
        else:
            assert challenger.boost_activation.is_called()
            assert champion.decay_activation.is_called()
        assert 1 == len(selector.child_codelets)
        assert isinstance(selector.child_codelets[0], RelationSelector)


def test_spawns_builder_when_fizzling(bubble_chamber):
    champion = Mock()
    champion.start.relations_in_space_with.return_value = StructureCollection(
        {champion}
    )
    selector = RelationSelector(Mock(), Mock(), bubble_chamber, champion, Mock())
    selector.run()
    assert selector.challenger is None
    assert CodeletResult.FIZZLE == selector.result
    assert 1 == len(selector.child_codelets)
    assert isinstance(selector.child_codelets[0], RelationBuilder)
