from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Label


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
    label = Label(Mock(), Mock(), start, Mock(), Mock(), Mock())
    start.labels = StructureCollection({label})
    assert StructureCollection({label_1, label_2}) == label.nearby()
