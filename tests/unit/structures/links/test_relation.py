from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Relation


def test_copy():
    old_start = Mock()
    old_end = Mock()
    new_start = Mock()
    new_end = Mock()
    parent_id = "id"
    relation = Relation(Mock(), Mock(), old_start, old_end, Mock(), Mock(), Mock())
    copy = relation.copy(start=new_start, end=new_end, parent_id=parent_id)
    assert relation.start == old_start
    assert relation.end == old_end
    assert copy.start == new_start
    assert copy.end == new_end
    assert copy.parent_id == parent_id


def test_nearby():
    relation_1 = Mock()
    chunk_1 = Mock()
    chunk_1.relations = StructureCollection({relation_1})
    relation_2 = Mock()
    chunk_2 = Mock()
    chunk_2.relations = StructureCollection({relation_2})
    nearby_chunks = StructureCollection({chunk_1, chunk_2})
    start = Mock()
    start.nearby.return_value = nearby_chunks
    end = Mock()
    end.nearby.return_value = nearby_chunks
    relation = Relation(Mock(), Mock(), start, end, Mock(), Mock(), Mock())
    start.relations = StructureCollection({relation})
    end.relations = StructureCollection({relation})
    assert StructureCollection({relation_1, relation_2}) == relation.nearby()
