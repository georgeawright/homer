import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters.correspondence_suggesters import (
    SubFrameToFrameCorrespondenceSuggester,
)


def test_gets_target_space_one_if_necessary(bubble_chamber):
    target_conceptual_space = Mock()
    target_structure_two = Mock()
    target_structure_two.is_link = True
    target_structure_two.is_node = False
    target_structure_two.is_label = True
    target_structure_two.parent_concept.parent_space = target_conceptual_space
    target_space_two = Mock()
    target_structure_two.parent_space = target_space_two
    target_view = Mock()
    frame_one = Mock()
    frame_two = Mock()
    frame_two.input_space = target_space_two
    target_view.matched_sub_frames = {frame_two: frame_one}

    target_structures = {
        "target_structure_two": target_structure_two,
        "target_space_two": target_space_two,
        "target_view": target_view,
    }

    correspondence_suggester = SubFrameToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.target_space_one is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_space_one is not None
    assert CodeletResult.FIZZLE == correspondence_suggester.result


def test_gets_target_structure_one_if_necessary(bubble_chamber):
    label_parent_concept = Mock()
    label_parent_concept.is_slot = True
    target_conceptual_space = Mock()
    target_conceptual_space.contents = bubble_chamber.new_structure_collection(
        label_parent_concept
    )
    target_structure_two_start = Mock()
    target_structure_two_start.is_label = False
    target_structure_two = Mock()
    target_structure_two.is_link = True
    target_structure_two.is_node = False
    target_structure_two.is_label = True
    target_structure_two.is_relation = False
    target_structure_two.start = target_structure_two_start
    target_structure_two.parent_concept.is_slot = True
    target_structure_two.parent_concept.parent_space = target_conceptual_space
    target_space_two = Mock()
    target_structure_two.parent_space = target_space_two
    target_view = Mock()
    target_space_one = Mock()
    frame_one = Mock()
    frame_one.input_space = target_space_one
    frame_two = Mock()
    frame_two.input_space = target_space_two
    target_structure_one_start = Mock()
    target_structure_one_start.is_label = False
    target_view.matched_sub_frames = {frame_two: frame_one}
    target_view.grouped_nodes = bubble_chamber.new_structure_collection(
        target_structure_two_start
    )
    target_view.node_groups = [
        {
            target_space_two: target_structure_two_start,
            target_space_one: target_structure_one_start,
        }
    ]
    target_structure_one = Mock()
    target_structure_one.is_label = True
    target_structure_one.start = target_structure_one_start
    target_structure_one.has_location_in_space.return_value = True
    target_structure_one.parent_concept = label_parent_concept
    target_structure_one.labels = bubble_chamber.new_structure_collection()
    target_structure_one.corresponding_exigency = 1.0
    target_structure_one_start.labels = bubble_chamber.new_structure_collection(
        target_structure_one
    )
    target_space_one.contents = bubble_chamber.new_structure_collection(
        target_structure_one_start, target_structure_one
    )

    target_structures = {
        "target_structure_two": target_structure_two,
        "target_space_two": target_space_two,
        "target_view": target_view,
    }

    correspondence_suggester = SubFrameToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.target_structure_one is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_structure_one is not None
