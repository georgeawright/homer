import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Concept
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import SimplexView


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
    view_concept = Concept(
        Mock(),
        Mock(),
        "view",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(view_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), view_concept, build_concept, None, None, 1)
    view_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    top_level_working_space = WorkingSpace(
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
    chamber.working_spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def input_space(bubble_chamber):
    space = WorkingSpace(
        Mock(), Mock(), "input", Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    space._activation = 1.0
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.fixture
def target_frame(bubble_chamber):
    frame = Frame(Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection())
    frame._activation = 1.0
    bubble_chamber.frames.add(frame)
    return frame


def test_successful_creates_view_and_spawns_follow_up_and_same_view_cannot_be_recreated(
    bubble_chamber,
    input_space,
    target_frame,
):
    parent_id = ""
    urgency = 1.0
    target_spaces = StructureCollection({input_space, target_frame})
    builder = SimplexViewBuilder.spawn(
        parent_id, bubble_chamber, target_spaces, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, SimplexView)
    assert isinstance(builder.child_codelets[0], SimplexViewEvaluator)
    builder = SimplexViewBuilder.spawn(
        parent_id, bubble_chamber, target_spaces, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
