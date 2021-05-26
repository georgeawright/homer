import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.label_evaluators import LabelProjectionEvaluator
from homer.codelets.selectors.label_selectors import LabelProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "label": Mock()}
    label = Mock()
    label.quality = current_quality
    correspondence = Mock()
    correspondence.quality = current_quality
    correspondence.is_correspondence = True
    correspondence.start.quality = classification
    evaluator = LabelProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({label, correspondence}),
        Mock(),
    )
    evaluator.run()
    assert classification == label.quality
    assert classification == correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelProjectionSelector)
