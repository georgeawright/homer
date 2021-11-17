import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.random_machine import RandomMachine
from homer.structure_collection import StructureCollection


def test_setup():
    bubble_chamber = BubbleChamber.setup(Mock())
    assert isinstance(bubble_chamber.chunks, StructureCollection)
    assert isinstance(bubble_chamber.random_machine, RandomMachine)
    assert bubble_chamber.random_machine.seed is None

    bubble_chamber = BubbleChamber.setup(Mock(), random_seed=1)
    assert isinstance(bubble_chamber.random_machine, RandomMachine)
    assert bubble_chamber.random_machine.seed == 1
