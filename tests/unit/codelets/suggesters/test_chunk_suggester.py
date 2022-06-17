import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters import ChunkSuggester
from linguoplotter.codelets.builders import ChunkBuilder
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Chunk
from linguoplotter.tools import hasinstance


@pytest.fixture
def parent_space():
    space = Mock()
    space.name = "conceptual"
    space.is_conceptual_space = True
    space.is_basic_level = True
    space.proximity_between.return_value = 1.0
    return space


@pytest.fixture
def target_structure_two(bubble_chamber, parent_space):
    chunk = Mock()
    chunk.members = bubble_chamber.new_structure_collection()
    chunk.parent_spaces = bubble_chamber.new_structure_collection(parent_space)
    chunk.chunking_exigency = 1.0
    return chunk


@pytest.fixture
def target_structure_one(bubble_chamber, parent_space, target_structure_two):
    chunk = Mock()
    chunk.members = bubble_chamber.new_structure_collection()
    chunk.parent_spaces = bubble_chamber.new_structure_collection(parent_space)
    chunk.potential_chunk_mates = bubble_chamber.new_structure_collection(
        target_structure_two
    )
    return chunk


def test_gets_target_structure_two(bubble_chamber, target_structure_one):
    target_structures = {"target_structure_one": target_structure_one}
    suggester = ChunkSuggester("", "", bubble_chamber, target_structures, 1)
    assert suggester.target_structure_two is None
    suggester.run()
    assert suggester.target_structure_two is not None
