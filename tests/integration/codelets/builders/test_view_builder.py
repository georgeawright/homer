import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ViewBuilder, ViewEnlarger
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.chunks import View
from homer.structures.links import Correspondence
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
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
    return chamber


@pytest.fixture
def target_start_space():
    space = WorkingSpace(
        "start",
        StructureCollection(),
        Mock(),
        Mock(),
        parent_spaces=StructureCollection(),
    )
    return space


@pytest.fixture
def target_end_space():
    space = WorkingSpace(
        "end",
        StructureCollection(),
        Mock(),
        Mock(),
        parent_spaces=StructureCollection(),
    )
    return space


@pytest.fixture
def target_start(target_start_space):
    start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({target_start_space}),
    )
    target_start_space.contents.add(start)
    return start


@pytest.fixture
def target_end(target_end_space):
    end = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), StructureCollection({target_end_space})
    )
    target_end_space.contents.add(end)
    return end


@pytest.fixture
def target_correspondence(
    bubble_chamber, target_start, target_end, target_start_space, target_end_space
):
    parent_concept = Mock()
    parent_space = bubble_chamber.common_parent_space(
        target_start_space, target_end_space
    )
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        target_start,
        target_end,
        target_start_space,
        target_end_space,
        parent_concept,
        parent_space,
        conceptual_space,
        quality,
    )
    target_start.links_in.add(correspondence)
    target_start.links_out.add(correspondence)
    target_end.links_in.add(correspondence)
    target_end.links_out.add(correspondence)
    parent_space.contents.add(correspondence)
    bubble_chamber.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def second_target_correspondence(bubble_chamber, target_start_space, target_end_space):
    start = Mock()
    end = Mock()
    parent_concept = Mock()
    parent_space = bubble_chamber.common_parent_space(
        target_start_space, target_end_space
    )
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        start,
        end,
        target_start_space,
        target_end_space,
        parent_concept,
        parent_space,
        conceptual_space,
        quality,
    )
    parent_space.contents.add(correspondence)
    bubble_chamber.correspondences.add(correspondence)
    return correspondence


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_correspondence, second_target_correspondence
):
    parent_id = ""
    urgency = 1.0

    builder = ViewBuilder.spawn(
        parent_id, bubble_chamber, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, View)
    assert isinstance(builder.child_codelets[0], ViewEnlarger)
    builder = ViewBuilder.spawn(
        parent_id, bubble_chamber, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
