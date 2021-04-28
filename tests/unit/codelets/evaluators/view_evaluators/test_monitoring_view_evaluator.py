import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize(
    "current_quality, correspondences_quality, raw_input_size, "
    + "no_of_raw_correspondences, expected_quality",
    [
        (0, 1, 20, 20, 1),
        (1, 0, 20, 0, 0),
        (1, 0, 20, 20, 0.5),
        (1, 1, 20, 10, 0.75),
    ],
)
def test_changes_target_structure_quality(
    current_quality,
    correspondences_quality,
    raw_input_size,
    no_of_raw_correspondences,
    expected_quality,
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "view": Mock()}
    raw_input_contents = []
    for i in range(raw_input_size):
        raw_item = Mock()
        raw_item.is_raw = True
        raw_input_contents.append(raw_item)
    view = Mock()
    view.raw_input_space = Mock()
    view.raw_input_space.contents = StructureCollection(set(raw_input_contents))
    correspondences = []
    for i in range(no_of_raw_correspondences):
        correspondence = Mock()
        correspondence.start = raw_input_contents[i]
        correspondence.quality = correspondences_quality
        correspondences.append(correspondence)
    view.members = StructureCollection(set(correspondences))
    view.quality = current_quality
    evaluator = MonitoringViewEvaluator(Mock(), Mock(), bubble_chamber, view, Mock())
    evaluator.run()
    assert expected_quality == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], MonitoringViewSelector)
