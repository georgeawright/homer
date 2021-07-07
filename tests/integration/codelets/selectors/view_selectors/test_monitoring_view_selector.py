import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    view_concept = Concept(
        Mock(),
        Mock(),
        "view-monitoring",
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
    input_space = WorkingSpace(
        Mock(), Mock(), "input", Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    chamber.working_spaces.add(input_space)
    text_working_space = WorkingSpace(
        "", "", "", text_concept, Mock(), [], StructureCollection({Mock()}), 1, [], []
    )
    chamber.working_spaces.add(text_working_space)
    chamber.frames.add(Mock())
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    return space


@pytest.fixture
def raw_input_space():
    space = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    return space


@pytest.fixture
def raw_item_one(raw_input_space):
    item = Chunk(
        "",
        "",
        [Location([], raw_input_space)],
        Mock(),
        raw_input_space,
        Mock(),
        is_raw=True,
    )
    raw_input_space.add(item)
    return item


@pytest.fixture
def raw_item_two(raw_input_space):
    item = Chunk(
        "",
        "",
        [Location([], raw_input_space)],
        Mock(),
        raw_input_space,
        Mock(),
        is_raw=True,
    )
    raw_input_space.add(item)
    return item


@pytest.fixture
def good_view(
    bubble_chamber, target_space, raw_input_space, raw_item_one, raw_item_two
):
    text_space = Mock()
    interpretation_space = Mock()
    correspondence_to_item_one = Correspondence(
        "",
        "",
        raw_item_one,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence_to_item_two = Correspondence(
        "",
        "",
        raw_item_two,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    view_members = StructureCollection(
        {correspondence_to_item_one, correspondence_to_item_two}
    )
    view = MonitoringView(
        "good_view",
        "",
        Location([], target_space),
        view_members,
        StructureCollection({text_space, raw_input_space, interpretation_space}),
        text_space,
        1.0,
    )
    target_space.add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def bad_view(bubble_chamber, target_space, raw_input_space, raw_item_one):
    text_space = Mock()
    interpretation_space = Mock()
    interpretation_space.parent_concept.name = "interpretation"
    correspondence_to_item_one = Correspondence(
        "",
        "",
        raw_item_one,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    view_members = StructureCollection({correspondence_to_item_one})
    view = MonitoringView(
        "bad_view",
        "",
        Location([], target_space),
        view_members,
        StructureCollection({text_space, raw_input_space, interpretation_space}),
        Mock(),
        0.0,
    )
    target_space.add(view)
    bubble_chamber.views.add(view)
    return view


def test_good_view_is_boosted_bad_view_is_decayed(bubble_chamber, good_view, bad_view):
    original_good_view_activation = good_view.activation
    original_bad_view_activation = bad_view.activation
    parent_id = ""
    champion = bad_view
    urgency = 1.0
    selector = MonitoringViewSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    assert selector.result == CodeletResult.SUCCESS
    good_view.update_activation()
    bad_view.update_activation()
    assert good_view.activation > original_good_view_activation
    assert bad_view.activation < original_bad_view_activation
