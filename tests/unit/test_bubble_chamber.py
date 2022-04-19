import pytest
from unittest.mock import Mock

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.random_machine import RandomMachine
from linguoplotter.structure_collection import StructureCollection


def test_setup():
    bubble_chamber = BubbleChamber.setup(Mock())
    assert isinstance(bubble_chamber.chunks, StructureCollection)
    assert isinstance(bubble_chamber.random_machine, RandomMachine)
    assert bubble_chamber.random_machine.seed is None

    bubble_chamber = BubbleChamber.setup(Mock(), random_seed=1)
    assert isinstance(bubble_chamber.random_machine, RandomMachine)
    assert bubble_chamber.random_machine.seed == 1
