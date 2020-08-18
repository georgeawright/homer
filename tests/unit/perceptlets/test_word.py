import math
import pytest
from unittest.mock import Mock, patch

from homer.activation_patterns import WorkspaceActivationPattern
from homer.perceptlets.word import Word

FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "strength, concept_activation, expected_importance",
    [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (1.0, 0, 0.5)],
)
def test_importance(strength, concept_activation, expected_importance):
    with patch.object(
        WorkspaceActivationPattern,
        "get_activation_as_scalar",
        return_value=concept_activation,
    ):
        activation_pattern = WorkspaceActivationPattern(Mock())
        parent_concept = Mock()
        parent_concept.activation_pattern = activation_pattern
        word = Word("value", parent_concept, strength, Mock())
        assert expected_importance == word.importance


@pytest.mark.parametrize(
    "number_of_relations, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness(number_of_relations, expected_unhappiness):
    word = Word("value", Mock(), Mock(), Mock())
    for i in range(number_of_relations):
        word.relations.add(Mock())
    assert math.isclose(
        expected_unhappiness, word.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
