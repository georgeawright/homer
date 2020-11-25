from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Relation


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
    relation = Relation(start, end, Mock(), Mock(), Mock())
    start.relations = StructureCollection({relation})
    end.relations = StructureCollection({relation})
    assert StructureCollection({relation_1, relation_2}) == relation.nearby()
