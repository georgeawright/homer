import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import DiscourseViewBuilder
from homer.codelets.suggesters.view_suggesters import DiscourseViewSuggester
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Concept
from homer.structures.spaces import WorkingSpace
from homer.structures.spaces.frames import Template
from homer.structures.views import DiscourseView, MonitoringView
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    view_concept = Concept(
        Mock(),
        Mock(),
        "view-discourse",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(view_concept)
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(Mock(), Mock(), view_concept, suggest_concept, None, None, 1)
    view_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    discourse_concept = Concept(
        Mock(),
        Mock(),
        "discourse",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(discourse_concept)
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
    text_space_one = WorkingSpace(
        "",
        "",
        "text1",
        text_concept,
        Mock(),
        [],
        StructureCollection({Mock()}),
        1,
        [],
        [],
    )
    chamber.working_spaces.add(text_space_one)
    text_space_two = WorkingSpace(
        "",
        "",
        "text2",
        text_concept,
        Mock(),
        [],
        StructureCollection({Mock()}),
        1,
        [],
        [],
    )
    chamber.working_spaces.add(text_space_two)
    frame = Template("", "", "", discourse_concept, Mock(), [], StructureCollection())
    chamber.frames.add(frame)
    monitoring_view_one = MonitoringView(
        "",
        "",
        Mock(),
        Mock(),
        StructureCollection({text_space_one}),
        text_space_one,
        0.0,
    )
    chamber.views.add(monitoring_view_one)
    monitoring_view_two = MonitoringView(
        "",
        "",
        Mock(),
        Mock(),
        StructureCollection({text_space_two}),
        text_space_two,
        0.0,
    )
    chamber.views.add(monitoring_view_two)
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
    frame = Template(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection(),
    )
    frame._activation = 1.0
    bubble_chamber.frames.add(frame)
    return frame


@pytest.mark.skip
def test_successful_creates_view_and_spawns_follow_up_and_same_view_cannot_be_recreated(
    bubble_chamber,
    input_space,
    target_frame,
):
    parent_id = ""
    urgency = 1.0
    target_spaces = StructureCollection({input_space, target_frame})
    suggester = DiscourseViewSuggester.spawn(
        parent_id, bubble_chamber, target_spaces, urgency
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], DiscourseViewBuilder)
