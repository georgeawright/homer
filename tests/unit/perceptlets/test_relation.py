import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.relation import Relation

FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "number_of_relations, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness(number_of_relations, expected_unhappiness):
    relation = Relation("value", Mock(), Mock(), Mock(), Mock(), Mock())
    for i in range(number_of_relations):
        relation.relations.add(Mock())
    assert math.isclose(
        expected_unhappiness, relation.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
