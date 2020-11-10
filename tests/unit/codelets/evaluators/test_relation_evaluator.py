import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import RelationEvaluator
from homer.codelets.selectors import RelationSelector


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    concept = Mock()
    concept.classify.return_value = classification
    relation = Mock()
    relation.quality = current_quality
    relation.parent_concept = concept
    evaluator = RelationEvaluator(Mock(), Mock(), Mock(), relation, Mock())
    evaluator.run()
    assert classification == relation.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationSelector)
