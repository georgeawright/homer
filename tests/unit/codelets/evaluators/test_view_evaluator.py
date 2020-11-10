import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import ViewEvaluator
from homer.codelets.selectors import ViewSelector
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    view = Mock()
    member_1 = Mock()
    member_1.quality = classification
    member_2 = Mock()
    member_2.quality = classification
    view.members = StructureCollection({member_1, member_2})
    view.quality = current_quality
    evaluator = ViewEvaluator(Mock(), Mock(), Mock(), view, Mock())
    evaluator.run()
    assert classification == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ViewSelector)
