from unittest.mock import Mock

from homer.codelets.evaluators import RawPerceptletLabelEvaluator


def test_engender_follow_up():
    target_label = Mock()
    target_label.location = [0, 0, 0]
    raw_perceptlet = Mock()
    raw_perceptlet.labels.get_active.side_effect = [target_label]
    bubble_chamber = Mock()
    bubble_chamber.workspace.raw_perceptlets.get_active.side_effect = [raw_perceptlet]
    evaluator = RawPerceptletLabelEvaluator(
        bubble_chamber, Mock(), Mock(), target_label, Mock(), Mock()
    )
    follow_up = evaluator._engender_follow_up()
    assert RawPerceptletLabelEvaluator == type(follow_up)
