import pytest
from unittest.mock import Mock

from linguoplotter.codelets.evaluators import RelationEvaluator
from linguoplotter.codelets.selectors import RelationSelector
from linguoplotter.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, classification
):
    concept = Mock()
    concept.classifier.classify.return_value = classification
    relation = Mock()
    relation.quality = current_quality
    relation.parent_concept = concept
    evaluator = RelationEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(relation),
        Mock(),
    )
    evaluator.run()
    assert classification == relation.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationSelector)
