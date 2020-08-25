import math
import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import GroupEvaluator

FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "champion_size, challenger_size, "
    + "champion_connections, challenger_connections, expected",
    [(10, 5, 5, 3, 0.75), (5, 10, 3, 5, -0.75)],
)
def test_run_competition(
    champion_size,
    challenger_size,
    champion_connections,
    challenger_connections,
    expected,
):
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.size = champion_size
    champion.total_connection_activations.side_effect = [champion_connections]
    challenger = Mock()
    challenger.size = challenger_size
    challenger.total_connection_activations.side_effect = [challenger_connections]
    evaluator = GroupEvaluator(
        Mock(), Mock(), Mock(), champion, challenger, Mock(), Mock()
    )
    actual = evaluator._run_competition()
    assert math.isclose(expected, actual, abs_tol=FLOAT_COMPARISON_TOLERANCE)
