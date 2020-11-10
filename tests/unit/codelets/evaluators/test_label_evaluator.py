import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import LabelEvaluator
from homer.codelets.selectors import LabelSelector


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    concept = Mock()
    concept.classify.return_value = classification
    label = Mock()
    label.quality = current_quality
    label.parent_concept = concept
    evaluator = LabelEvaluator(Mock(), Mock(), Mock(), label, Mock())
    evaluator.run()
    assert classification == label.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelSelector)
