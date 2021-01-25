import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ViewBuilder
from homer.codelets.evaluators import ViewEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.chunks import View
from homer.structures.links import Correspondence, Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace


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
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    text_concept = Concept(
        Mock(), Mock(), "text", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(text_concept)
    text_conceptual_space = ConceptualSpace(
        Mock(), Mock(), "text", text_concept, [], StructureCollection(), 1, [], []
    )
    chamber.conceptual_spaces.add(text_conceptual_space)
    chamber.working_spaces.add(
        WorkingSpace(
            Mock(),
            Mock(),
            "top level working",
            Mock(),
            Mock(),
            [],
            StructureCollection(),
            0,
            [],
            [],
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
def target_start_space(bubble_chamber):
    space = WorkingSpace(
        Mock(),
        Mock(),
        "start",
        Mock(),
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.fixture
def target_end_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
        "end",
        Mock(),
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
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
def target_view_correspondence(
    bubble_chamber, target_start, target_end, target_start_space, target_end_space
):
    parent_concept = Mock()
    parent_space = bubble_chamber.get_super_space(target_start_space, target_end_space)
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        target_start,
        target_end,
        Location(Mock(), parent_space),
        target_start_space,
        target_end_space,
        parent_concept,
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
def second_target_view_correspondence(
    bubble_chamber, target_start_space, target_end_space
):
    start = Mock()
    end = Mock()
    parent_concept = Mock()
    parent_space = bubble_chamber.get_super_space(target_start_space, target_end_space)
    conceptual_space = Mock()
    quality = 1.0
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        Location(Mock(), parent_space),
        target_start_space,
        target_end_space,
        parent_concept,
        conceptual_space,
        quality,
    )
    parent_space.contents.add(correspondence)
    bubble_chamber.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def target_view(bubble_chamber, target_view_correspondence):
    view = View(
        Mock(),
        Mock(),
        Location([], bubble_chamber.spaces["top level working"]),
        StructureCollection({target_view_correspondence}),
        Mock(),
        Mock(),
        1.0,
    )
    bubble_chamber.spaces["top level working"].add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def second_target_view(bubble_chamber, second_target_view_correspondence):
    view = View(
        Mock(),
        Mock(),
        Location([], bubble_chamber.spaces["top level working"]),
        StructureCollection({second_target_view_correspondence}),
        Mock(),
        Mock(),
        1.0,
    )
    bubble_chamber.spaces["top level working"].add(view)
    bubble_chamber.views.add(view)
    return view


def test_successful_adds_members_to_view_and_spawns_follow_up_and_same_view_cannot_be_recreated(
    bubble_chamber,
    target_view,
    second_target_view,
):
    parent_id = ""
    urgency = 1.0
    builder = ViewBuilder.spawn(parent_id, bubble_chamber, target_view, urgency)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, View)
    assert isinstance(builder.child_codelets[0], ViewEvaluator)
    builder = ViewBuilder.spawn(parent_id, bubble_chamber, target_view, urgency)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
