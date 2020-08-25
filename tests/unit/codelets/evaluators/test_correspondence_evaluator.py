import math
import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import CorrespondenceEvaluator

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_passes_preliminary_checks():
    first_argument = Mock()
    second_argument = Mock()
    parent_concept = Mock()
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.first_argument = first_argument
    champion.second_argument = second_argument
    champion.parent_concept = parent_concept
    challenger = Mock()
    challenger.first_argument = first_argument
    challenger.second_argument = second_argument
    challenger.parent_concept = parent_concept
    evaluator = CorrespondenceEvaluator(
        Mock(), Mock(), Mock(), champion, challenger, Mock(), Mock()
    )
    assert evaluator._passes_preliminary_checks() is True
    champion.first_argument = second_argument
    champion.second_argument = first_argument
    assert evaluator._passes_preliminary_checks() is False


@pytest.mark.parametrize(
    "champion_connections, challenger_connections, expected",
    [(1.0, 0.9, 0.09), (0.9, 1.0, -0.09)],
)
def test_run_competition(champion_connections, challenger_connections, expected):
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.total_connection_activations.side_effect = [champion_connections]
    challenger = Mock()
    challenger.total_connection_activations.side_effect = [challenger_connections]
    evaluator = CorrespondenceEvaluator(
        Mock(), Mock(), Mock(), champion, challenger, Mock(), Mock()
    )
    actual = evaluator._run_competition()
    assert math.isclose(expected, actual, abs_tol=FLOAT_COMPARISON_TOLERANCE)
