from unittest.mock import Mock

from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.selectors import CorrespondenceSelector


def test_engender_follow_up():
    target_correspondence = Mock()
    target_correspondence.location = [0, 0, 0]
    bubble_chamber = Mock()
    bubble_chamber.concept_space = {"correspondence-selection": Mock()}
    collection = Mock()
    collection.get_most_active.side_effect = [target_correspondence]
    bubble_chamber.workspace.correspondences.at.side_effect = [collection]
    evaluator = CorrespondenceEvaluator(
        bubble_chamber, Mock(), Mock(), target_correspondence, Mock(), Mock()
    )
    follow_up = evaluator._engender_follow_up()
    assert CorrespondenceSelector == type(follow_up)
