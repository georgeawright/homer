import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


@pytest.mark.parametrize(
    "current_quality, correspondences_quality, interpretation_size, "
    + "no_of_chunks_with_members, expected_quality",
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
    interpretation_size,
    no_of_chunks_with_members,
    expected_quality,
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "view": Mock()}
    interpretation_chunks = []
    for i in range(interpretation_size):
        chunk = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
        interpretation_chunks.append(chunk)
    correspondences = []
    for i in range(no_of_chunks_with_members):
        correspondence = Mock()
        correspondence.quality = correspondences_quality
        correspondences.append(correspondence)
        interpretation_chunks[i].members.is_empty.return_value = False
    view = Mock()
    view.interpretation_space = Mock()
    view.interpretation_space.contents = StructureCollection(set(interpretation_chunks))
    view.members = StructureCollection(set(correspondences))
    view.quality = current_quality
    monitoring_views_collection = StructureCollection({view})
    bubble_chamber.monitoring_views.where.return_value = monitoring_views_collection
    evaluator = MonitoringViewEvaluator(Mock(), Mock(), bubble_chamber, view, Mock())
    evaluator.run()
    assert expected_quality == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], MonitoringViewSelector)
