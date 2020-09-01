from unittest.mock import Mock, patch

from homer.codelets.evaluators import GroupLabelEvaluator
from homer.codelets.selectors import GroupLabelSelector
from homer.perceptlet_collection import PerceptletCollection


def test_engender_follow_up():
    target_group = Mock()
    target_group.location = [0, 0, 0]
    with patch.object(
        PerceptletCollection, "get_most_active", return_value=target_group
    ):
        at = PerceptletCollection()
        with patch.object(PerceptletCollection, "at", return_value=at):
            bubble_chamber = Mock()
            bubble_chamber.workspace.groups = PerceptletCollection()
            bubble_chamber.concept_space = {"group-label-selection": Mock()}
            evaluator = GroupLabelEvaluator(
                bubble_chamber, Mock(), Mock(), target_group, Mock(), Mock()
            )
            follow_up = evaluator._engender_follow_up()
            assert GroupLabelSelector == type(follow_up)
