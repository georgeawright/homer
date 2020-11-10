import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.selectors import CorrespondenceSelector


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    concept = Mock()
    concept.classify.return_value = classification
    correspondence = Mock()
    correspondence.quality = current_quality
    correspondence.parent_concept = concept
    evaluator = CorrespondenceEvaluator(Mock(), Mock(), Mock(), correspondence, Mock())
    evaluator.run()
    assert classification == correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)
