import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import ViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Relation
from homer.structures.nodes import Concept
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
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    return space


@pytest.fixture
def view_members():
    members = StructureCollection({Mock(), Mock()})
    return members


@pytest.fixture
def input_spaces():
    space_1 = Mock()
    space_2 = Mock()
    return StructureCollection({space_1, space_2})


@pytest.fixture
def good_view(bubble_chamber, target_space, view_members, input_spaces):
    view = View(
        Mock(),
        Mock(),
        Location([], target_space),
        view_members,
        input_spaces,
        Mock(),
        1.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def bad_view(bubble_chamber, target_space, view_members, input_spaces):
    view = View(
        Mock(),
        Mock(),
        Location([], target_space),
        view_members,
        input_spaces,
        Mock(),
        0.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


def test_good_view_is_boosted_bad_view_is_decayed(
    bubble_chamber, target_space, good_view, bad_view
):
    original_good_view_activation = good_view.activation
    original_bad_view_activation = bad_view.activation
    parent_id = ""
    champion = bad_view
    urgency = 1.0
    selector = ViewSelector.spawn(parent_id, bubble_chamber, champion, urgency)
    selector.run()
    good_view.update_activation()
    bad_view.update_activation()
    assert good_view.activation > original_good_view_activation
    assert bad_view.activation < original_bad_view_activation
