import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Relation


def test_copy(bubble_chamber):
    old_start = Mock()
    old_end = Mock()
    new_start = Mock()
    new_end = Mock()
    parent_id = "id"
    relation = Relation(
        Mock(),
        Mock(),
        old_start,
        old_end,
        StructureCollection(bubble_chamber, [old_start, old_end]),
        Mock(),
        Mock(),
        [Mock(), Mock()],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    copy = relation.copy(
        start=new_start, end=new_end, parent_id=parent_id, bubble_chamber=bubble_chamber
    )
    assert relation.start == old_start
    assert relation.end == old_end
    assert copy.start == new_start
    assert copy.end == new_end
    assert copy.parent_id == parent_id


def test_nearby(bubble_chamber):
    start = Mock()
    end = Mock()
    relation = Relation(
        Mock(),
        Mock(),
        start,
        end,
        StructureCollection(bubble_chamber, [start, end]),
        Mock(),
        Mock(),
        [Mock(), Mock()],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    start.relations = StructureCollection(bubble_chamber, [relation])
    end.relations = StructureCollection(bubble_chamber, [relation])
    assert StructureCollection(Mock(), []) == relation.nearby()
