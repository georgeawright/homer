import pytest
from unittest.mock import Mock

from homer.coderack import Coderack


@pytest.mark.parametrize(
    "urgency_values, bubble_chamber_satisfaction, random_numbers",
    [
        ([0.2, 0.4, 0.6, 0.8], 1.0, [0.9, 0.9, 0.9, 0.9]),
        ([0.2, 0.4, 0.6, 0.8], 0.0, [0.9, 0.1, 0.1, 0.1]),
    ],
)
def test_select_codelet(urgency_values, bubble_chamber_satisfaction, random_numbers):
    codelets = []
    for urgency_value in urgency_values:
        codelet = Mock()
        codelet.urgency = urgency_value
        codelets.append(codelet)
    bubble_chamber = Mock()
    satisfaction = Mock()
    satisfaction.activation.as_scalar.side_effect = [
        bubble_chamber_satisfaction for _ in random_numbers
    ]
    bubble_chamber.concept_space = {"satisfaction": satisfaction}
    coderack = Coderack(bubble_chamber, Mock())
    coderack.IDEAL_POPULATION = 1
    coderack._codelets = codelets
    codelet = coderack._select_codelet()
    assert codelet.urgency in urgency_values
