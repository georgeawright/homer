import pytest
import random
from unittest.mock import Mock, patch

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.selectors import CorrespondenceSelector
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.tools import hasinstance


def test_finds_challenger_when_not_given_one(bubble_chamber):
    input_space = Mock()
    champion_start = Mock()
    challenger_start = Mock()
    input_space.contents = bubble_chamber.new_structure_collection(
        champion_start, challenger_start
    )
    view = Mock()
    view.input_spaces = bubble_chamber.new_structure_collection(input_space)

    champion = Mock()
    champion.parent_view = view
    champion.start = champion_start
    champion.is_correspondence = True
    champion.size = 1
    champion.quality = 1.0
    champion.activation = 1.0

    challenger = Mock()
    challenger.parent_view = view
    challenger.start = challenger_start
    challenger.is_correspondence = True
    challenger.size = 1
    challenger.quality = 1.0
    challenger.activation = 1.0

    champion.nearby.return_value = bubble_chamber.new_structure_collection(challenger)
    challenger.nearby.return_value = bubble_chamber.new_structure_collection(champion)

    selector = CorrespondenceSelector(
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
        space_1 = Mock()
        space_1.contents = bubble_chamber.new_structure_collection()
        space_2 = Mock()

        new_conceptual_space = Mock()
        new_target_one = Mock()
        space_1.contents.add(new_target_one)
        new_target_one.name = "target1"
        new_target_two = Mock()
        new_space_one = Mock()
        new_target_one.parent_space = new_space_one
        new_space_one.parent_spaces = bubble_chamber.new_structure_collection(space_1)
        new_space_one.conceptual_space = new_conceptual_space
        new_space_two = Mock()
        new_space_two.parent_spaces = bubble_chamber.new_structure_collection(space_2)
        new_space_two.conceptual_space = new_conceptual_space
        new_space_two.is_basic_level = True
        space_2.contents.of_type.return_value = bubble_chamber.new_structure_collection(
            new_target_two
        )

        view = Mock()
        view.name = "view"
        view.input_spaces = bubble_chamber.new_structure_collection(space_1)

        start_argument = Mock()
        start_argument.links.where.return_value = (
            bubble_chamber.new_structure_collection(new_target_one)
        )
        start_argument.parent_space = new_space_one

        champion = Mock()
        space_1.contents.add(champion.start)
        champion.is_correspondence = True
        champion.name = "champion"
        champion.size = 1
        champion.quality = champion_quality
        champion.activation = champion_activation
        champion.start.arguments.get.return_value = start_argument
        champion.parent_view = view

        challenger = Mock()
        challenger.is_correspondence = True
        challenger.name = "challenger"
        challenger.size = 1
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        challenger.start.arguments.get.return_value = start_argument
        challenger.parent_view = view

        selector = CorrespondenceSelector(
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
        assert hasinstance(selector.child_codelets, CorrespondenceSuggester)
        assert hasinstance(selector.child_codelets, CorrespondenceSelector)
