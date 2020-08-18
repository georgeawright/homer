import pytest
import random
from unittest.mock import Mock, patch

from homer.coderack import Coderack


@pytest.mark.parametrize(
    "urgency_values, bubble_chamber_satisfaction, random_numbers, expected_urgency",
    [
        ([0.2, 0.4, 0.6, 0.8], 1.0, [0.9, 0.9, 0.9, 0.9], 0.8),
        ([0.2, 0.4, 0.6, 0.8], 0.0, [0.9, 0.1, 0.1, 0.1], 0.2),
    ],
)
def test_select_codelet(
    urgency_values, bubble_chamber_satisfaction, random_numbers, expected_urgency
):
    with patch.object(random, "random", side_effect=random_numbers):
        codelets = []
        for urgency_value in urgency_values:
            codelet = Mock()
            codelet.urgency = urgency_value
            codelets.append(codelet)
        bubble_chamber = Mock()
        bubble_chamber.satisfaction = bubble_chamber_satisfaction
        coderack = Coderack(bubble_chamber, Mock())
        coderack.IDEAL_POPULATION = 1
        coderack._codelets = codelets
        codelet = coderack.select_codelet()
        assert expected_urgency == codelet.urgency
