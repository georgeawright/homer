import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.spaces import Frame, WorkingSpace


def test_nearby():
    top_level_working_space = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    input_1 = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    input_2 = WorkingSpace(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    frame_1 = Frame(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    frame_2 = Frame(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    view_1 = View(
        Mock(),
        Mock(),
        Location([], top_level_working_space),
        StructureCollection(),
        StructureCollection({input_1, frame_1}),
        Mock(),
        Mock(),
    )
    view_2 = View(
        Mock(),
        Mock(),
        Location([], top_level_working_space),
        StructureCollection(),
        StructureCollection({input_1, frame_2}),
        Mock(),
        Mock(),
    )
    view_3 = View(
        Mock(),
        Mock(),
        Location([], top_level_working_space),
        StructureCollection(),
        StructureCollection({input_2, frame_1}),
        Mock(),
        Mock(),
    )
    top_level_working_space.add(view_1)
    top_level_working_space.add(view_2)
    top_level_working_space.add(view_3)
    assert view_2 in view_1.nearby()
    assert view_1 in view_2.nearby()
    assert view_3 not in view_1.nearby()
    assert view_3 not in view_2.nearby()
