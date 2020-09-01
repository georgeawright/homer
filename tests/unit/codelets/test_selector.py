import pytest
import random
from unittest.mock import Mock, patch

from homer.codelets.selectors import GroupSelector


@pytest.mark.parametrize(
    "champion_quality, challenger_quality, champion_random, challenger_random, "
    + "selection_randomness, expected",
    [
        (1.0, 0.0, 1.0, 0.0, 0.5, 1.0),
        (0.0, 1.0, 0.0, 1.0, 0.5, -1.0),
        (0.5, 0.5, 0.0, 1.0, 0.5, -0.5),
    ],
)
def test_calculate_confidence(
    champion_quality,
    challenger_quality,
    champion_random,
    challenger_random,
    selection_randomness,
    expected,
):
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.quality = champion_quality
    challenger = Mock()
    challenger.quality = challenger_quality
    with patch.object(
        random, "random", side_effect=[champion_random, challenger_random]
    ):
        selector = GroupSelector(
            Mock(), Mock(), Mock(), champion, Mock(), Mock(), challenger
        )
        selector.SELECTION_RANDOMNESS = selection_randomness
        selector._calculate_confidence()
        assert expected == selector.confidence
