import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "correspondence": Mock()}
    concept = Mock()
    concept.classifier.classify.return_value = classification
    correspondence = Mock()
    correspondence.quality = current_quality
    correspondence.parent_concept = concept
    evaluator = CorrespondenceEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({correspondence}), Mock()
    )
    evaluator.run()
    assert classification == correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], CorrespondenceSelector)
