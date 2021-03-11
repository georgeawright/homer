import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.tools import equivalent_space


def test_equivalent_space():
    common_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    original_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        common_concept,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    original_space_copy = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        common_concept,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    other_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    structure_with_equivalent_space = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), original_space_copy), Location(Mock(), other_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    structure_without_equivalent_space = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), other_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    assert original_space_copy == equivalent_space(
        structure_with_equivalent_space, original_space
    )
    with pytest.raises(Exception):
        equivalent_space(structure_without_equivalent_space, original_space)
