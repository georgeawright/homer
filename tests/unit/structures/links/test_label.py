import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Label


def test_copy():
    old_start = Mock()
    new_start = Mock()
    parent_id = "id"
    label = Label(Mock(), Mock(), old_start, Mock(), [Mock(), Mock()], Mock())
    copy = label.copy(start=new_start, parent_id=parent_id)
    assert label.start == old_start
    assert copy.start == new_start
    assert copy.parent_id == parent_id


def test_nearby():
    label_1 = Mock()
    chunk_1 = Mock()
    chunk_1.labels = StructureCollection({label_1})
    label_2 = Mock()
    chunk_2 = Mock()
    chunk_2.labels = StructureCollection({label_2})
    nearby_chunks = StructureCollection({chunk_1, chunk_2})
    start = Mock()
    start.nearby.return_value = nearby_chunks
    label = Label(Mock(), Mock(), start, Mock(), [Mock(), Mock()], Mock())
    start.labels = StructureCollection({label})
    assert StructureCollection({label_1, label_2}) == label.nearby()
