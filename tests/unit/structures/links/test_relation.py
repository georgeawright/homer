import pytest
from unittest.mock import Mock

from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Relation


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
        Mock(),
    )
    start.relations = StructureCollection(bubble_chamber, [relation])
    end.relations = StructureCollection(bubble_chamber, [relation])
    assert StructureCollection(Mock(), []) == relation.nearby()
