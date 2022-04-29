import pytest
import random
from unittest.mock import Mock, patch

from linguoplotter.random_machine import RandomMachine


def test_random_machine_seed():
    random_machine_1 = RandomMachine(Mock(), seed=1)
    random_number_1 = random_machine_1.generate_number()
    random_machine_2 = RandomMachine(Mock(), seed=1)
    random_number_2 = random_machine_2.generate_number()
    assert random_number_1 == random_number_2


@pytest.mark.parametrize(
    "satisfaction, number, random_number, expected",
    [
        (1.0, 0.1, 1.0, 0.1),  # complete determinism when satisfaction == 1
        (1.0, 0.1, 0.0, 0.1),
        (1.0, 0.9, 1.0, 0.9),
        (1.0, 0.9, 0.0, 0.9),
        (0.0, 1.0, 0.1, 0.1),  # complete randomness when satisfaction == 0
        (0.0, 0.0, 0.1, 0.1),
        (0.0, 1.0, 0.9, 0.9),
        (0.0, 0.0, 0.9, 0.9),
        (0.5, 1.0, 0.0, 0.5),  # half randomness when satisfaction == 0.5
        (0.5, 1.0, 0.5, 0.75),
        (0.5, 0.5, 0.0, 0.25),
        (0.5, 0.2, 0.0, 0.1),
    ],
)
def test_randomize_number(satisfaction, number, random_number, expected):
    bubble_chamber = Mock()
    bubble_chamber.satisfaction = satisfaction
    random_machine = RandomMachine(bubble_chamber)
    random_machine.determinism_smoothing_function = lambda x: x
    with patch.object(random, "random", return_value=random_number):
        assert expected == random_machine.randomize_number(number)


def test_select():
    bubble_chamber = Mock()
    bubble_chamber.satisfaction = 0.5
    random_machine = RandomMachine(bubble_chamber, seed=1)

    a = Mock()
    a.name = "a"
    a.quality = 0.5
    b = Mock()
    b.name = "b"
    b.quality = 0.5
    collection = {a: True, b: True}

    selection = random_machine.select(collection, lambda x: x.quality)
    assert selection == a

    selection = random_machine.select(collection, lambda x: x.quality)
    assert selection == a

    selection = random_machine.select(collection, lambda x: x.quality)
    assert selection == b

    selection = random_machine.select(collection, lambda x: x.quality)
    assert selection == b
