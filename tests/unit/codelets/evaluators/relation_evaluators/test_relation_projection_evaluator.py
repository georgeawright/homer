import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.relation_evaluators import RelationProjectionEvaluator
from homer.codelets.selectors.relation_selectors import RelationProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "relation": Mock()}
    relation = Mock()
    relation.quality = current_quality
    correspondence = Mock()
    correspondence.quality = current_quality
    correspondence.is_correspondence = True
    correspondence.start.quality = classification
    evaluator = RelationProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({relation, correspondence}),
        Mock(),
    )
    evaluator.run()
    assert classification == relation.quality
    assert classification == correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationProjectionSelector)
