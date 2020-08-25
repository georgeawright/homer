import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import GroupLabelEvaluator


@pytest.mark.parametrize(
    "champion_proportion, challenger_proportion, "
    + "champion_proximity, challenger_proximity, expected",
    [
        (1.0, 0.0, 1.0, 0.0, 1.0),
        (0.0, 1.0, 0.0, 1.0, -1.0),
        (0.5, 0.5, 0.5, 0.5, 0.0),
        (1.0, 0.0, 0.0, 1.0, 0.0),
        (1.0, 0.0, 0.5, 0.5, 0.5),
    ],
)
def test_run_competition(
    champion_proportion,
    challenger_proportion,
    champion_proximity,
    challenger_proximity,
    expected,
):
    target_group = Mock()
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.parent_concept.proximity_to.side_effect = [champion_proximity]
    challenger = Mock()
    challenger.parent_concept.proximity_to.side_effect = [challenger_proximity]
    evaluator = GroupLabelEvaluator(
        Mock(), Mock(), Mock(), target_group, champion, challenger, Mock(), Mock()
    )
    evaluator.champion_proportion = champion_proportion
    evaluator.challenger_proportion = challenger_proportion
    assert expected == evaluator._run_competition()
