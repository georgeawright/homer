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
from homer.structures.links import Correspondence, Relation
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
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
    chamber.working_spaces.add(
        WorkingSpace(
            Mock(), Mock(), "top level working", StructureCollection(), Mock(), Mock()
        )
    )
    view_concept = Concept(
        Mock(), Mock(), "view", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(view_concept)
    build_concept = Concept(
        Mock(), Mock(), "build", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), view_concept, build_concept, None, None, 1)
    view_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_start_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
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
        Mock(),
        Mock(),
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
        Mock(),
        Mock(),
        StructureCollection({target_start_space}),
    )
    target_start_space.contents.add(start)
    return start


@pytest.fixture
def target_end(target_end_space):
    end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({target_end_space}),
    )
    target_end_space.contents.add(end)
    return end


@pytest.fixture
def first_correspondence(
    bubble_chamber, target_start, target_end, target_start_space, target_end_space
):
    parent_concept = Mock()
    parent_space = bubble_chamber.common_parent_space(
        target_start_space, target_end_space
    )
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
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
def second_correspondence(bubble_chamber, target_start_space, target_end_space):
    start = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    end = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    parent_concept = Mock()
    parent_space = bubble_chamber.common_parent_space(
        target_start_space, target_end_space
    )
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        target_start_space,
        target_end_space,
        parent_concept,
        parent_space,
        conceptual_space,
        quality,
    )
    start.links_out = StructureCollection({correspondence})
    start.links_in = StructureCollection({correspondence})
    end.links_out = StructureCollection({correspondence})
    end.links_in = StructureCollection({correspondence})
    parent_space.contents.add(correspondence)
    bubble_chamber.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def nearby_correspondence(bubble_chamber, target_start_space, target_end_space):
    start = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    end = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    parent_space = bubble_chamber.common_parent_space(
        target_start_space, target_end_space
    )
    correspondence = Correspondence(
        Mock(), Mock(), start, end, Mock(), Mock(), Mock(), parent_space, Mock(), 1.0
    )
    parent_space.contents.add(correspondence)
    bubble_chamber.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def target_view(bubble_chamber, first_correspondence, second_correspondence):
    view = View(
        Mock(),
        Mock(),
        StructureCollection({first_correspondence, second_correspondence}),
        bubble_chamber.spaces["top level working"],
        Mock(),
        0.0,
    )
    return view


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_view, nearby_correspondence
):
    parent_id = ""
    urgency = 1.0

    enlarger = ViewEnlarger.spawn(parent_id, bubble_chamber, target_view, urgency)
    assert 2 == target_view.size
    enlarger.run()
    assert CodeletResult.SUCCESS == enlarger.result
    assert 3 == target_view.size
    assert isinstance(enlarger.child_codelets[0], ViewEnlarger)
    enlarger = ViewEnlarger.spawn(parent_id, bubble_chamber, target_view, urgency)
    enlarger.run()
    assert CodeletResult.FIZZLE == enlarger.result
