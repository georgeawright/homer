import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


@pytest.mark.parametrize(
    "current_quality, correspondences_quality, input_size, "
    + "raw_inputs_in_interpretation, output_space_quality, expected_quality",
    [
        (0, 1, 20, 20, 1, 1),
        (1, 0, 20, 0, 0, 0),
        (1, 0, 20, 20, 0.5, 0.25),
        (1, 1, 20, 10, 0.75, 0.5625),
        (1, 1, 20, 20, 0, 0),
    ],
)
def test_changes_target_structure_quality(
    current_quality,
    correspondences_quality,
    input_size,
    raw_inputs_in_interpretation,
    output_space_quality,
    expected_quality,
):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "view-monitoring": Mock()}

    conceptual_space = Mock()

    input_space = Mock()
    bubble_chamber.spaces = {"input": input_space}
    input_space.conceptual_spaces = StructureCollection({conceptual_space})
    input_space.contents = StructureCollection()
    raw_chunks = []
    for i in range(input_size):
        chunk = Mock()
        chunk.raw_members = StructureCollection({chunk})
        chunk.is_raw = True
        input_space.contents.add(chunk)
        raw_chunks.append(chunk)

    view = Mock()
    view.members = StructureCollection()
    for i in range(raw_inputs_in_interpretation):
        correspondence = Mock()
        correspondence.conceptual_space = conceptual_space
        correspondence.end.arguments = StructureCollection({raw_chunks[i]})
        correspondence.quality = correspondences_quality
        view.members.add(correspondence)

    view.output_space.quality = output_space_quality
    view.quality = current_quality

    evaluator = MonitoringViewEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({view}), Mock()
    )
    evaluator.run()
    assert expected_quality == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], MonitoringViewSelector)
