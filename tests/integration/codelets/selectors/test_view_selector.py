import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import ViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View
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
        Mock(),
    )
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(
        Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock(), Mock()
    )
    return space


@pytest.fixture
def view_members():
    members = StructureCollection({Mock(), Mock()})
    return members


@pytest.fixture
def good_view(bubble_chamber, target_space, view_members):
    view = View(
        Mock(),
        Mock(),
        view_members,
        Mock(),
        Mock(),
        1.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def bad_view(bubble_chamber, target_space, view_members):
    view = View(
        Mock(),
        Mock(),
        view_members,
        Mock(),
        Mock(),
        0.0,
    )
    target_space.contents.add(view)
    bubble_chamber.views.add(view)
    return view


def test_good_chunk_is_boosted_bad_chunk_is_decayed(
    bubble_chamber, target_space, good_view, bad_view
):
    parent_id = ""
    champion = bad_view
    urgency = 1.0
    selector = ViewSelector.spawn(parent_id, bubble_chamber, champion, urgency)
    for _ in range(20):
        selector.run()
        selector = selector.child_codelets[0]
        good_view.update_activation()
        bad_view.update_activation()
    assert 1 == good_view.activation
    assert 0 == bad_view.activation
