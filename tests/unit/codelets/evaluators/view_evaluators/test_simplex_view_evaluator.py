import pytest
from unittest.mock import Mock

from linguoplotter.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from linguoplotter.codelets.selectors.view_selectors import SimplexViewSelector
from linguoplotter.structure_collection import StructureCollection


@pytest.mark.parametrize(
    "current_quality, correspondences_quality, no_of_frame_input_items, "
    + "no_of_matched_frame_items, no_of_frame_output_items, "
    + "no_of_projected_frame_items, output_quality, expected_view_quality",
    [
        (0.75, 0.5, 4, 2, 4, 2, 0.5, 0.5),
        (0.75, 1, 4, 4, 4, 0, 0.0, 0.5),
        (0.5, 0.75, 4, 3, 4, 3, 0.75, 0.75),
        (0.5, 1, 4, 0, 4, 0, 0, 0.25),
    ],
)
def test_changes_target_structure_quality(
    bubble_chamber,
    current_quality,
    correspondences_quality,
    no_of_frame_input_items,
    no_of_matched_frame_items,
    no_of_frame_output_items,
    no_of_projected_frame_items,
    output_quality,
    expected_view_quality,
):
    view = Mock()
    frame = Mock()

    frame.input_space.contents = bubble_chamber.new_structure_collection()
    for _ in range(no_of_matched_frame_items):
        item = Mock()
        item.is_correspondence = False
        item.correspondences.is_empty.return_value = False
        frame.input_space.contents.add(item)
    for _ in range(no_of_frame_input_items - no_of_matched_frame_items):
        item = Mock()
        item.is_correspondence = False
        item.correspondences.is_empty.return_value = True
        frame.input_space.contents.add(item)

    frame.output_space.contents = bubble_chamber.new_structure_collection()
    for _ in range(no_of_projected_frame_items):
        item = Mock()
        item.is_correspondence = False
        item.has_correspondence_to_space.return_value = True
        frame.output_space.contents.add(item)
    for _ in range(no_of_frame_output_items - no_of_projected_frame_items):
        item = Mock()
        item.is_correspondence = False
        item.has_correspondence_to_space.return_value = False
        frame.output_space.contents.add(item)
    view.parent_frame = frame

    view.output_space.quality = output_quality

    member_1 = Mock()
    member_1.quality = correspondences_quality
    member_2 = Mock()
    member_2.quality = correspondences_quality
    view.members = bubble_chamber.new_structure_collection(member_1, member_2)
    view.quality = current_quality

    evaluator = SimplexViewEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(view),
        Mock(),
    )
    evaluator.run()
    assert expected_view_quality == view.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], SimplexViewSelector)
