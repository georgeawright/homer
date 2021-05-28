import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.selectors import CorrespondenceSelector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"correspondence": Mock(), "select": Mock()}
    return chamber


def test_finds_challenger_when_not_given_one(bubble_chamber):
    space_1 = Mock()
    space_2 = Mock()

    new_conceptual_space = Mock()
    new_target_one = Mock()
    new_target_two = Mock()
    new_space_one = Mock()
    new_target_one.parent_space = new_space_one
    new_space_one.parent_spaces = StructureCollection({space_1})
    new_space_one.conceptual_space = new_conceptual_space
    new_space_two = Mock()
    new_space_two.conceptual_space = new_conceptual_space
    new_space_two.is_basic_level = True
    space_2.contents.of_type.return_value = StructureCollection({new_space_two})

    view = Mock()
    view.input_spaces = StructureCollection({space_1, space_2})

    start_argument = Mock()
    start_argument.links.not_of_type.return_value = StructureCollection(
        {new_target_one}
    )
    start_argument.parent_space = new_space_one

    champion = Mock()
    challenger = Mock()
    champion.size = 1
    champion.quality = 1.0
    champion.activation = 1.0
    champion.start.arguments.get.return_value = start_argument
    champion.parent_view = view

    challenger.size = 1
    challenger.quality = 1.0
    challenger.activation = 1.0
    challenger.start.arguments.get.return_value = start_argument
    challenger.parent_view = view

    champion.start.correspondences_to_space.return_value = StructureCollection(
        {champion, challenger}
    )

    selector = CorrespondenceSelector(
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
        space_1 = Mock()
        space_2 = Mock()

        new_conceptual_space = Mock()
        new_target_one = Mock()
        new_target_two = Mock()
        new_space_one = Mock()
        new_target_one.parent_space = new_space_one
        new_space_one.parent_spaces = StructureCollection({space_1})
        new_space_one.conceptual_space = new_conceptual_space
        new_space_two = Mock()
        new_space_two.conceptual_space = new_conceptual_space
        new_space_two.is_basic_level = True
        space_2.contents.of_type.return_value = StructureCollection({new_space_two})

        view = Mock()
        view.input_spaces = StructureCollection({space_1, space_2})

        start_argument = Mock()
        start_argument.links.not_of_type.return_value = StructureCollection(
            {new_target_one}
        )
        start_argument.parent_space = new_space_one

        champion = Mock()
        champion.size = 1
        champion.quality = champion_quality
        champion.activation = champion_activation
        champion.start.arguments.get.return_value = start_argument
        champion.parent_view = view

        challenger = Mock()
        challenger.size = 1
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        challenger.start.arguments.get.return_value = start_argument
        challenger.parent_view = view

        selector = CorrespondenceSelector(
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
        assert hasinstance(selector.child_codelets, CorrespondenceSuggester)
        assert hasinstance(selector.child_codelets, CorrespondenceSelector)
