import pytest
from unittest.mock import Mock

from linguoplotter.coderack import Coderack
from linguoplotter.random_machine import RandomMachine


@pytest.mark.parametrize(
    "urgency_values, bubble_chamber_satisfaction, random_seed, expected_urgencies",
    [
        # completetly deterministic
        (
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            1.0,
            1,
            [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        ),
        # semi-random
        (
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            0.5,
            1,
            [0.9, 0.7, 0.8, 0.4, 0.5, 0.3, 0.6, 0.1, 0.2],
        ),
        # completely random
        (
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            0.0,
            1,
            [0.2, 0.3, 0.1, 0.9, 0.7, 0.5, 0.6, 0.8, 0.4],
        ),
    ],
)
def test_select_a_codelet(
    urgency_values, bubble_chamber_satisfaction, random_seed, expected_urgencies
):
    bubble_chamber = Mock()
    bubble_chamber.satisfaction = bubble_chamber_satisfaction
    bubble_chamber.random_machine = RandomMachine(bubble_chamber, random_seed)
    bubble_chamber.random_machine.determinism_smoothing_function = lambda x: x
    coderack = Coderack(bubble_chamber, Mock())
    coderack.IDEAL_POPULATION = 1
    for urgency_value in urgency_values:
        codelet = Mock()
        codelet.urgency = urgency_value
        coderack._codelets.append(codelet)
    for expected_urgency in expected_urgencies:
        codelet = coderack._select_a_codelet()
        assert expected_urgency == codelet.urgency
