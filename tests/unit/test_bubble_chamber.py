import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.structure_collection import StructureCollection


@pytest.mark.skip
def test_update_activations():
    pass


def test_has_chunk():
    existing_chunk_members = StructureCollection({Mock(), Mock()})
    existing_chunk = Mock()
    existing_chunk.members = existing_chunk_members
    bubble_chamber = BubbleChamber(
        Mock(),
        Mock(),
        StructureCollection({existing_chunk}),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    assert bubble_chamber.has_chunk(existing_chunk_members)
