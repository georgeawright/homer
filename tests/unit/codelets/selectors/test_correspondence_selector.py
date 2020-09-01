from unittest.mock import Mock, patch

from homer.codelets.selectors import CorrespondenceSelector
from homer.perceptlet_collection import PerceptletCollection

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_passes_preliminary_checks():
    first_argument = Mock()
    second_argument = Mock()
    parent_concept = Mock()
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.first_argument = first_argument
    champion.second_argument = second_argument
    champion.parent_concept = parent_concept
    challenger = Mock()
    challenger.first_argument = first_argument
    challenger.second_argument = second_argument
    challenger.parent_concept = parent_concept
    with patch.object(PerceptletCollection, "get_random", return_value=challenger):
        bubble_chamber = Mock()
        bubble_chamber.workspace.correspondences.at.side_effect = [
            PerceptletCollection(),
            PerceptletCollection(),
        ]
        selector = CorrespondenceSelector(
            bubble_chamber, Mock(), Mock(), champion, Mock(), Mock()
        )
        selector.challenger = challenger
        assert selector._passes_preliminary_checks() is True
        champion.first_argument = second_argument
        champion.second_argument = first_argument
        assert selector._passes_preliminary_checks() is False


def test_engender_follow_up():
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.activation.as_scalar.side_effect = [0.6]
    challenger = Mock()
    challenger.activation.as_scalar.side_effect = [0.5]
    selector = CorrespondenceSelector(
        Mock(), Mock(), Mock(), champion, Mock(), Mock(), challenger
    )
    follow_up = selector._engender_follow_up()
    assert CorrespondenceSelector == type(follow_up)
