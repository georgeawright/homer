import math
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder, ChunkEnlarger
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.spaces import WorkingSpace


def test_successful_adds_member_to_chunk_and_spawns_follow_up():
    parent_id = ""
    urgency = 1.0
    bubble_chamber = BubbleChamber(
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    input_space = WorkingSpace(StructureCollection(), 0, location_concept)
    parent_spaces = StructureCollection({input_space})
    target_chunk = Chunk(
        10,
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    second_chunk = Chunk(
        10,
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    bubble_chamber.chunks.add(target_chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(target_chunk)
    input_space.contents.add(second_chunk)
    target_chunk.parent_spaces.add(input_space)
    builder = ChunkBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert isinstance(builder.child_structure, Chunk)
    assert isinstance(builder.child_codelets[0], ChunkEnlarger)
