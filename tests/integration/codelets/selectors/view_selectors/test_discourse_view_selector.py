import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.view_selectors import DiscourseViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import DiscourseView, MonitoringView


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
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(view_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), view_concept, select_concept, None, None, 1)
    view_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
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
    input_concept = Concept(
        Mock(), Mock(), "input", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(input_concept)
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        input_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.working_spaces.add(input_space)
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
    frame = Frame("", "", "", discourse_concept, Mock(), [], StructureCollection())
    chamber.frames.add(frame)
    monitoring_view_one = MonitoringView(
        "", "", Mock(), Mock(), Mock(), text_space_one, 0.0
    )
    chamber.views.add(monitoring_view_one)
    monitoring_view_two = MonitoringView(
        "", "", Mock(), Mock(), Mock(), text_space_two, 0.0
    )
    chamber.views.add(monitoring_view_two)
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    return space


@pytest.fixture
def common_target_space_item(bubble_chamber):
    item = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), bubble_chamber.spaces["input"], Mock()
    )
    return item


@pytest.fixture
def input_spaces():
    space_1 = Mock()
    space_2 = Mock()
    return StructureCollection({space_1, space_2})


@pytest.fixture
def good_view(bubble_chamber, target_space, input_spaces, common_target_space_item):
    correspondence = Correspondence(
        "",
        "",
        common_target_space_item,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    view = DiscourseView(
        Mock(),
        Mock(),
        Location([], target_space),
        StructureCollection({correspondence}),
        input_spaces,
        Mock(),
        1.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def bad_view(bubble_chamber, target_space, input_spaces, common_target_space_item):
    correspondence = Correspondence(
        "",
        "",
        common_target_space_item,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    view = DiscourseView(
        Mock(),
        Mock(),
        Location([], target_space),
        StructureCollection({correspondence}),
        input_spaces,
        Mock(),
        0.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.mark.skip
def test_good_view_is_boosted_bad_view_is_decayed(bubble_chamber, good_view, bad_view):
    original_good_view_activation = good_view.activation
    original_bad_view_activation = bad_view.activation
    parent_id = ""
    champion = bad_view
    urgency = 1.0
    selector = DiscourseViewSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    good_view.update_activation()
    bad_view.update_activation()
    assert bad_view.activation < original_bad_view_activation
    assert good_view.activation > original_good_view_activation
