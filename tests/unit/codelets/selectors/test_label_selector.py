import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors import LabelSelector
from homer.codelets.suggesters import LabelSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"label": Mock(), "select": Mock()}
    node = Mock()
    node.value = ""
    chamber.input_nodes = [node]
    return chamber


def test_finds_challenger_when_not_given_one(bubble_chamber):
    parent_concept = Mock()
    parent_concept.instance_type = str
    champion = Mock()
    challenger = Mock()
    champion.parent_concept = parent_concept
    champion.size = 1
    champion.quality = 1.0
    champion.activation = 1.0
    challenger.parent_concept = parent_concept
    challenger.size = 1
    challenger.quality = 1.0
    challenger.activation = 1.0
    champion.start.labels_in_space.return_value = StructureCollection(
        {champion, challenger}
    )
    selector = LabelSelector(
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
    with patch.object(random, "random", return_value=random_number):
        parent_concept = Mock()
        parent_concept.instance_type = str
        champion = Mock()
        champion.parent_concept = parent_concept
        champion.size = 1
        champion.quality = champion_quality
        champion.activation = champion_activation
        challenger = Mock()
        challenger.parent_concept = parent_concept
        challenger.size = 1
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        selector = LabelSelector(
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
        assert hasinstance(selector.child_codelets, LabelSelector)
        assert hasinstance(selector.child_codelets, LabelSuggester)
