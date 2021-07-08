import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.codelets.selectors.view_selectors import SimplexViewSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize(
    "current_quality, correspondences_quality, no_of_slots, no_of_slot_values",
    [(0.75, 0.5, 4, 2), (0.5, 0.75, 4, 3)],
)
def test_changes_target_structure_quality(
    current_quality, correspondences_quality, no_of_slots, no_of_slot_values
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "view-simplex": Mock()}
    view = Mock()
    view.slots = [Mock() for _ in range(no_of_slots)]
    view.slot_values = {Mock(): Mock() for _ in range(no_of_slot_values)}
    member_1 = Mock()
    member_1.quality = correspondences_quality
    member_2 = Mock()
    member_2.quality = correspondences_quality
    view.members = StructureCollection({member_1, member_2})
    view.quality = current_quality
    evaluator = SimplexViewEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({view}), Mock()
    )
    evaluator.run()
    assert correspondences_quality == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], SimplexViewSelector)
